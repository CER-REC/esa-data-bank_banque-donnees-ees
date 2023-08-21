from math import trunc
import json
from pathlib import Path
from collections import defaultdict
import re
import camelot
import pandas as pd
import PyPDF2
from src.util.database_connection import engine, schema
from src.util.file_location import get_pdf_file_location
from src.functions.extract_camelot_table.upsert_camelot_table import upsert_camelot_table
from src.util.exception_and_logging.handle_exception import ExceptionHandler

def is_not_empty(lines):
    """
    This function checks if the csv text extracted as JSON 
    string is empty or not
    Args:
        lines (array of array of strings): csv text
        Example: [["Linear Features Density Class ","Baseline Case","Future Case"],
        ["Linear Features Density Class ","Amount of Habitat Available",
        "Change from Baseline to Project Case",]]

    """
    regex = re.compile("[0-9a-zA-Z]")
    for line in lines:
        for cell in line:
            if regex.search(cell):
                return True
    return False

def extract_camelot_table(pdf_id):
    """
    This function extracts the tables from the pdf files and upsert 
    the extracted tables in CamelotTable table
    Args:
        pdf_id (integer): pdf id number

    """
    # absolute file path (network shared directory) of the pdf document
    pdf_file_path = get_pdf_file_location(pdf_id)

    # mapping between PdfPageId and PageNumber
    # need this information to extract PdfPageId from PageNumber for a given pdf with a PdfId
    query = f"SELECT PdfPageId, PageNumber FROM {schema}.PdfPage WHERE PdfId = {pdf_id}"
    with ExceptionHandler(f"Error executing select sql statement for PdfId - {pdf_id}"), engine.begin() as conn:
        df_page_info = pd.read_sql(query, con=conn, index_col=["PageNumber"])

    camelot_table_data = defaultdict(list)
    
    with Path(pdf_file_path).open('rb') as pdf, ExceptionHandler("Error reading pdf using PyPDF2"):
        reader = PyPDF2.PdfReader(pdf)
        if reader.is_encrypted:
            reader.decrypt("")
        for page_num in range(len(reader.pages)):
            with ExceptionHandler(f"Handle missing page numbers for PdfId - {pdf_id}"):
                if (page_num+1) not in df_page_info.index:
                    raise ValueError(f"Missing page number in PdfPage for PdfId = {pdf_id}")
            
            # get PdfPageId from PageNumber
            page_id = df_page_info.loc[page_num+1, "PdfPageId"]
            tables = camelot.read_pdf(
                    pdf_file_path,
                    pages=str(page_num+1),
                    strip_text="\n",
                    line_scale=40,
                    flag_size=True,
                    copy_text=["v"],
            )
            for index, table in enumerate(tables):
                table_number = index + 1
                number_of_rows, number_of_columns = table.shape
                whitespace = trunc(table.whitespace)
                csv_text = table.df.to_json(None, orient='values')
                has_content = is_not_empty(json.dumps(csv_text))
                camelot_table_data["PdfPageId"].append(page_id)
                camelot_table_data["OrderNumber"].append(table_number)
                camelot_table_data["NumberOfRows"].append(number_of_rows)
                camelot_table_data["NumberOfColumns"].append(number_of_columns)
                camelot_table_data["WhitespacePercent"].append(whitespace)
                camelot_table_data["HasContent"].append(has_content)
                camelot_table_data["JsonText"].append(csv_text)

    # upsert the CamelotTable table
    upsert_camelot_table(pdf_id, camelot_table_data)
