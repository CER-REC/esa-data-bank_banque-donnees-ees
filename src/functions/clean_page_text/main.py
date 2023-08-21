from src.util.pdf_page.clean_pdf_page_text import clean_pdf_page_text
from src.util.pdf_page.upsert_pdf_page_text import upsert_pdf_page_text
from src.util.pdf_page.pdf_page import PdfPageTextColumn


def clean_page_text(pdf_id):
    """
        This function loads raw page contents from the database for a specific pdf. 
        Then The function changes text to lower case characters. Then removes emails, 
        special characters, and trailing spaces. Reduces multiple white spaces (>2) 
        to single white spaces. Finally updates the database.

        Parameters
        ----------
        pdf_id: id of the pdf document

        Returns
        ----------
        (boolean, string) tuple to indicate success or failure with error message 
        
    """
    
    page_clean_text_dict = clean_pdf_page_text(pdf_id)
    upsert_pdf_page_text(pdf_id, page_clean_text_dict, PdfPageTextColumn.CLEAN_TEXT.value)
