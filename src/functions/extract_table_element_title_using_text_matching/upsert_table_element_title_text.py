from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def upsert_table_element_title_text(pdf_id, df_table):
    """
        update / insert the 'TitleText' column of the 'TableElement' table
        based on pdf_id and 'TableElement' as a DataFrame object

        Params:
        ------------------------------
        pdf_id (integer): id of the pdf document
        df_table (DataFrame): dataframe object with only two columns
            as follows: 'TableElementId' and 'TitleText'

        Returns:
        ------------------------------
    """
    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error executing upsert TableElement TitleText for PdfId - {pdf_id}"), \
        engine.begin() as conn:

        # step 1 - create a temp data in database
        df_table.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - merge temporary table into TableElement table
        conn.exec_driver_sql(
            f'''
            MERGE {schema}.TableElement AS Target
            USING {schema}.{temp_table_name} AS Source
            ON Target.TableElementId = Source.TableElementId

            /* update existing pdf page raw text */
            WHEN MATCHED THEN
                UPDATE SET 
                Target.TitleText = Source.TitleText
            ;
            '''
        )

        # step 3 - delete the temp table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
