import collections
from pathlib import Path

import os
from PyPDF2 import PdfReader, PdfWriter
from tika import parser
from src.util.file_location import get_pdf_file_location, \
    get_regdocs_id
from src.util.pdf_page.pdf_page import get_pdf_page_folder
from src.util.exception_and_logging.handle_exception import ExceptionHandler


EMPTY_PAGE_TEXT = "This page intentionally left blank."

def extract_pdf_page_text(pdf_id, page_rotation_degree=0):
    """
        Given a pdf_id, the pdf file path will be retrieved. Based on the page_rotation value, each pdf
        page will be kept its own orientation or rotated. After rotation, the text of each page will be
        appended to a list and returned from the function.

        (Special Instructions): Tika parser does not support page level text
        processing. Therefore, we read the Pdf content using PyPDF2 and then
        store each page separately in a different directory. Finally, Tika parser
        is used to extract the text content from the pdf.
    """
    file_path = get_pdf_file_location(pdf_id)

    regdocs_id = get_regdocs_id(pdf_id)

    pdf_page_folder_name = get_pdf_page_folder(page_rotation_degree)

    pdf_page_root = Path(file_path).parent.parent.joinpath(pdf_page_folder_name)
    if not os.path.isdir(pdf_page_root):
        os.makedirs(pdf_page_root)

    with ExceptionHandler(f"Error reading pdf using PyPDF2 for PdfId - {pdf_id}"):
        reader = PdfReader(file_path)

    number_of_pages = len(reader.pages)

    page_text_dict = collections.defaultdict(str)

    for index in range(number_of_pages):
        # page number starts from 1
        page_num = index + 1
        page_file_name = pdf_page_root.joinpath(f"{regdocs_id}_{page_num}.pdf")

        # skip pages that already exists
        if not os.path.exists(page_file_name):
            with ExceptionHandler(f"Error writing file - {page_file_name}"), open(page_file_name, "wb") as temp_file:
                writer = PdfWriter()
                writer.add_page(reader.pages[index].rotate(page_rotation_degree))
                writer.write(temp_file)

        # tika's parser extracts content of one page
        with ExceptionHandler(f"Error parsing pdf {page_file_name} using tika"):
            content = parser.from_file(str(page_file_name),
                                       xmlContent=False,
                                       requestOptions={"timeout": 300})["content"]

        if content is None:
            content = EMPTY_PAGE_TEXT

        page_text_dict[page_num] = content.strip()

    return page_text_dict
