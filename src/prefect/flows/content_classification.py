from prefect import flow

from src.prefect.helper import log_execution_info
from src.util.process_applications import get_pdf_ids
from src.prefect.tasks.content_classification import execute_label_ik_task, execute_label_vcs_task


@flow(name="label IK and VCs")
@log_execution_info
def execute_content_classification_flow(application_id):
    """
        This flow includes the following tasks:-
        - Label IK to all the content
        - Label VC to all the content

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    pdf_ids = get_pdf_ids(application_id)
    for pdf_id in pdf_ids:
        execute_label_ik_task(pdf_id)
        execute_label_vcs_task(pdf_id)
