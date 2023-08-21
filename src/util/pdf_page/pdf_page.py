from enum import Enum


class PdfPageTextColumn(Enum):
    """ Enum for text columns in PdgPage table """
    RAW_TEXT = "RawText"
    CLEAN_TEXT = "CleanText"
    RAW_ROTATED90_TEXT = "RawTextRotated90"
    CLEAN_ROTATED90_TEXT = "CleanTextRotated90"


def get_pdf_page_folder(page_rotation_degree):
    """
    This function returns the corresponding pdf page folder given the rotation degree
    """
    if page_rotation_degree == 0:
        return "pdf_pages"
    if page_rotation_degree == 90:
        return "pdf_rotated90_pages"
    return "pdf_pages"
