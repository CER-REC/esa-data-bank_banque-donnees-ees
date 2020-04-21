from pathlib import Path
from dotenv import load_dotenv
from multiprocessing import Pool
import time
from sqlalchemy import text, create_engine
import os
import pandas as pd
import json
from wand.image import Image
from io import StringIO
import sys
from contextlib import redirect_stdout, redirect_stderr
import camelot
from uuid import uuid4
import traceback
import io

pdf_files_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/PDF")
csv_tables_folder = Path(r"C:\Users\T1Ivan\Desktop\3")

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


def extract_csv(args):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        pdf_id, total_pages, engine_string, pdf_files_folder_string, csv_tables_folder_string = args
        pdf_files_folder = Path(pdf_files_folder_string)
        csv_tables_folder = Path(csv_tables_folder_string)
        engine = create_engine(engine_string)
        start_time = time.time()

        def save_tables(tables, page, method):
            for index, table in enumerate(tables):
                table_number = index + 1
                csv_id = f"{pdf_id}_{page}_{method}_{table_number}"
                csv_file_name = f"{csv_id}.csv"
                csv_full_path = str(csv_tables_folder.joinpath(csv_file_name))
                csvRows, csvColumns = table.shape
                accuracy = table.accuracy
                whitespace = table.whitespace
                order = table.order
                top_row_json = json.dumps(table.df.iloc[0].tolist())
                csv_text = table.df.to_json(None, orient='values')
                table.to_csv(csv_full_path, index=False, header=False, encoding="utf-8-sig")

                with engine.connect() as conn:
                    statement = text(
                        "INSERT INTO csvs (csvId, csvFileName, csvFullPath, pdfId, page, tableNumber," +
                        "topRowJson, csvRows, csvColumns, method, accuracy, whitespace, csvText) " +
                        "VALUE (:csvId, :csvFileName, :csvFullPath, :pdfId, :page, :tableNumber, " +
                        ":topRowJson, :csvRows, :csvColumns, :method, :accuracy, :whitespace, :csvText);")
                    result = conn.execute(statement, {"csvId": csv_id, "csvFileName": csv_file_name,
                                                      "csvFullPath": csv_full_path, "pdfId": pdf_id,
                                                      "page": page, "tableNumber": table_number,
                                                      "topRowJson": top_row_json, "csvRows": csvRows,
                                                      "csvColumns": csvColumns, "method": method,
                                                      "accuracy": accuracy, "whitespace": whitespace,
                                                      "csvText": csv_text})

        try:
            pdf_file_path = pdf_files_folder.joinpath(f"{pdf_id}.pdf")

            for page in range(1, total_pages + 1):
                try:
                    tables = camelot.read_pdf(str(pdf_file_path), pages=str(page), strip_text='\n',
                                              line_scale=40, flag_size=True, copy_text=['v'],)
                    save_tables(tables, page, "lattice-v")
                except Exception as e:
                    print(f'Error processing {pdf_id} on page {page}:')
                    print(e)
                    traceback.print_tb(e.__traceback__)

            with engine.connect() as conn:
                statement = text("UPDATE pdfs SET csvsExtracted = :csvsExtracted WHERE pdfId = :pdfId;")
                result = conn.execute(statement, {"csvsExtracted": 'true', "pdfId": pdf_id})
            duration = round(time.time() - start_time)
            print(f"{pdf_id}: done {total_pages} pages in {duration} seconds ({round(duration/60, 2)} min or {round(duration/3600, 2)} hours)")
        except Exception as e:
            print(f'Error processing {pdf_id}:')
            print(e)
            traceback.print_tb(e.__traceback__)
        finally:
            return buf.getvalue()


def clear_db():
    with engine.connect() as conn:
        result = conn.execute("DELETE FROM csvs;")
        print(f"Deleted {result.rowcount} csvs from DB")
        result = conn.execute("UPDATE pdfs SET csvsExtracted = NULL WHERE csvsExtracted IS NOT NULL;")
        print(f"Reset {result.rowcount} PDFs from DB (csvsExtracted = NULL)")
    csvs = list(csv_tables_folder.glob("*.csv"))
    for f in csvs:
        f.unlink()
    print(f"Deleted {len(csvs)} CSV files")
    print("Done")


def create_args_for_csv_extraction():
    statement = text("SELECT * FROM pdfs WHERE csvsExtracted IS NULL ORDER BY totalPages DESC;")
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


def extract_tables(files):
    log_file = "log.txt"
    with Path(log_file).open("w") as f:
        pass  # Clearing the log file

    def log_it(s):
        with Path(log_file).open("a", encoding="utf-8-sig") as f:
            f.write(s)
        print(s, end='', flush=True)

    start_time = time.time()
    time_stamp = time.strftime("%H:%M:%S %Y-%m-%d")
    log_it(f"Items to process: {len(files)} at {time_stamp}\n")

    # Sequential mode - if using, please comment out the multiprocessing mode code  
    # for file in files[-12:]:
    #     result = extract_csv(file)
    #     print(result, end='', flush=True)

    # Multiprocessing mode - if using, please comment out the sequential mode code
    with Pool() as pool:
        results = pool.map(extract_csv, files, chunksize=1)
    for result in results:
        log_it(result)

    duration = round(time.time() - start_time)
    log_it(f"\nDone {len(files)} items in {duration} seconds ({round(duration/60, 2)} min or {round(duration/3600, 2)} hours)")


if __name__ == "__main__":
    clear_db()  # CAREFUL! DELETES ALL CSV files and CSV DB entries, and resets PDFs (csvsExtracted = NULL)!
    inputs = create_args_for_csv_extraction()
    extract_tables(inputs)
