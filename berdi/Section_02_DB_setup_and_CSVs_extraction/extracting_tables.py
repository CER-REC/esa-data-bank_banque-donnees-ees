import sys
from pathlib import Path
from berdi.Database_Connection_Files.connect_to_database import connect_to_db
from multiprocessing import Pool
import time
from sqlalchemy import text
import os
import pandas as pd
import json
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import camelot
import traceback
import re

sys.path.append(str(Path(__file__).parent.parent.absolute()))

# Caution! Removes all data!
# Only make clear_database = True, if you want to remove all data from the database.
clear_database = False

# Load environment variables (from .env file) for the database
engine = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path and Index filepath
pdf_files_folder = Path(os.getenv("PDFS_FILEPATH"))
# csv_tables_folder = Path().resolve().parent.parent.joinpath("Data_Files").joinpath("CSVs")
csv_tables_folder = Path(os.getenv("CSV_TABLES_FOLDER_PATH"))

if not pdf_files_folder.exists():
    print(pdf_files_folder, "does not exist!")
elif not csv_tables_folder.exists():
    print(csv_tables_folder, "does not exist!")


def is_empty(lines):
    regex = re.compile("[0-9a-zA-Z]")
    for line in lines:
        for cell in line:
            if regex.search(cell):
                return False
    return True


def extract_csv(args):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        pdf_id, total_pages, pdf_files_folder_string, csv_tables_folder_string = args
        pdf_files_folder2 = Path(pdf_files_folder_string)
        csv_tables_folder2 = Path(csv_tables_folder_string)
        start_time = time.time()

        def save_tables(csv_tables, csv_page, method):
            for index, table in enumerate(csv_tables):
                table_number = index + 1
                csv_id = f"{pdf_id}_{csv_page}_{method}_{table_number}"
                csv_file_name = f"{csv_id}.csv"
                csv_full_path = str(csv_tables_folder2.joinpath(csv_file_name))
                csv_rows, csv_columns = table.shape
                accuracy = table.accuracy
                whitespace = table.whitespace
                top_row_json = json.dumps(table.df.iloc[0].tolist())
                csv_text = table.df.to_json(None, orient="values")
                table.to_csv(
                    csv_full_path, index=False, header=False, encoding="utf-8-sig"
                )
                has_content = 0 if is_empty(json.dumps(csv_text)) else 1

                with engine.connect() as conn2:
                    statement2 = text(
                        "INSERT INTO csvs (csvId, csvFileName, csvFullPath, pdfId, page, tableNumber,"
                        + "topRowJson, csvRows, csvColumns, method, accuracy, whitespace, csvText, hasContent) "
                        + "VALUE (:csvId, :csvFileName, :csvFullPath, :pdfId, :page, :tableNumber, "
                        + ":topRowJson, :csvRows, :csvColumns, :method, :accuracy, :whitespace, :csvText, :hasContent);"
                    )
                    conn2.execute(
                        statement2,
                        {
                            "csvId": csv_id,
                            "csvFileName": csv_file_name,
                            "csvFullPath": csv_full_path,
                            "pdfId": pdf_id,
                            "page": csv_page,
                            "tableNumber": table_number,
                            "topRowJson": top_row_json,
                            "csvRows": csv_rows,
                            "csvColumns": csv_columns,
                            "method": method,
                            "accuracy": accuracy,
                            "whitespace": whitespace,
                            "csvText": csv_text,
                            "hasContent": has_content,
                        },
                    )

        try:
            pdf_file_path = pdf_files_folder2.joinpath(f"{pdf_id}.pdf")

            # Running Camelot to extract tables on each individual page at a time
            for page in range(1, total_pages + 1):
                try:
                    # Running Camelot to extract tables from PDFs
                    # May need to modify parameters for your specific use-case
                    # More info here: https://camelot-py.readthedocs.io/en/master/
                    # And here for Advanced Usage: https://camelot-py.readthedocs.io/en/master/user/advanced.html
                    tables = camelot.read_pdf(
                        str(pdf_file_path),
                        pages=str(page),
                        strip_text="\n",
                        line_scale=40,
                        flag_size=True,
                        copy_text=["v"],
                    )
                    save_tables(tables, page, "lattice-v")
                except Exception as e:
                    print(f"Error processing {pdf_id} on page {page}:")
                    print(e)
                    traceback.print_tb(e.__traceback__)

            # Add extracted table to the database
            with engine.connect() as conn:
                statement = text(
                    "UPDATE pdfs SET csvsExtracted = :csvsExtracted WHERE pdfId = :pdfId;"
                )
                conn.execute(statement, {"csvsExtracted": "true", "pdfId": pdf_id})
            duration = round(time.time() - start_time)
            mins = round(duration / 60, 2)
            hrs = round(duration / 3600, 2)
            print(
                f"{pdf_id}: done {total_pages} pages in {duration} seconds ({mins} min or {hrs} hours)"
            )
        except Exception as e:
            print(f"Error processing {pdf_id}:")
            print(e)
            traceback.print_tb(e.__traceback__)
        finally:
            return buf.getvalue()


# CAREFUL! DELETES ALL CSV files and CSV DB entries, and resets PDFs (csvsExtracted = NULL)!
def clear_db():
    with engine.connect() as conn:
        result = conn.execute("DELETE FROM csvs;")
        print(f"Deleted {result.rowcount} csvs from DB")
        result = conn.execute(
            "UPDATE pdfs SET csvsExtracted = NULL WHERE csvsExtracted IS NOT NULL;"
        )
        print(f"Reset {result.rowcount} PDFs from DB (csvsExtracted = NULL)")
    csvs = list(csv_tables_folder.glob("*.csv"))
    for f in csvs:
        f.unlink()
    print(f"Deleted {len(csvs)} CSV files")
    print("Done")


if clear_database == True:
    clear_db()


def extract_tables(multiprocessing=False):
    statement = text(
        "SELECT * FROM pdfs WHERE csvsExtracted IS NULL ORDER BY totalPages DESC;"
    )
    with engine.connect() as conn:
        df = pd.read_sql(statement, conn)
    pdfs = df.to_dict("records")

    files = []
    for pdf in pdfs:
        files.append(
            (
                pdf["pdfId"],
                int(pdf["totalPages"]),
                str(pdf_files_folder),
                str(csv_tables_folder),
            )
        )

    start_time = time.time()
    time_stamp = time.strftime("%H:%M:%S %Y-%m-%d")
    print(f"Items to process: {len(files)} at {time_stamp}\n")

    if multiprocessing == False:
        # Sequential mode
        for file in files[:]:
            result = extract_csv(file)
            print(result, end="", flush=True)
    else:
        # Multiprocessing mode
        with Pool() as pool:
            results = pool.map(extract_csv, files, chunksize=1)
        for result in results:
            print(result, end="", flush=True)

    duration = round(time.time() - start_time)
    mins = round(duration / 60, 2)
    secs = round(duration / 3600, 2)
    print(
        f"\nDone {len(files)} items in {duration} seconds ({mins} min or {secs} hours)"
    )


if __name__ == "__main__":
    extract_tables(multiprocessing=False)
