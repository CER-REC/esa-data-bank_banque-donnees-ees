# pylint: disable=duplicate-code
from src.util.database_connection import schema, engine


def extract_figure_title_using_toc(pdf_id):
    """
    This function extracts figure titles using TOC titles for a given pdf
    """
    with engine.begin() as conn:
        conn.exec_driver_sql(f"""
           WITH Figure_CTE AS (
               /* 
               get the figures, the pdf pages where the figures are extracted from, 
               and the order in which the figures appear on their pdf pages
               */
               SELECT f.FigureId
                   , f.PdfPageId
                   , RANK() OVER (PARTITION BY f.PdfPageId ORDER BY b.OrderNumber) AS NewOrderNumber
               FROM {schema}.Figure f
                   INNER JOIN {schema}.Block b
                       ON f.BlockId = b.BlockId
                   INNER JOIN {schema}.PdfPage pp 
                       ON f.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
           ), TitleTOC_CTE AS (
               /*
               get the TOC titles, the pdf pages the TOCs refer to, and the order in which the TOC elements are listed
               */
               SELECT t.ContentTitle AS TitleTOC
                   , tf.PdfPageId
                   , RANK() OVER (PARTITION BY tf.PdfPageId ORDER BY tpp.PageNumber, t.OrderNumber) AS NewOrderNumber
               FROM {schema}.TOCReferredPdfPage tf
                   INNER JOIN {schema}.TOC t 
                       ON t.TOCId = tf.TOCId AND t.ContentType = 'Figure'
                   INNER JOIN {schema}.PdfPage pp 
                       ON pp.PdfPageId = tf.PdfPageId AND pp.PdfId = {pdf_id}
                   INNER JOIN {schema}.PdfPage tpp
                       ON tpp.PdfPageId = t.PdfPageId
           ), Source AS (
               /*
               match figures and TOC titles based on the pdf pages and the orders
               */
               SELECT f.FigureId, t.TitleTOC
               FROM Figure_CTE f
                   INNER JOIN TitleTOC_CTE t 
                       ON f.PdfPageId = t.PdfPageId AND f.NewOrderNumber = t.NewOrderNumber
           )

           UPDATE {schema}.Figure 
           SET Figure.TitleTOC = Source.TitleTOC
           FROM Source
           WHERE Figure.FigureId = Source.FigureId;
        """)
