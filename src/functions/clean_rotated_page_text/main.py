from src.util.pdf_page.clean_pdf_page_text import clean_pdf_page_text
from src.util.pdf_page.upsert_pdf_page_text import upsert_pdf_page_text
from src.util.pdf_page.pdf_page import PdfPageTextColumn


def clean_rotated90_page_text(pdf_id):
    """
        This function retrieves and cleans the raw text of rotated 90 degrees from the database for a specific pdf,
        and insert or update the clean rotated text in the database.
    """
    page_rotation_degree = 90
    page_text_dict = clean_pdf_page_text(pdf_id, page_rotation_degree)
    upsert_pdf_page_text(pdf_id, page_text_dict, PdfPageTextColumn.CLEAN_ROTATED90_TEXT.value)
