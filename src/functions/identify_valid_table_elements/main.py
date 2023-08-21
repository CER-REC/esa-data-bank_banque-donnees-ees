import pandas as pd
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.content.content_type import ContentType


def identify_valid_table_elements(pdf_id):
    """
        This function checks if the tables in CamelotTable are valid
        using a stored procedure insert TableElementId, CamelotTableId, PdfPageId into TableElement table
        and update PdfPageId, Type values in Content table
        ------
        Input:
        ------
        pdf_id integer value
        ------
        Return:
        ------
    """
    with ExceptionHandler(f"Error removing existing table elements for PdfId - {pdf_id}"), engine.begin() as conn:
        # Delete content will result in also deleting the Table Elements because of a delete cascade
        delete_stmt = f"""
            DELETE c
            FROM {schema}.Content c
                INNER JOIN {schema}.PdfPage pp 
                    ON c.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            WHERE Type = '{ContentType.TABLE_ELEMENT.value}';
        """
        conn.exec_driver_sql(delete_stmt)

    with ExceptionHandler(f"Error querying CamelotTable of PdfId - {pdf_id}"), engine.begin() as conn:
        # capture rows with valid extracted tables
        stmt = f'''SELECT ct.CamelotTableId, ct.PdfPageId, pg.PdfId  
                    FROM {schema}.CamelotTable ct
                        INNER JOIN {schema}.PdfPage pg
                            ON ct.PdfPageId = pg.PdfPageId AND pg.PdfId = {pdf_id}
                    WHERE HasContent = 1 AND NumberOfColumns > 1 AND WhitespacePercent < 78;'''
        df_camelot_tables = pd.read_sql_query(stmt, conn)

    # iterate over output of processed CamelotTable output(df_camelot_tables)
    # use "CamelotTableId", "PdfPageId" of each row as parameters
    # of the stored procedure
    stored_proc = f'''Exec {schema}.PR_Load_TableElement @intCamelotTableId = ?, @intPdfPageId = ?;'''
    with ExceptionHandler(f"Error loading TableElements of PdfId - {pdf_id}"), engine.begin() as conn:
        for _, row in df_camelot_tables.iterrows():
            params = (int(row["CamelotTableId"]), int(row["PdfPageId"]))
            conn.exec_driver_sql(stored_proc, params)
