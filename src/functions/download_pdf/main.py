import os
from pathlib import Path
import pandas as pd
import requests
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name


def update_pdf_file_path(app_id, df_pdf):
    """
        This function updates the FilePath column in Pdf table based on the dataframe df_pdf
        The dataframe contains PdfId and FilePath columns
    """
    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error updating sql statement with Application Id - {app_id}"), \
        engine.begin() as conn:
        
        # step 1 - create a temp data in database
        df_pdf.to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")
        
        # step 2 - update Title in AlignmentSheet table
        conn.exec_driver_sql(
            f"""
                UPDATE {schema}.Pdf
                SET {schema}.Pdf.FilePath = {schema}.{temp_table_name}.FilePath
                FROM {schema}.{temp_table_name}
                WHERE {schema}.Pdf.PdfId = {schema}.{temp_table_name}.PdfId;
            """
        )


def download_file(application_id):
    """
    This function attempts to download and save all the PDF files in a shared 
    drive folder for a given Application ID where FilePath values are NULL.
    
    Args:
        application_id (integer): Application ID number

    """
    query = f"""
        SELECT PdfId, RegdocsDataId, PDFDownloadURL 
        FROM {schema}.Pdf 
        WHERE ApplicationId = {application_id};
    """

    with ExceptionHandler(f"Error executing sql with ApplicationId - {application_id}"), \
        engine.begin() as conn:
        pdfs = pd.read_sql(query, conn)

    df_pdf = pd.DataFrame(columns=["PdfId", "FilePath"])
    
    for index, row in pdfs.iterrows():
        data_id = row["RegdocsDataId"]
        full_name = Path(os.getenv("ROOT_DIRECTORY")) \
            .joinpath("raw").joinpath("pdfs") \
            .joinpath((str(data_id) + ".pdf"))
        
        if not os.path.exists(full_name):
            with ExceptionHandler(f"Error downloading file for RegDocsId - {data_id}"):
                # timeout in 60 seconds
                response = requests.get(row["PDFDownloadURL"], timeout=60)  
            
            with ExceptionHandler(f"Error opening file {full_name}"), open(full_name, "wb") as file:
                file.write(response.content)

        df_pdf.loc[index, "PdfId"] = row["PdfId"]
        df_pdf.loc[index, "FilePath"] = str(full_name)
    
    update_pdf_file_path(application_id, df_pdf)
