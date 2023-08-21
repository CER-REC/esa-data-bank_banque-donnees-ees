import pandas as pd
from src.util.database_connection import engine, schema
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import TMP_TABLE_PREFIX


def delete_temp_tables():
    """
    This function drops all the temporary tables in the database
    """
    with ExceptionHandler("Error deleting temp tables"), engine.begin() as conn:
        df_tables = pd.read_sql(f"""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA='{schema}' AND TABLE_NAME LIKE '{TMP_TABLE_PREFIX}%'
        """, conn)

        for _, row in df_tables.iterrows():
            conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{row['TABLE_NAME']}")
