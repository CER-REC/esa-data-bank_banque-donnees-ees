from prefect import flow

from src.prefect.helper import log_execution_info
from src.util.process_applications import get_pdf_ids
from src.prefect.tasks.alignment_sheet_extraction import execute_extract_alignment_sheet_task, \
    execute_extract_alignment_sheet_title_task


@flow(name="alignment sheet extraction")
@log_execution_info
def execute_alignment_sheet_extraction_flow(application_id):
    """
        This flow includes the following tasks:-
        - Extract alignment sheets
        - Extract titles for the alignment sheets

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    pdf_ids = get_pdf_ids(application_id)
    for pdf_id in pdf_ids:
        execute_extract_alignment_sheet_task(pdf_id)
        execute_extract_alignment_sheet_title_task(pdf_id)
    