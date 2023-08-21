from prefect import flow

from src.prefect.helper import log_execution_info
from src.prefect.tasks.translation import execute_create_translation_file_task, execute_load_translation_task


@flow(name="prepare translation file to be sent to the translation team")
@log_execution_info
def execute_creating_translation_file_flow():
    """
    This flow creates a translation file to be sent to the translation team
    """
    execute_create_translation_file_task()


@flow(name="load translation and update FrenchFileName")
@log_execution_info
def execute_loading_translation_flow(filepath):
    """
    This flow loads the translation results into the database
    """
    execute_load_translation_task(filepath)
