import pandas as pd
from src.util.database_connection import engine, schema
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def upsert_block(pdf_id, block_data):
    """
        Given a pdf_id, and a dictionary as input. This function attempts to upsert
        the dictionary column values into the block table.

        Parameters
        -------------------
        pdf_id:- a string containing the id of the pdf document
        block_data:- a dictionary containing the following keys each containing a list 
            PdfPageId, OrderNumber, BboxArea, and IsImage

        Returns
        ------------------
        None

    """
    pdf_temp_table_name = get_temp_table_name()

    df_block = pd.DataFrame(block_data)

    with ExceptionHandler(f"Error executing upsert sql statement for PdfId - {pdf_id}"), engine.begin() as db_con:

        # step 1 - insert data frame into a temporary table
        df_block.to_sql(pdf_temp_table_name, schema=schema, con=db_con,
                        index=False, if_exists="replace")

        # step 2 - merge temporary table into Block table
        db_con.exec_driver_sql(
            f"""
                MERGE {schema}.Block AS Target
                USING {schema}.{pdf_temp_table_name} AS Source
                    ON Target.PdfPageId = Source.PdfPageId
                        AND Target.OrderNumber = Source.OrderNumber

                /* insert new block rows */
                WHEN NOT MATCHED BY Target THEN
                    INSERT (PdfPageId, OrderNumber, BboxArea, IsImage)
                    VALUES (Source.PdfPageId, Source.OrderNumber, Source.BboxArea, Source.IsImage)

                /* update existing block rows */
                WHEN MATCHED
                    AND (ISNULL(Target.BboxArea, 0.0) <> ISNULL(Source.BboxArea, 0.0)
                    OR ISNULL(Target.IsImage, 0) <> ISNULL(Source.IsImage, 0)) THEN
                    UPDATE SET 
                    Target.BboxArea = Source.BboxArea,
                    Target.IsImage = Source.IsImage
                ;
            """
        )

        # step 3 - update Pdf table and indicate block data has been extracted successfully
        db_con.exec_driver_sql(f"UPDATE {schema}.Pdf SET BlockExtracted = 1  WHERE PdfId = {pdf_id}")

        # step 4 - finally delete the temporary table
        db_con.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{pdf_temp_table_name}")
