from src.util.database_connection import schema, engine


def extract_table_element_title_using_toc(pdf_id):
    """
    This function updates the title of all the table elements using TOC titles for a given pdf_id
    """
    with engine.begin() as conn:
        conn.exec_driver_sql(f"""
            WITH TableElement_CTE AS (
                /* 
                get the table elements, the pdf pages where the table elements are on, 
                and the order in which the table elements appear on their pdf pages
                */
                SELECT te.TableElementId
                    , te.PdfPageId
                    , RANK() OVER (PARTITION BY te.PdfPageId ORDER BY c.OrderNumber) AS NewOrderNumber
                FROM {schema}.TableElement te
                    INNER JOIN {schema}.CamelotTable c 
                        ON te.CamelotTableId = c.CamelotTableId
                    INNER JOIN {schema}.PdfPage pp 
                        ON te.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            ), TitleTOC_CTE AS (
                /*
                get the TOC titles, the pdf pages the TOCs refer to, and the order in which the TOC elements are listed
                */
                SELECT t.ContentTitle AS TitleTOC
                    , tf.PdfPageId
                    , RANK() OVER (PARTITION BY tf.PdfPageId ORDER BY tpp.PageNumber, t.OrderNumber) AS NewOrderNumber
                FROM {schema}.TOCReferredPdfPage tf
                    INNER JOIN {schema}.TOC t 
                        ON t.TOCId = tf.TOCId AND t.ContentType = 'Table'
                    INNER JOIN {schema}.PdfPage pp 
                        ON pp.PdfPageId = tf.PdfPageId AND pp.PdfId = {pdf_id}
                    INNER JOIN {schema}.PdfPage tpp
                        ON tpp.PdfPageId = t.PdfPageId
            ), Source AS (
                /*
                match table elements and TOC titles based on the pdf pages and the orders
                */
                SELECT te.TableElementId, t.TitleTOC
                FROM TableElement_CTE te
                    INNER JOIN TitleTOC_CTE t 
                        ON te.PdfPageId = t.PdfPageId AND te.NewOrderNumber = t.NewOrderNumber
            )
            
            UPDATE {schema}.TableElement 
            SET TableElement.TitleTOC = Source.TitleTOC
            FROM Source
            WHERE TableElement.TableElementId = Source.TableElementId;
        """)
