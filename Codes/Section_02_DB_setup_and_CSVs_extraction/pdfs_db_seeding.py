import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from dotenv import load_dotenv
from sqlalchemy import text
import os
import pandas as pd
import PyPDF2

# Load environment variables (from .env file) for the database
engine = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path and Index filepath
pdf_files_folder = Path(os.getenv("PDFS_FILEPATH"))
# index2 = Path().resolve().parent.parent.joinpath("Input_Files").joinpath(
#     "Index_of_PDFs_for_Major_Projects_with_ESAs.csv")
index2 = Path(os.getenv("INDEX2_FILEPATH"))

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
elif not index2.exists():
    print(index2, "does not exist!")

# Increase max size of pandas dataframe output when using a notebook
pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1200)

def insert_pdfs():
    df = pd.read_csv(index2)
    df = df[["Data ID", "Application Name", "Application Short Name", "Commodity", "Hearing order"]]
    df = df.rename(columns={"Data ID": "pdfId", "Commodity": "commodity", "Hearing order": "hearingOrder",
                            "Application Short Name": "short_name", "Application Name": "application_title_short"})

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
                    "INSERT INTO pdfs (pdfId, totalPages, hearingOrder, application_title_short," +
                    "short_name, commodity) VALUES (:pdfId, :totalPages, :hearingOrder," +
                    ":application_title_short, :short_name, :commodity);")
                params = {
                    "pdfId": row.pdfId, "totalPages": total_pages, "hearingOrder": row.hearingOrder,
                    "application_title_short": row.application_title_short,
                    "short_name": row.short_name, "commodity": row.commodity}
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    return print(f"{row.pdfId}: ERROR! Updated {result.rowcount} rows!")
                print(f"Inserted {result.rowcount} for {row.pdfId}")
            except Exception as e:
                print(f"Error for {row.pdfId}: {e}")
    print("All done")


if __name__ == "__main__":
    insert_pdfs()
