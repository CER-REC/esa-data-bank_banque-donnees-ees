import pandas as pd

from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def upsert_tocs(pdf_id, toc_dict):
    """
        This function upsert TOC table given the PdfId and a dict of the following structure:
        { "PdfPageId": [], "OrderNumber": [], "ContentType": [], "ContentTitle": [] }
        The lists are of the same length.
    """
    temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error upserting TOCs for PdfId - {pdf_id}"), engine.begin() as conn:
        # step 1 - create a temp table of the TOC items
        pd.DataFrame(toc_dict).to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - merge temporary table into TOC table
        conn.exec_driver_sql(
            f'''
                MERGE {schema}.TOC AS Target
                USING {schema}.{temp_table_name} AS Source
                ON Target.PdfPageId = Source.PdfPageId AND Target.OrderNumber = Source.OrderNumber

                /* insert new pdf page rows */
                WHEN NOT MATCHED BY Target THEN
                    INSERT (PdfPageId, OrderNumber, ContentType, ContentTitle)
                    VALUES (Source.PdfPageId, Source.OrderNumber, Source.ContentType, Source.ContentTitle)

                /* update existing pdf page raw text */
                WHEN MATCHED 
                    AND (ISNULL(Target.ContentType, '') <> ISNULL(Source.ContentType, '') 
                    OR ISNULL(Target.ContentTitle, '') <> ISNULL(Source.ContentTitle, '')) THEN
                    UPDATE SET 
                    Target.ContentType = Source.ContentType
                    , Target.ContentTitle = Source.ContentTitle
                ;
                '''
        )

        # step 3 - update Pdf table to indicate TOCs are extracted for the pdf file
        conn.exec_driver_sql(f"UPDATE {schema}.Pdf SET TOCItemExtracted = 1 WHERE PDFId = {pdf_id};")

        # step 4 - delete the temporary table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
