from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def update_content_title(pdf_id, df_table):
    """
    This function updates the Title column in Content table using the data given in df_table.
    df_table has two columns ContentId and Title
    """
    temp_table_name = get_temp_table_name()

    with ExceptionHandler(f"Error updating Title in Content table for PdfId - {pdf_id}"), engine.begin() as conn:
        # step 1 - create a temp data in database
        df_table.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - update Title column in Content table
        conn.exec_driver_sql(f"""
            UPDATE {schema}.Content 
            SET Content.Title = tmp.Title
            FROM {schema}.{temp_table_name} tmp
            WHERE Content.ContentId = tmp.ContentId;
        """)

        # step 3 - delete the temp table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
