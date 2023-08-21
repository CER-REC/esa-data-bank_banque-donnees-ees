from src.util.content.content_type import ContentType
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def delete_content(pdf_id, df_content, content_type):
    """
    This functions receives a pdf_id, a dataframe and content_type, and deletes unmatched rows from Content table and
    TableElement or Figure table.
    If content_type is TableElement, dataframe has to contain CamelotTableId and PdfPageId columns
    If content_type is Figure, dataframe has to contain BlockId and PdfPageId columns
    """
    with ExceptionHandler("Unrecognized content_type for delete_unmatched_content function"):
        if content_type not in (type.value for type in ContentType):
            raise ValueError(f"Unrecognized content_type for delete_unmatched_content function: {content_type}")

    if content_type == ContentType.TABLE_ELEMENT.value:
        child_table_name = "TableElement"
        child_table_identifier_col = "TableElementId"
        child_table_secondary_col = "CamelotTableId"
    else:
        child_table_name = "Figure"
        child_table_identifier_col = "FigureId"
        child_table_secondary_col = "BlockId"

    with ExceptionHandler("Missing column in the input dataframe for delete_unmatched_content function"):
        if child_table_secondary_col not in df_content.columns:
            raise ValueError(f"Missing column in the input dataframe for delete_unmatched_content function: "
                             f"{child_table_secondary_col}")

    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error deleting Content/TableElement rows for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        df_content.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")
        conn.exec_driver_sql(f"""
                DELETE c
                FROM {schema}.Content c
                    INNER JOIN {schema}.PdfPage pp 
                        ON pp.PdfPageId = c.PdfPageId AND pp.PdfId = {pdf_id}
                WHERE c.Type = '{content_type}'
                    AND NOT EXISTS (
                        SELECT 1
                        FROM {schema}.{child_table_name} t
                            INNER JOIN {schema}.{temp_table_name} tmp 
                                ON t.{child_table_secondary_col} = tmp.{child_table_secondary_col} 
                                    AND t.PdfPageId = tmp.PdfPageId
                        WHERE c.ContentId = t.{child_table_identifier_col});
                """)
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
