from prefect import task

from src.functions.create_thumbnail.main import create_thumbnail
from src.prefect.helper import log_execution_info

@task
@log_execution_info
def execute_create_thumbnail_task(application_id):
    """
    This task create thumbnail for all pages based on an application id
    """
    create_thumbnail(application_id)
