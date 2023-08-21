import pandas as pd
from src.util.database_connection import engine, schema
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def upsert_vcmapping_table(pdf_id, vcs_data):
    """
        Given a pdf_id, and a dictionary as input. This function attempts to upsert
        the dictionary column values into the ContentValueComponentMapping table.

        Parameters
        -------------------
        pdf_id:- a string containing the id of the pdf document
        vcs_data:- a dictionary containing the following keys each containing a list
            ContentId, ValueComponentId, FrequencyCount

        Returns
        ------------------
        None

    """
    if not vcs_data:
        return
    
    temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error deleting and inserting ContentValueComponentMapping for PdfId - {pdf_id}"), \
            engine.begin() as db_con:
        # step 1 - delete existing ContentValueComponentMapping values of the pdf
        db_con.exec_driver_sql(f"""
            DELETE m
            FROM {schema}.ContentValueComponentMapping m 
                INNER JOIN {schema}.Content c ON m.ContentId = c.ContentId
                INNER JOIN {schema}.PdfPage pp ON c.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id};
        """)

        # step 2 - insert data frame into a temporary table
        pd.DataFrame(vcs_data).to_sql(temp_table_name, schema=schema, con=db_con, index=False, if_exists="replace")

        # step 3 - insert into ContentValueComponentMapping from the temp table
        db_con.exec_driver_sql(
            f"""
                INSERT INTO {schema}.ContentValueComponentMapping (ContentId, ValueComponentId, FrequencyCount)
                SELECT ContentId, ValueComponentId, FrequencyCount
                FROM {schema}.{temp_table_name};
            """
        )

        # step 4 - finally delete the temporary table
        db_con.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
