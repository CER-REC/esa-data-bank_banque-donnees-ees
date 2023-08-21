from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.content.content_type import ContentType
from src.util.content.remove_contents_with_empty_titles import remove_contents_with_empty_titles


def extract_final_figure_title(pdf_id):
    """
    This function receives a pdf_id and updates the Title column in Content table of all the figures in the pdf
    Figures with no titles found are deleted at the end
    """
    # use TitleText as the first option and TitleTOC as the second option for the final title of a figure
    # if TitleText or TitleTOC is not null, and update Title column in Content table accordingly
    with ExceptionHandler(f"Failed to extract final figure titles for PdfId - {pdf_id}"), engine.begin() as conn:
        conn.exec_driver_sql(f"""
             WITH Source AS (
                select FigureId
                    , ISNULL(TitleText, TitleTOC) as FinalTitle
                FROM {schema}.Figure f
                    INNER JOIN {schema}.PdfPage pp ON f.PdfPageId = pp.PdfPageId 
                        AND PdfId = {pdf_id}
                WHERE TitleText IS NOT NULL OR TitleTOC IS NOT NULL
            )
            UPDATE {schema}.Content
            SET Content.Title = Source.FinalTitle
            FROM Source
            WHERE ContentId = Source.FigureId;
        """)

    # remove records of 'Content' and 'Figure' if title is empty or ''
    remove_contents_with_empty_titles(pdf_id, ContentType.FIGURE.value)
