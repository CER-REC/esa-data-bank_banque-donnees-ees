import os
from pathlib import Path
import requests
import pandas as pd
import fitz
from src.util.file_location import get_pdf_file_location
from src.util.pdf_page.pdf_page import get_pdf_page_folder
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.exception_and_logging.process_logs import berdi_logger

THUMBNAIL_WIDTH = 198
THUMBNAIL_HEIGHT = 153

def save_thumbnail(file_path, page_index, regdocs_id, page_number):
    """
        store pdf page thumbnail based on pdf path and page number

        Parameters
        --------------------
        file_path (string): absolute path of the file
        page_index (int): index of the page that starts with 0 to total page count - 1
        regdocs_id (int): regdocs id of the pdf document
        page_number (int): page number that starts with 1 to total page count
    """
    doc = fitz.open(file_path)
    page = doc.load_page(page_index)
    pix = page.get_pixmap(alpha=True)
    pix_new = fitz.Pixmap(pix, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, None)
    with ExceptionHandler(f"Error storing the thumbnail file for RegdocsId - {regdocs_id}"):
        pix_new.save(Path(os.getenv("OUTPUT_ROOT_DIRECTORY")).joinpath("thumbnails")
                     .joinpath(f"{regdocs_id}_{page_number}.jpg"))

def create_thumbnail(application_id):
    """
        create a thumbnail of size 198 in width and 153 in height (portrait)
        for all pages based on an application id
    """
    query = f"""
        SELECT *
        FROM (SELECT pd.RegdocsDataId as RegdocsDataId, pd.PdfId AS PdfId, 
                pg.PageNumber AS PageNumber, pd.PDFDownloadURL AS PDFDownloadURL
                FROM {schema}.Pdf pd
                    LEFT JOIN {schema}.PdfPage pg ON pd.PdfId = pg.PdfId
                    INNER JOIN {schema}.Content ct ON pg.PdfPageId = ct.PdfPageId 
                    AND (ct.Type = 'AlignmentSheet' OR ct.Type = 'Figure')
                    AND pd.ApplicationId = '{application_id}'

                UNION

                SELECT pd.RegdocsDataId as RegdocsDataId, pd.PdfId AS PdfId, 
                    mn.Min_Page AS PageNumber, pd.PDFDownloadURL AS PDFDownloadURL
                FROM {schema}.Pdf pd
                    LEFT JOIN {schema}.PdfPage pg ON pd.PdfId = pg.PdfId
                    INNER JOIN {schema}.TableElement te ON te.PdfPageId = pg.PdfPageId
                    INNER JOIN (
                        SELECT te.TableElementGroupId, MIN(pg.PageNumber) AS Min_Page
                        FROM {schema}.TableElement te 
                        INNER JOIN {schema}.PdfPage pg ON pg.PdfPageId = te.PdfPageId
                        GROUP BY te.TableElementGroupId
                    ) mn ON mn.TableElementGroupId = te.TableElementGroupId
                    AND pd.ApplicationId = '{application_id}') T
        GROUP BY RegdocsDataId, PdfId, PageNumber, PDFDownloadURL;
    """
    
    # Get all pages with page text of this pdf
    with ExceptionHandler(f"Error querying thumbnail information for Application Id - {application_id}"), \
            engine.begin() as conn:
        df_thumbnail = pd.read_sql(query, conn)
    
    for _, row in df_thumbnail.iterrows():
        regdocs_id, pdf_id, page_number = row["RegdocsDataId"], row["PdfId"], row["PageNumber"]

        pdf_file_path = get_pdf_file_location(pdf_id)

        pdf_page_folder_name = get_pdf_page_folder(page_rotation_degree=0)

        pdf_page_root = Path(pdf_file_path).parent.parent

        pdf_page_file_path = pdf_page_root.joinpath(pdf_page_folder_name).joinpath(f"{pdf_id}_{page_number}.pdf")
        
        if os.path.exists(pdf_page_file_path):
            # if pdf page is available then it's just one page
            # that's why the first page (index = 0) is selected
            save_thumbnail(file_path=pdf_page_file_path, page_index=0, regdocs_id=regdocs_id, \
                           page_number=page_number)
        
        # if pdf page is not available look for the main pdf
        elif os.path.exists(pdf_file_path):
            # page number starts from 1
            save_thumbnail(file_path=pdf_file_path, page_index=page_number-1, regdocs_id=regdocs_id, \
                           page_number=page_number)
        
        else:
            # if both the main pdf file and pdf page file is removed
            # then just download the pdf file and save the thumbnail 
            with ExceptionHandler(f"Error downloading file for PdfId - {pdf_id}"):
                # timeout in 5 seconds
                response = requests.get(row["PDFDownloadURL"], timeout=5)

            with ExceptionHandler(f"Error opening file {pdf_file_path}"), open(pdf_file_path, "wb") as file:
                file.write(response.content)
            
            save_thumbnail(file_path=pdf_file_path, page_index=0, regdocs_id=regdocs_id, page_number=page_number)
        
        berdi_logger.log_info(f"Processing of ApplicationId - {application_id}, RegdocsId - {regdocs_id}, "
                          f"PdfId - {pdf_id}, and PageNumber {page_number} completed")
