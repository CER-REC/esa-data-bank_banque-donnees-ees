from src.util.content.content_type import ContentType
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def remove_contents_with_empty_titles(pdf_id, content_type):
    """
        This function removes all the records from the 'Content' table where 'Title'
        field is empty. The 'Content' table has on delete cascade enabled. Therefore,
        deletion of a content record would result in the deletion of the
        linked records in the 'TableElement' table.

        Params
        -----------------
        pdf_id (number): pdf_id of the table 'Pdf'
        content_type: value of ContentType enum - TableElement, Figure, AlignmentSheet

        Returns
        -----------------
        None
    """
    with ExceptionHandler("Unrecognized content_type for remove_contents_with_empty_titles function"):
        if content_type not in (type.value for type in ContentType):
            raise ValueError(f"Unrecognized content_type for remove_contents_with_empty_titles function: "
                             f"{content_type}")

    stmt = f"""DELETE ct 
                FROM {schema}.Content ct 
                    INNER JOIN {schema}.PdfPage pg 
                        ON ct.PdfPageId = pg.PdfPageId 
                            AND (ct.Title IS NULL OR ct.Title = '') 
                            AND pg.PdfId = '{pdf_id}'
                WHERE Type = '{content_type}';
            """
    with ExceptionHandler(f"Failed to delete the contents of PdfId - {pdf_id} with empty titles"), \
        engine.begin() as conn:
        conn.exec_driver_sql(statement=stmt)
