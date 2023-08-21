from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def update_table_element_good_quality(pdf_id, df_table):
    """
    This function updates the isGoodQuality column in TableElement
    df_table is a dataframe with the two columns - isGoodQuality and TableElementId
    """
    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error updating TableElement isGoodQuality for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        # step 1 - create a temp data in database
        df_table.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - merge temporary table into TableElement table
        conn.exec_driver_sql(
            f'''
                UPDATE {schema}.TableElement
                SET TableElement.isGoodQuality = tmp.isGoodQuality
                FROM {schema}.{temp_table_name} tmp
                WHERE TableElement.TableElementId = tmp.TableElementId;
                '''
        )

        # step 3 - delete the temp table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
