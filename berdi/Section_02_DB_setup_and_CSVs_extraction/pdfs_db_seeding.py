import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from sqlalchemy import text
import pandas as pd
import PyPDF2
from berdi.Database_Connection_Files.connect_to_database import connect_to_db
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).parents[2].resolve()
RAW_DATA = "data/raw"
OLD_PROJECTS = "Index_of_PDFs_for_Major_Projects_with_ESAs.csv"
NEW_PROJECTS = "Phase2_Index_of_PDFs_for_Major_Projects_with_ESAs.csv"

# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=REPO_ROOT / "berdi/Database_Connection_Files" / ".env", override=True
)
engine = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path and Index filepath
pdf_files_folder = REPO_ROOT / RAW_DATA / "pdfs"
index = REPO_ROOT / RAW_DATA / "index_for_projects" / NEW_PROJECTS

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
if not index.exists():
    print(index, "does not exist!")


def insert_pdfs():
    df = pd.read_csv(index)  # getting permission error on Windows
    df = df[
        [
            "Data ID",
            "Application Name",
            "Application Short Name",
            "Commodity",
            "Hearing Order",
        ]
    ]
    df = df.rename(
        columns={
            "Data ID": "pdfId",
            "Commodity": "commodity",
            "Hearing Order": "hearingOrder",
            "Application Short Name": "short_name",
            "Application Name": "application_title_short",
        }
    )

    with engine.connect() as conn:
        for row in df.itertuples():
            try:
                r = conn.execute("SELECT * from pdfs WHERE pdfId = %s;", (row.pdfId,))
                if r.rowcount == 1:
                    continue

                pdf_path = pdf_files_folder.joinpath(f"{row.pdfId}.pdf")
                with pdf_path.open("rb") as pdf:
                    reader = PyPDF2.PdfFileReader(pdf)
                    if reader.isEncrypted:
                        reader.decrypt("")
                    total_pages = reader.getNumPages()

                stmt = text(
                    "INSERT INTO pdfs (pdfId, totalPages, hearingOrder, application_title_short,"
                    + "short_name, commodity) VALUES (:pdfId, :totalPages, :hearingOrder,"
                    + ":application_title_short, :short_name, :commodity);"
                )
                params = {
                    "pdfId": row.pdfId,
                    "totalPages": total_pages,
                    "hearingOrder": None
                    if pd.isna(row.hearingOrder)
                    else row.hearingOrder,
                    "application_title_short": row.application_title_short,
                    "short_name": row.short_name,
                    "commodity": row.commodity,
                }
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    return print(f"{row.pdfId}: ERROR! Updated {result.rowcount} rows!")
                print(f"Inserted {result.rowcount} for {row.pdfId}")
            except Exception as e:
                print(f"Error for {row.pdfId}: {e}")
    print("All done")


if __name__ == "__main__":
    insert_pdfs()
