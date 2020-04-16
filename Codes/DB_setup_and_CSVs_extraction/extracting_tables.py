from pathlib import Path
from dotenv import load_dotenv
from multiprocessing import Pool
import time
from sqlalchemy import text, create_engine
import os
import pandas as pd
import json
import json
from external import extract_csv


pdf_files_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/PDF")
# csv_tables_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/all_csvs")
csv_tables_folder = Path(r"C:\Users\T1Ivan\Desktop\1")

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
elif not csv_tables_folder.exists():
    print(csv_tables_folder, "does not exist!")


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


def clear_db():
    with engine.connect() as conn:
        result = conn.execute("DELETE FROM csvs;")
        print(f"Deleted {result.rowcount} csvs from DB")
        result = conn.execute("UPDATE esa.pdfs SET csvsExtracted = NULL WHERE csvsExtracted IS NOT NULL;")
        print(f"Reset {result.rowcount} PDFs from DB (csvsExtracted = NULL)")
    csvs = list(csv_tables_folder.glob("*.csv"))
    for f in csvs:
        f.unlink()
    print(f"Deleted {len(csvs)} CSV files")
    print("Done")


def create_args_for_csv_extraction():
    statement = text("SELECT * FROM esa.pdfs WHERE csvsExtracted IS NULL ORDER BY totalPages DESC;")
    with engine.connect() as conn:
        df = pd.read_sql(statement, conn)
    pdfs = df.to_dict("records")

    files = []
    for pdf in pdfs:
        files.append(
            (pdf["pdfId"],
             int(pdf["totalPages"]),
             engine_string,
             str(pdf_files_folder),
             str(csv_tables_folder)))
    return files


def extract_tables():
    log_file = "log.txt"
    with Path(log_file).open("w") as f:
        pass  # Clearing the log file

    def log_it(s):
        with Path(log_file).open("a", encoding="utf-8-sig") as f:
            f.write(s)
        print(s)

    start_time = time.time()
    files = create_args_for_csv_extraction()[:1]
    time_stamp = time.strftime("%H:%M:%S %Y-%m-%d")
    log_it(f"Items to process: {len(files)} at {time_stamp}\n")

    with Pool() as pool:
        results = pool.map(extract_csv, files, chunksize=1)
    for result in results:
        log_it(result)

    duration = round(time.time() - start_time)
    log_it(f"\nDone {len(files)} items in {duration} seconds ({round(duration/60, 2)} min or {round(duration/3600, 2)} hours)")


if __name__ == "__main__":
    clear_db()  # CAREFUL! DELETES ALL CSV files and CSV DB entries, and resets PDFs (csvsExtracted = NULL)!
    extract_tables()
