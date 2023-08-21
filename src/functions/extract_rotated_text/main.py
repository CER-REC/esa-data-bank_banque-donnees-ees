from src.util.pdf_page.extract_pdf_page_text import extract_pdf_page_text
from src.util.pdf_page.upsert_pdf_page_text import upsert_pdf_page_text
from src.util.pdf_page.pdf_page import PdfPageTextColumn


def extract_rotated_text(pdf_id):
    """
    Given the pdf id, pdf file path will be retrieved. Each pdf page will be rotated 90 degrees.
    The rotated pdf page will be saved in the root_directory/raw/pdf_rotated90_pages folder.
    The text of each rotated page will be extracted and inserted into pdf table.
    """
    page_rotation_degree = 90
    page_text_dict = extract_pdf_page_text(pdf_id, page_rotation_degree)
    upsert_pdf_page_text(pdf_id, page_text_dict, PdfPageTextColumn.RAW_ROTATED90_TEXT.value)
