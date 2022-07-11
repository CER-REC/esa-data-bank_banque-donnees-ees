import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from berdi.Database_Connection_Files.connect_to_sqlserver_database import connect_to_db
from multiprocessing import Pool
import time
from sqlalchemy import text
import pandas as pd
import json
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import camelot
import traceback
import re
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).parents[2].resolve()
print(REPO_ROOT)
RAW_DATA = "data/raw"
PROCESSED_DATA = "data/processed"

# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=REPO_ROOT / "berdi/Database_Connection_Files" / ".env", override=True
)
conn = connect_to_db()


pdf_files_folder = REPO_ROOT / RAW_DATA / "pdfs"
csv_tables_folder = REPO_ROOT / PROCESSED_DATA / "csvs" / "new_projects"

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

                with conn:
                    cursor = conn.cursor()
                    statement2 = "INSERT INTO [DS_TEST].BERDI.csvs(csvId, csvFileName, csvFullPath, pdfId, page, tableNumber, topRowJson, csvRows, csvColumns, method, accuracy, whitespace, csvText, hasContent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    params = (
                        csv_id,
                        csv_file_name,
                        csv_full_path,
                        pdf_id,
                        csv_page,
                        table_number,
                        top_row_json,
                        csv_rows,
                        csv_columns,
                        method,
                        accuracy,
                        whitespace,
                        csv_text,
                        has_content,
                    )
                    cursor.execute(statement2, params)

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
            with conn:
                cursor = conn.cursor()
                statement = "UPDATE [DS_TEST].BERDI.pdfs SET csvsExtracted = ? WHERE pdfId = ?"
                cursor.execute(statement, ("true", pdf_id))
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
    with conn:
        cursor = conn.cursor()
        result = cursor.execute("DELETE FROM csvs;")
        print(f"Deleted {result.rowcount} csvs from DB")
        result = cursor.execute(
            "UPDATE pdfs SET csvsExtracted = NULL WHERE csvsExtracted IS NOT NULL;"
        )
        print(f"Reset {result.rowcount} PDFs from DB (csvsExtracted = NULL)")
    csvs = list(csv_tables_folder.glob("*.csv"))
    for f in csvs:
        f.unlink()
    print(f"Deleted {len(csvs)} CSV files")
    print("Done")


def extract_tables(multi_process=False):
    # statement = text(
    #     "SELECT * FROM [DS_TEST].BERDI.pdfs WHERE csvsExtracted IS NULL ORDER BY totalPages DESC"
    # )
    with conn:
        #cursor = conn.cursor()
        df = pd.read_sql("SELECT * FROM [DS_TEST].BERDI.pdfs WHERE csvsExtracted IS NULL ORDER BY totalPages DESC;", conn)
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

    if multi_process == False:
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
    # CAREFUL! THE PART BELOW DELETES ALL CSV files and CSV DB entries, and resets PDFs (csvsExtracted = NULL)!
    # # Only make clear_database = True, if you want to remove all data from the database.
    # # Making this part verbose and commenting it to prevent accidental deletion of data.
    # clear_database = False
    # if clear_database == True:
    #     clear_db()

    extract_tables()
