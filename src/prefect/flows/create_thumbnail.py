from prefect import flow

from src.prefect.tasks.create_thumbnail import execute_create_thumbnail_task
from src.prefect.helper import log_execution_info

@flow(name="create thumbnails")
@log_execution_info
def execute_create_thumbnail_flow(application_id):
    """
        This flow creates thumbnail files for all the pages containing
        alignment sheet, figure or table

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    execute_create_thumbnail_task(application_id)
