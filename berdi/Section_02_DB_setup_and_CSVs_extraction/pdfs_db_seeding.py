import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from sqlalchemy import text
import pandas as pd
import PyPDF2
from berdi.Database_Connection_Files.connect_to_sqlserver_database import connect_to_db
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).parents[2].resolve()
RAW_DATA = "data/raw"
OLD_PROJECTS = "Index_of_PDFs_for_Major_Projects_with_ESAs.csv"
NEW_PROJECTS = "Phase3_Index_of_PDFs_for_Major_Projects_with_ESAs.csv"

# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=REPO_ROOT / "berdi/Database_Connection_Files" / ".env", override=True
)
conn = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path and Index filepath
pdf_files_folder = REPO_ROOT / RAW_DATA / "pdfs"
index = REPO_ROOT / RAW_DATA / "index_for_projects" / NEW_PROJECTS

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
if not index.exists():
    print(index, "does not exist!")


def insert_pdfs():
    df = pd.read_csv(index, encoding = 'cp1252')  # getting permission error on Windows
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

    with conn:
        cursor = conn.cursor()
        print(cursor)
        for row in df.itertuples():
            try:
                r = cursor.execute("SELECT * FROM [DS_TEST].BERDI.pdfs WHERE pdfId = ?;", (row.pdfId))
                if r.rowcount == 1:
                    continue

                pdf_path = pdf_files_folder.joinpath(f"{row.pdfId}.pdf")
                with pdf_path.open("rb") as pdf:
                    reader = PyPDF2.PdfFileReader(pdf)
                    if reader.isEncrypted:
                        reader.decrypt("")
                    total_pages = reader.getNumPages()

                result = cursor.execute("INSERT INTO BERDI.pdfs(pdfId, totalPages, hearingOrder,\
                application_title_short, short_name, commodity) VALUES (?, ?, ?, ?, ?, ?)",
                (row.pdfId, total_pages, None if pd.isna(row.hearingOrder) else row.hearingOrder,
                row.application_title_short, row.short_name, row.commodity))
                if result.rowcount != 1:
                    return print(f"{row.pdfId}: ERROR! Updated {result.rowcount} rows!")
                print(f"Inserted {result.rowcount} for {row.pdfId}")
            except Exception as e:
                print(f"Error for {row.pdfId}: {e}")
    print("All done")


if __name__ == "__main__":
    insert_pdfs()
