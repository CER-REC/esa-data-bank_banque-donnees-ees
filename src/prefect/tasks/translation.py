from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.create_output_files.translation.prepare_for_translation import create_translation_file
from src.functions.create_output_files.translation.load_translation import load_translation


@task
@log_execution_info
def execute_create_translation_file_task():
    """
    This task outputs a csv file with EnglishText column listing the text to be translated
    The file will be located in output root directory
    """
    create_translation_file()


@task
@log_execution_info
def execute_load_translation_task(filepath):
    """
    This task populates or updates the French columns with the translation results in a csv file, whose filepath is
    the input to this function
    """
    load_translation(filepath)
