import pandas as pd

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.database_connection import engine, schema


def group_table_elements(pdf_id):
    """
    This function is to find table element groups - groups of table elements that have the same title and appear on
    consecutive pdf pages, and create new table element rows and update the TableElementGroupId values in TableElement
    table accordingly.
    """
    with ExceptionHandler(f"Error querying table elements and their groups for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        df_table_elements = pd.read_sql(f"""  
            WITH TableElementCTE AS (
                /* retrieve table elements and numbers representing groups of consecutive pdf pages */
                SELECT te.TableElementId
                    , te.FileName
                    , c.Title
                    , pp.PageNumber
	                , ca.OrderNumber
                    , pp.PageNumber - DENSE_RANK() OVER (ORDER BY pp.PageNumber) AS ConsecutivePageGroup
                FROM {schema}.TableElement te
                    INNER JOIN {schema}.Content c 
                        ON c.ContentId = te.TableElementId AND c.Title IS NOT NULL
                    INNER JOIN {schema}.CamelotTable ca 
                        ON ca.CamelotTableId = te.CamelotTableId
                    INNER JOIN {schema}.PdfPage pp 
                        ON te.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            )
            
            /* retrieve table elements and numbers representing table element groups */
            SELECT TableElementId
                , FileName
                , PageNumber
                , OrderNumber
                , DENSE_RANK() OVER (ORDER BY Title, ConsecutivePageGroup) AS TableElementGroupNumber
            FROM TableElementCTE
            ;
        """, con=conn)

    for id_group in df_table_elements["TableElementGroupNumber"].unique():
        # iterate through each table element group
        # get a list of table element ids that belong to the same group
        table_element_id_list = df_table_elements.loc[df_table_elements["TableElementGroupNumber"] == id_group,
                                                      "TableElementId"].tolist()
        # use the file name of the first table element in the group as the zip folder name for the group
        zip_folder_name = df_table_elements[df_table_elements["TableElementGroupNumber"] == id_group] \
            .sort_values(["PageNumber", "OrderNumber"])["FileName"].iloc[0]

        with ExceptionHandler(f"Error creating and updating a table element group for TableElementIds - "
                              f"{table_element_id_list}"), engine.begin() as conn:
            # the condition will be like "TableElementId IN (1,2,3)" if there are multiple table element ids,
            # if not the condition will be like "TableElementId = 1"
            table_element_id_condition = f"TableElementId IN {tuple(table_element_id_list)}" \
                if len(table_element_id_list) > 1 else f"TableElementId = {table_element_id_list[0]}"
            # compose zip folder name for sql statement
            zip_folder_name = f"'{zip_folder_name}'" if zip_folder_name else "NULL"

            conn.exec_driver_sql(f"""       
                /* delete old TableElementGroup rows */
                DELETE teg  
                FROM {schema}.TableElementGroup teg
                    INNER JOIN {schema}.TableElement te 
                        ON teg.TableElementGroupId = te.TableElementGroupId AND {table_element_id_condition};
                 
                /* insert into TableElementGroup rows */ 
                INSERT INTO {schema}.TableElementGroup(ZipFolderName)
                VALUES ({zip_folder_name});
                
                /* update TableElementGroupId with the new id value */
                UPDATE {schema}.TableElement
                SET TableElementGroupId = SCOPE_IDENTITY()
                WHERE {table_element_id_condition};
            """)
