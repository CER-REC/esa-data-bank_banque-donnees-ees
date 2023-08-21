from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def update_alignment_sheet_title(pdf_id, df_alignment_sheet):
    """
    This function updates the Title column in AlignmentSheet table based on the dataframe df_alignment_sheet
    The dataframe contains AlignmentSheetId and Title columns
    """
    if not df_alignment_sheet.shape[0]:
        return
    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error executing update AlignmentSheet Title for PdfId - {pdf_id}"), engine.begin() as conn:
        # step 1 - create a temp data in database
        df_alignment_sheet.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - update Title in AlignmentSheet table
        conn.exec_driver_sql(
            f'''
            UPDATE {schema}.AlignmentSheet
            SET AlignmentSheet.Title = CAST({schema}.{temp_table_name}.Title AS VARCHAR(1000))
            FROM {schema}.{temp_table_name}
            WHERE AlignmentSheet.AlignmentSheetId = {schema}.{temp_table_name}.AlignmentSheetId;
            '''
        )

        # step 3 - delete the temp table
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")


def update_content_title_from_alignment_sheet(pdf_id):
    """
    This functions updates the Title column in Content table based on the Title values from AlignmentSheet table
    """
    with ExceptionHandler(f"Error updating Content Title from AlignmentSheet Title for PdfId - {pdf_id}"),\
            engine.begin() as conn:
        conn.exec_driver_sql(f'''
            UPDATE {schema}.Content
            SET Content.Title = tmp.Title
            FROM (
                SELECT AlignmentSheetId, Title
                FROM {schema}.AlignmentSheet a
                    INNER JOIN {schema}.PdfPage pp ON a.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
                ) tmp
            WHERE Content.ContentId = tmp.AlignmentSheetId;
        ''')
