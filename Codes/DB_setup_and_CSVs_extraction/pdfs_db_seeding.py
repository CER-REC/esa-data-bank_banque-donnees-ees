from pathlib import Path
from dotenv import load_dotenv
from multiprocessing import Pool
import time
from sqlalchemy import text, create_engine
import os
import pandas as pd
import json
import PyPDF2


pdf_files_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/PDF")
csv_tables_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/all_csvs")
index2 = Path().parent.parent.parent.absolute().joinpath(
    "Input Files").joinpath("Index of PDFs for Major Projects with ESAs.csv")

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
elif not csv_tables_folder.exists():
    print(csv_tables_folder, "does not exist!")
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
    df = df[["Data ID", "Application Name", "Application Short Name", "Commodity", "Hearing order"]] # FIXME:
    df = df.rename(columns={"Data ID": "pdfId", "Commodity": "commodity", "Application Short Name": "short_name",
                            "Hearing order": "hearingOrder", "Application Name": "application_name"})

    with engine.connect() as conn:
        for row in df.itertuples():
            try:
                pdf_path = pdf_files_folder.joinpath(f"{row.pdfId}.pdf")
                with pdf_path.open("rb") as pdf:
                    reader = PyPDF2.PdfFileReader(pdf)
                    if reader.isEncrypted:
                        reader.decrypt("")
                    total_pages = reader.getNumPages()
                
                stmt = text(
                    "INSERT INTO pdfs (pdfId, totalPages, hearingOrder, application_name, application_title_short," +
                    "short_name, commodity) VALUES (:pdfId, :totalPages, :hearingOrder, :application_name," +
                    ":application_title_short, :short_name, :commodity);")
                params = {
                    "pdfId": row.pdfId, "totalPages": total_pages, "hearingOrder": row.hearingOrder,
                    "application_name": row.application_name, "application_title_short": "PLACEHOLDER", # FIXME:
                    "short_name": row.short_name, "commodity": row.commodity}
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    print(f"{row.pdfId}: ERROR! Updated {result.rowcount} rows!")
            except Exception as e:
                print(f"Error for {row.pdfId}: {e}")
    print("All done")

