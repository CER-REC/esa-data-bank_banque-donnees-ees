import pandas as pd
from src.util.database_connection import engine, schema
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def upsert_camelot_table(pdf_id, table_data):
    """
        Given a pdf_id, and a dictionary as input. This function attempts to upsert
        the dictionary column values into the CamelotTable table.

        Parameters
        -------------------
        pdf_id:- a string containing the id of the pdf document
        table_data:- a dictionary containing the following keys each containing a list 
            PdfPageId, OrderNumber, NumberofRows, NumberofColumns, WhitespacePercent, HasContent, JsonText

        Returns
        ------------------
        True / False (boolean): based on whether update / insert is successful

    """
    pdf_temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error executing upsert sql statement for PdfId - {pdf_id}"), engine.begin() as db_con:
        # step 1 - insert data frame into a temporary table
        pd.DataFrame(table_data).to_sql(pdf_temp_table_name, schema=schema, con=db_con,
                                        index=False, if_exists="replace")

        # step 2 - merge temporary table into CamelotTable table
        db_con.exec_driver_sql(
            f"""
                MERGE {schema}.CamelotTable AS Target
                USING {schema}.{pdf_temp_table_name} AS Source
                ON Target.PdfPageId = Source.PdfPageId
                AND Target.OrderNumber = Source.OrderNumber

                /* insert new camelot table rows */
                WHEN NOT MATCHED BY Target THEN
                    INSERT (PdfPageId, OrderNumber, NumberOfRows, NumberOfColumns, WhitespacePercent, HasContent, 
                            JsonText)
                    VALUES (Source.PdfPageId, Source.OrderNumber, Source.NumberOfRows, Source.NumberOfColumns, 
                            Source.WhitespacePercent, Source.HasContent, Source.JsonText)

                /* update existing camelot table rows */
                WHEN MATCHED 
                    AND (ISNULL(Target.NumberOfRows, 0) <> ISNULL(Source.NumberOfRows, 0)
                    OR ISNULL(Target.NumberOfColumns, 0) <> ISNULL(Source.NumberOfColumns, 0)
                    OR ISNULL(Target.WhitespacePercent, 0) <> ISNULL(Source.WhitespacePercent, 0)
                    OR ISNULL(Target.HasContent, 0) <> ISNULL(Source.HasContent, 0)
                    OR ISNULL(Target.JsonText, '') <> ISNULL(Source.JsonText, '')) THEN
                    UPDATE SET 
                    Target.NumberOfRows = Source.NumberOfRows,
                    Target.NumberOfColumns = Source.NumberOfColumns,
                    Target.WhitespacePercent = Source.WhitespacePercent,
                    Target.HasContent = Source.HasContent,
                    Target.JsonText = Source.JsonText;
            """
        )

        # step 3 - update Pdf table and indicate block data has been extracted successfully
        db_con.exec_driver_sql(f"UPDATE {schema}.Pdf SET CamelotTableExtracted = 1  WHERE PdfId = {pdf_id}")

        # step 4 - finally delete the temporary table
        db_con.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{pdf_temp_table_name}")
