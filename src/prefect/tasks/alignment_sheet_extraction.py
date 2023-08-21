from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.extract_alignment_sheet.main import extract_alignment_sheet
from src.functions.extract_alignment_sheet_title.main import extract_alignment_sheet_title


@task
@log_execution_info
def execute_extract_alignment_sheet_task(pdf_id):
    """
    This task extracts alignment sheets for a pdf
    """
    extract_alignment_sheet(pdf_id)


@task
@log_execution_info
def execute_extract_alignment_sheet_title_task(pdf_id):
    """
    This task extracts titles for alignment sheets of a pdf
    """
    extract_alignment_sheet_title(pdf_id)
