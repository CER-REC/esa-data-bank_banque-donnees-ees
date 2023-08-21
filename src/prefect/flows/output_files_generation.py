from prefect import flow

from src.prefect.helper import log_execution_info
from src.prefect.tasks.output_files_generation import execute_generate_internal_folders_task
from src.prefect.tasks.output_files_generation import execute_generate_external_folders_task


@flow(name="generate english dataset internal folders")
@log_execution_info
def execute_internal_dataset_generation_flow(application_id):
    """
        This flow includes the following tasks:-
        - generate english internal folders

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    execute_generate_internal_folders_task(application_id)


@flow(name="generate english dataset external folders")
@log_execution_info
def execute_external_dataset_generation_flow():
    """
        This flow includes the following tasks:-
        - generate english external folders

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    execute_generate_external_folders_task()
