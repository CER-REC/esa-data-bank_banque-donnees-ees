import pandas as pd

from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.exception_and_logging.process_logs import berdi_logger
from src.util.content.delete_unmatched_content import ContentType


def _find_pdf_pages_with_figures(pdf_id):
    """
    This function receives a pdf_id and returns a list of pdf_page_id where figures might exist
    """
    with ExceptionHandler(f"Error querying PdfPage of Block for PdfId - {pdf_id}"), engine.begin() as conn:
        # Get the PdfPageIds and the TotalBboxArea, ImageCount, and TotalImageBboxArea for each pdf page
        df_pdf_pages = pd.read_sql_query(f'''
            SELECT b.PdfPageId
                , SUM(BboxArea) AS TotalBboxArea
                , SUM(CAST(IsImage AS int)) AS ImageCount
                , SUM(CASE WHEN IsImage = 1 THEN BboxArea ELSE 0 END) AS TotalImageBboxArea 
            FROM {schema}.Block b
                INNER JOIN {schema}.PdfPage pg
                    ON b.PdfPageId = pg.PdfPageId AND pg.PdfId = {pdf_id}
            GROUP BY b.PdfPageId;
            ''', con=conn)

    # calculate the thresholds in terms of image proportion and image count per pdf page
    df_pdf_pages['ImageAreaProportion'] = df_pdf_pages.apply(lambda x: x["TotalImageBboxArea"]/x["TotalBboxArea"]
                                                             if x["TotalBboxArea"] else 0, axis=1)
    image_proportion_threshold = max(df_pdf_pages['ImageAreaProportion'].mean(), 0.1)
    image_count_threshold = df_pdf_pages['ImageCount'].mean()

    # return the PdfPageIds of the pdf pages that meet the thresholds
    return df_pdf_pages[(df_pdf_pages["ImageAreaProportion"] > image_proportion_threshold) |
                        (df_pdf_pages["ImageCount"] > image_count_threshold)]["PdfPageId"].unique().tolist()


def identify_valid_figures(pdf_id):
    """
    This function identify the valid figures and insert/update to the Content and Figure tables
    """
    with ExceptionHandler(f"Error removing existing figures for PdfId - {pdf_id}"), engine.begin() as conn:
        # Delete content will result in also deleting the Figures because of a delete cascade
        delete_stmt = f"""
            DELETE c
            FROM {schema}.Content c
                INNER JOIN {schema}.PdfPage pp 
                    ON c.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            WHERE Type = '{ContentType.FIGURE.value}';
        """
        conn.exec_driver_sql(delete_stmt)

    pdf_page_id_list = _find_pdf_pages_with_figures(pdf_id)
    if not pdf_page_id_list:
        berdi_logger.log_info(f"No valid figures found for PdfId - {pdf_id}")
        return

    # select blocks from blocks if they are on the identified pdf pages
    with ExceptionHandler(f"Error querying Block of PdfId - {pdf_id}"), engine.begin() as conn:
        pdf_page_condition_str = f"={pdf_page_id_list[0]}" if len(pdf_page_id_list) == 1 else \
            f"IN {tuple(pdf_page_id_list)}"
        df_blocks = pd.read_sql_query(f'''
            SELECT BlockId, PdfPageId
            FROM {schema}.Block 
            WHERE PdfPageId {pdf_page_condition_str} AND IsImage = 1;
            ''', con=conn)

    # call stored procedure to insert records to Content and Figure tables
    stored_proc = f'''Exec {schema}.PR_Load_Figure @intBlockId = ?, @intPdfPageId = ?;'''
    with ExceptionHandler(f"Error loading Figures of PdfId - {pdf_id}"), engine.begin() as conn:
        for _, row in df_blocks.iterrows():
            params = (int(row["BlockId"]), int(row["PdfPageId"]))
            conn.exec_driver_sql(stored_proc, params)
