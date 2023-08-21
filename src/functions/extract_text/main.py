from src.util.pdf_page.extract_pdf_page_text import extract_pdf_page_text
from src.util.pdf_page.upsert_pdf_page_text import upsert_pdf_page_text
from src.util.pdf_page.pdf_page import PdfPageTextColumn


def extract_page_text(pdf_id):
    """
        This function loads the original file location of the pdf document
        from the database using the PdfId attribute. Then it 
        extracts the text content from the pdf document for all the pages 
        and inserts it into the database.
    """
    page_text_dict = extract_pdf_page_text(pdf_id)
    upsert_pdf_page_text(pdf_id, page_text_dict, PdfPageTextColumn.RAW_TEXT.value)
