from wand.image import Image
from sqlalchemy import text, create_engine
from io import StringIO
import sys
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import camelot
from uuid import uuid4
import pandas as pd
import traceback
import io
import json
import time


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
