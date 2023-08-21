import pandas as pd
from src.util.database_connection import engine, schema
from src.util.temp_table import get_temp_table_name
from src.functions.extract_page_metadata.models import PageMetadataColumn, PdfColumn
from src.util.exception_and_logging.handle_exception import ExceptionHandler

def upsert_metadata(pdf_id, meta_data):
    """
        Given a pdf_id, and a dictionary as input. This function attempts to upsert
        the dictionary column values into the block table.

        Parameters
        -------------------
        pdf_id:- a string containing the id of the pdf document
        meta_data:- a dictionary containing the following keys each containing a list 
            PdfPageId, AttributeKey, AttributeValue, and AttributeType

        Returns
        ------------------
        None

    """
    pdf_temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error upserting PageMetadata table for PdfId - {pdf_id}"), engine.begin() as db_con:

        df_meta_data = pd.DataFrame(meta_data)

        # step 1 - insert data frame into a temporary table
        df_meta_data.to_sql(pdf_temp_table_name, schema=schema, con=db_con,
                                index=False, if_exists="replace")

        # step 2 - merge temporary table into PdfPage table
        db_con.exec_driver_sql(
            f"""
                MERGE {schema}.PageMetadata AS Target
                USING {schema}.{pdf_temp_table_name} AS Source
                ON Target.{PageMetadataColumn.PDF_PAGE_ID.value} = Source.{PageMetadataColumn.PDF_PAGE_ID.value}
                AND Target.{PageMetadataColumn.ATTRIBUTE_KEY.value} = Source.{PageMetadataColumn.ATTRIBUTE_KEY.value}

                /* insert new pdf metadata rows */
                WHEN NOT MATCHED BY Target THEN
                    INSERT ({PageMetadataColumn.PDF_PAGE_ID.value}, 
                            {PageMetadataColumn.ATTRIBUTE_KEY.value}, 
                            {PageMetadataColumn.ATTRIBUTE_VALUE.value}, 
                            {PageMetadataColumn.ATTRIBUTE_TYPE.value})
                    VALUES (Source.{PageMetadataColumn.PDF_PAGE_ID.value}, 
                            Source.{PageMetadataColumn.ATTRIBUTE_KEY.value}, 
                            Source.{PageMetadataColumn.ATTRIBUTE_VALUE.value}, 
                            Source.{PageMetadataColumn.ATTRIBUTE_TYPE.value})
                
                /* update existing pdf metadata rows */
                WHEN MATCHED AND (
                    ISNULL(Target.{PageMetadataColumn.ATTRIBUTE_VALUE.value}, '') <> 
                    ISNULL(Source.{PageMetadataColumn.ATTRIBUTE_VALUE.value}, '') OR 
                    ISNULL(Target.{PageMetadataColumn.ATTRIBUTE_TYPE.value}, '') <> 
                    ISNULL(Source.{PageMetadataColumn.ATTRIBUTE_TYPE.value}, '')) THEN
                    UPDATE SET
                    Target.{PageMetadataColumn.ATTRIBUTE_VALUE.value}=
                    Source.{PageMetadataColumn.ATTRIBUTE_VALUE.value},
                    Target.{PageMetadataColumn.ATTRIBUTE_TYPE.value}=
                    Source.{PageMetadataColumn.ATTRIBUTE_TYPE.value};
            """
        )

        # step 3 - update Pdf table and indicate block data has been extracted successfully
        db_con.exec_driver_sql(f""" UPDATE {schema}.Pdf SET {PdfColumn.PAGEMETADATAEXTRACTED.value} = 1
                                WHERE {PdfColumn.PDF_ID.value} = {pdf_id};""")

        # step 5 - finally delete the temporary table
        db_con.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{pdf_temp_table_name}")
