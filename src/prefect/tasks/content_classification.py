from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.assign_IK_labels.main import assign_ik_labels
from src.functions.label_VCs.main import label_vcs


@task
@log_execution_info
def execute_label_ik_task(pdf_id):
    """
    This task label all the content of a pdf whether they contain IK - Indigenous Knowledge
    """
    assign_ik_labels(pdf_id)


@task
@log_execution_info
def execute_label_vcs_task(pdf_id):
    """
    This tasks label all the content of a pdf whether they contain certain Value Components
    """
    label_vcs(pdf_id)
