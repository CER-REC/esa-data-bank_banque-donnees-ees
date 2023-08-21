from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.extract_text.main import extract_page_text
from src.functions.clean_page_text.main import clean_page_text
from src.functions.extract_TOCs.main import extract_tocs
from src.functions.extract_rotated_text.main import extract_rotated_text
from src.functions.clean_rotated_page_text.main import clean_rotated90_page_text
from src.functions.extract_page_metadata.main import extract_page_metadata
from src.functions.extract_camelot_table.main import extract_camelot_table
from src.functions.extract_block.main import extract_block


@task
@log_execution_info
def execute_extract_pdf_page_text_task(pdf_id):
    """
        This task reads the text from the Pdf table and
        then store the text into the PdfPage table
    """
    extract_page_text(pdf_id)

@task
@log_execution_info
def execute_clean_pdf_page_text_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    clean_page_text(pdf_id)


@task
@log_execution_info
def execute_extract_toc_items_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    extract_tocs(pdf_id)


@task
@log_execution_info
def execute_extract_rotated_pdf_page_text_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    extract_rotated_text(pdf_id)


@task
@log_execution_info
def execute_clean_rotated_pdf_page_text_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    clean_rotated90_page_text(pdf_id)


@task
@log_execution_info
def execute_extract_pdf_page_metadata_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    extract_page_metadata(pdf_id)


@task
@log_execution_info
def execute_extract_camelot_table_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    extract_camelot_table(pdf_id)


@task
@log_execution_info
def execute_extract_block_task(pdf_id):
    """
        This task reads the raw text content from the Pdf table,
        clean the text content and then store the text content back into
        the PdfPage table
    """
    extract_block(pdf_id)
