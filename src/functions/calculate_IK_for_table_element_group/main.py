import pandas as pd

from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def calculate_ik_for_table_element_group(table_element_group_id):
    """
    This function receives a TableElementGroupId, and returns True if any table element in this group contains IK, or
    returns False if none of the table elements contains IK
    """
    with ExceptionHandler(f"Error querying IK count for TableElementId - {table_element_group_id}"), \
            engine.begin() as conn:
        df_ik_count = pd.read_sql_query(f'''
            SELECT SUM(CAST(ContainsIK AS INT)) AS IKCount
            FROM {schema}.TableElement te 
                LEFT JOIN {schema}.Content c ON c.ContentId = te.TableElementId
            WHERE TableElementGroupId = {table_element_group_id};
        ''', con=conn)

    with ExceptionHandler(f"IK count is None for TableElementId - {table_element_group_id}"):
        if df_ik_count['IKCount'].iloc[0] is None:
            # If IKCount is null, that means we did not label IK for individual table elements in the group
            raise ValueError(f"IK count is None for TableElementId - {table_element_group_id}")

    return df_ik_count['IKCount'].iloc[0] > 0
