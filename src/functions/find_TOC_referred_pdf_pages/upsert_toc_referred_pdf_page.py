import pandas as pd

from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def upsert_toc_referred_pdf_page(toc_id, pdf_page_id_list):
    """ Given the TOC id and a list of PdfPageIds, we upsert the TOCReferredPdfPage table in the database """
    tmp_table_name = get_temp_table_name()
    tmp_data = {
        "TOCId": [toc_id] * len(pdf_page_id_list),
        "PdfPageId": pdf_page_id_list
    }
    with ExceptionHandler("Error upserting TOCReferredPdfPage"), engine.begin() as conn:
        pd.DataFrame(tmp_data).to_sql(tmp_table_name, schema=schema, con=conn, index=False,
                                      if_exists="replace")

        conn.exec_driver_sql(f'''
            MERGE {schema}.TOCReferredPdfPage AS Target
            USING {schema}.{tmp_table_name} AS Source
            ON Target.TOCId = Source.TOCId AND Target.PdfPageId = Source.PdfPageId
    
            WHEN NOT MATCHED BY Target THEN
                INSERT (TOCId, PdfPageId)
                VALUES (Source.TOCId, Source.PdfPageId)
    
            WHEN NOT MATCHED BY Source 
                AND Target.TOCId = {toc_id} THEN
                DELETE
            ;
            ''')

        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{tmp_table_name}")
