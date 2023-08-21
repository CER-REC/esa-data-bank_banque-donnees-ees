import pandas as pd

from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.extract_titles_from_text import TitleType, extract_titles_from_text
from src.functions.extract_figure_title_using_text_matching.upsert_figure_title_text import upsert_figure_title_text


def extract_figure_title_using_text_matching(pdf_id):
    """
    This function receives a pdf_id and upsert TitleText column in Figure table for all the figures found in the pdf
    """
    # Get all the pdf pages with figures and their raw page text and rotated page text
    with ExceptionHandler(f"Failed to query PdfPage with Figures for PdfId - {pdf_id}"), engine.begin() as conn:
        df_pdf_pages = pd.read_sql(f'''
            SELECT pp.PdfPageId, pp.RawText, pp.RawTextRotated90
            FROM {schema}.PdfPage pp 
            WHERE pp.PdfId = {pdf_id}
                AND EXISTS (
                    SELECT 1
                    FROM {schema}.Figure f
                    WHERE PP.PdfPageId = f.PdfPageId);
            ''', conn)

    if df_pdf_pages.empty:
        return

    # Get all the figures with their PdfPageId and orders on the pages
    with ExceptionHandler(f"Failed to query Figures for PdfId - {pdf_id}"), engine.begin() as conn:
        df_figures = pd.read_sql(f'''
            SELECT FigureId
                , f.PdfPageId
                , ROW_NUMBER() OVER (PARTITION BY b.PdfPageId ORDER BY b.OrderNumber) AS NewOrder
            FROM {schema}.Figure f 
                INNER JOIN {schema}.PdfPage pp 
                    ON f.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
                INNER JOIN {schema}.Block b
                    ON f.BlockId = b.BlockId
            ORDER BY PdfPageId, NewOrder;
            ''', conn)
    df_figures['TitleText'] = None

    for _, row in df_pdf_pages.iterrows():
        # iterate each pdf page and extract figure titles from the page
        titles = extract_titles_from_text(row["RawText"], TitleType.FIGURE.value)
        if not titles:
            titles = extract_titles_from_text(row["RawTextRotated90"], TitleType.FIGURE.value)

        # align all figures on the page and assign titles to the figures by matching the order
        for index, title in enumerate(titles):
            df_figures.loc[(df_figures["PdfPageId"] == row['PdfPageId']) & (df_figures["NewOrder"] == index+1),
                           "TitleText"] = title
    
    # upsert the titles extracted using text matching to TitleText column in Figure table
    if not df_figures.empty:
        upsert_figure_title_text(pdf_id, df_figures[['FigureId', 'TitleText']])
