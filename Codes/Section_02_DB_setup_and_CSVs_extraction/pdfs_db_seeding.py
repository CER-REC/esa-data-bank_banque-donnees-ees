from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
import os
import pandas as pd
import PyPDF2

pdf_files_folder = Path("//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/PDF")
# index2 = Path().resolve().parent.parent.joinpath("Input_Files").joinpath(
#     "Index_of_PDFs_for_Major_Projects_with_ESAs.csv")
index2 = Path(r"\\luxor\data\branch\Environmental Baseline Data\Version 4 - Final\Indices\Github_ESA_Final1.csv")

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
elif not index2.exists():
    print(index2, "does not exist!")

pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1200)

load_dotenv(override=True)
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
engine_string = f"mysql+mysqldb://{user}:{password}@{host}/{database}?charset=utf8mb4"
engine = create_engine(engine_string)


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
