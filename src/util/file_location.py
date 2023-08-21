import pandas as pd
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def get_pdf_file_location(pdf_id):
    """
        Given a pdf_id, returns the absolute path of the pdf document. 
        Absolute path points to the location of a shared network folder.
    """
    query = f"SELECT FilePath from {schema}.Pdf WHERE PdfId = {pdf_id};"
    with ExceptionHandler(f"Error executing select sql statement for PdfId - {pdf_id}"), engine.begin() as conn:
        pdf_data = pd.read_sql(query, conn)
    
    n_rows, _ = pdf_data.shape

    with ExceptionHandler(f"No pdf found with PdfId - {pdf_id}"):
        if n_rows <= 0:
            raise ValueError(f"No pdf found with PdfId - {pdf_id}")

    with ExceptionHandler(f"Missing FilePath for PdfId - {pdf_id}"):
        if not pdf_data["FilePath"].iloc[0]:
            raise ValueError(f"Missing FilePath for PdfId - {pdf_id}")

    return pdf_data["FilePath"].iloc[0]


def get_regdocs_id(pdf_id):
    """
        Given a pdf_id, returns the RegdocsDataId of the pdf document. 
    """
    query = f"SELECT RegdocsDataId from {schema}.Pdf WHERE PdfId = {pdf_id};"
    with ExceptionHandler(f"Error executing select sql statement for PdfId - {pdf_id}"), engine.begin() as conn:
        pdf_data = pd.read_sql(query, conn)
    
    n_rows, _ = pdf_data.shape

    with ExceptionHandler(f"No pdf found with PdfId - {pdf_id}"):
        if n_rows <= 0:
            raise ValueError(f"No pdf found with PdfId - {pdf_id}")

    with ExceptionHandler(f"Missing RegdocsDataId for PdfId - {pdf_id}"):
        if not pdf_data["RegdocsDataId"].iloc[0]:
            raise ValueError(f"Missing RegdocsDataId for PdfId - {pdf_id}")

    return pdf_data["RegdocsDataId"].iloc[0]
