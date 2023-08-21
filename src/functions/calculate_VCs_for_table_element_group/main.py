import pandas as pd

from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def calculate_vc_for_table_element_group(table_element_group_id):
    """
    This function receives an TableElementGroupId and returns a dictionary with all the value components as keys and
    the sums of occurrences of the corresponding value component in all the table elements in the group as values
    """
    with ExceptionHandler(f"Error querying VC count for TableElementGroupId - {table_element_group_id}"), \
            engine.begin() as conn:
        df_vc = pd.read_sql_query(f'''  
            SELECT ValueComponent, SUM(ISNULL(FrequencyCount, 0)) AS Count
            FROM {schema}.ValueComponent vc
                LEFT JOIN {schema}.ContentValueComponentMapping m 
                    ON m.ValueComponentId = vc.ValueComponentId 
                LEFT JOIN {schema}.TableElement t 
                    ON t.TableElementId = m.ContentId AND t.TableElementGroupId = {table_element_group_id}
            GROUP BY ValueComponent;
        ''', con=conn)

    return df_vc.set_index('ValueComponent')['Count'].to_dict()
