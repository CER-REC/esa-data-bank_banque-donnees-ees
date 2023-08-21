import pandas as pd

from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.pdf_page.pdf_page import PdfPageTextColumn
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def _update_pdf_text_extracted_col(pdf_id, text_col, conn):
    """
    Update PageTextExtracted to 1 in Pdf table if raw text has been extracted;
    update RotatedPageTextExtracted to 1 in Pdf table if rotated text has been extracted
    """
    if text_col == PdfPageTextColumn.RAW_TEXT.value:
        conn.exec_driver_sql(f"UPDATE {schema}.Pdf SET PageTextExtracted = 1  WHERE PdfId = {pdf_id};")
    elif text_col == PdfPageTextColumn.RAW_ROTATED90_TEXT.value:
        conn.exec_driver_sql(f"UPDATE {schema}.Pdf SET RotatedPageTextExtracted = 1  WHERE PdfId = {pdf_id};")


def upsert_pdf_page_text(pdf_id, page_text_dict, text_col):
    """
    Given pdf id, a dictionary with keys as page numbers and values as page text, and the text column name in the
    PdfPage table, the rows corresponding to the pdf_id and page numbers will be inserted or updated.
    """
    with ExceptionHandler(f"Error upserting PdfPage text column: empty data for PdfId - {pdf_id}"):
        if not page_text_dict:
            raise ValueError(f"Error upserting PdfPage text column: empty data for PdfId - {pdf_id}")

    page_data = {
        text_col: list(page_text_dict.values()),
        "PdfId": [pdf_id] * len(page_text_dict),
        "PageNumber": list(page_text_dict.keys())
    }
    temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error upserting PdfPage text column - {text_col}"), engine.begin() as conn:
        # step - 1 - create a temp data in database with the page text data
        pd.DataFrame(page_data).to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - merge temporary table into PdfPage table
        conn.exec_driver_sql(
            f'''
            MERGE {schema}.PdfPage AS Target
            USING {schema}.{temp_table_name} AS Source
            ON Target.PdfId = Source.PdfId AND Target.PageNumber = Source.PageNumber

            /* insert new pdf page rows */
            WHEN NOT MATCHED BY Target THEN
                INSERT (PdfId, PageNumber, {text_col})
                VALUES (Source.PdfId, Source.PageNumber, Source.{text_col})

            /* update existing pdf page raw text */
            WHEN MATCHED
                AND ISNULL(Target.{text_col}, '') <> ISNULL(Source.{text_col}, '') THEN
                UPDATE SET 
                Target.{text_col} = Source.{text_col}
                
            /* delete */
            WHEN NOT MATCHED BY Source 
                AND Target.PdfId = {pdf_id} THEN
                DELETE
            ;
            '''
        )

        # step 3 - update Pdf table and indicate text or rotated text has been extracted successfully
        _update_pdf_text_extracted_col(pdf_id, text_col, conn)

        # step 4 - delete the temp table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
