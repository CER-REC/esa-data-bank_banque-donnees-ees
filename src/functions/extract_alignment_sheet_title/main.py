import pandas as pd

from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.extract_titles_from_text import TitleType, extract_titles_from_text
from src.functions.extract_alignment_sheet_title.update_alignment_sheet_title import update_alignment_sheet_title, \
    update_content_title_from_alignment_sheet


def extract_alignment_sheet_title(pdf_id):
    """
    Given a pdf id, this function extracts titles for the alignment sheets in the pdf, and updates Title, FigureId
    columns in AlignmentSheet table and Title column in Content table for AlignmentSheet
    """
    # Find the figures that are on the same pdf pages as the alignment sheets and assign the figure titles to the
    # alignment sheet titles; if there are multiple figures on the same page, use the title of the first figure
    with ExceptionHandler(f"Error updating alignment sheet titles from figure titles for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        conn.exec_driver_sql(f'''
        WITH figure_title_cta AS (
            SELECT FigureId, PdfPageId, Title
            FROM (
                SELECT f.FigureId
                    , f.PdfPageId
                    , Title
                    , ROW_NUMBER() OVER (PARTITION BY b.PdfPageId ORDER BY b.OrderNumber) AS NewOrder
                FROM {schema}.Content c
                    LEFT JOIN {schema}.Figure f ON c.ContentId = f.FigureId
                    LEFT JOIN {schema}.Block b ON f.BlockId = b.BlockId
                WHERE Type = 'Figure' 
                    AND EXISTS (
                        SELECT 1 
                        FROM {schema}.AlignmentSheet a
                            INNER JOIN {schema}.PdfPage p ON a.PdfPageId = p.PdfPageId AND p.PdfId = {pdf_id}
                        WHERE a.PdfPageId = c.PdfPageId
                    )
            ) tmp
            WHERE NewOrder = 1
        )
        UPDATE {schema}.AlignmentSheet 
        SET AlignmentSheet.Title = figure_title_cta.Title
            , AlignmentSheet.FigureId = figure_title_cta.FigureId
        FROM figure_title_cta
        WHERE AlignmentSheet.PdfPageId = figure_title_cta.PdfPageId
        ''')

    # Select alignment sheet with no titles matched from figures
    with ExceptionHandler(f"Error selecting alignment sheet with no titles extracted for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        df_alignment_sheet = pd.read_sql(f'''
        SELECT  a.AlignmentSheetId
            , pp.RawText
            , pp.PageNumber
            , p.RegdocsDataId
        FROM {schema}.AlignmentSheet a
            INNER JOIN {schema}.PdfPage pp ON a.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            LEFT JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId
        WHERE a.Title IS NULL OR a.Title = ''
        ''', con=conn)

    # Extract alignment sheet titles from page text
    # If no titles extracted, use default format to title the alignment sheet
    df_alignment_sheet["Title"] = None
    for index, row in df_alignment_sheet.iterrows():
        title_candidates = extract_titles_from_text(row["RawText"], TitleType.ALIGNMENT_SHEET.value)
        if title_candidates:
            df_alignment_sheet.loc[index, "Title"] = title_candidates[0]
        else:
            # an example of the default title: "Alignment Sheet 121212 34"
            df_alignment_sheet.loc[index, "Title"] = " ".join(["Alignment Sheet", str(row["RegdocsDataId"]),
                                                               str(row["PageNumber"])])

    # Update Title column in AlignmentSheet table with the titles extracted from page text or using default name
    update_alignment_sheet_title(pdf_id, df_alignment_sheet[["AlignmentSheetId", "Title"]])

    # Update Title column in Content table with the Title values in AlignmentSheet table
    update_content_title_from_alignment_sheet(pdf_id)
