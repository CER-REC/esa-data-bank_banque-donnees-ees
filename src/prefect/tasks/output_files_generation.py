from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.create_output_files.internal.create_table_download_zip_folders import \
    create_table_download_zip_folders
from src.functions.create_output_files.internal.create_project_download_zip_folder import \
    create_project_download_zip_folder
from src.functions.create_output_files.internal.create_master_index_file import create_master_index_file
from src.functions.create_output_files.external.create_external_dataset import create_external_folder
from src.functions.rename_table_element_filenames.main import rename_table_element_filenames
from src.functions.create_output_files.language import Language
from src.util.process_applications import get_pdf_ids


@task
@log_execution_info
def execute_generate_internal_folders_task(app_id):
    """
        This task creates necessary folders to store the internal English dataset
        for a specific application id
    """
    
    # generate internal folders for the English language
    create_table_download_zip_folders(application_id=app_id, language=Language.EN.value)
    create_project_download_zip_folder(application_id=app_id, language=Language.EN.value)
    create_master_index_file(application_id=app_id, language=Language.EN.value)

    # generate internal folders for the French language
    pdf_ids = get_pdf_ids(app_id)
    for pdf_id in pdf_ids:
        rename_table_element_filenames(pdf_id, Language.FR.value)
    create_table_download_zip_folders(application_id=app_id, language=Language.FR.value)
    create_project_download_zip_folder(application_id=app_id, language=Language.FR.value)
    create_master_index_file(application_id=app_id, language=Language.FR.value)


@task
@log_execution_info
def execute_generate_external_folders_task():
    """
        This task creates necessary folders to store the external dataset
    """

    # generate external folders for the English language
    create_external_folder(language=Language.EN.value)

    # generate external folders for the French language
    create_external_folder(language=Language.FR.value)
