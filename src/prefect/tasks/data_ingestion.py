from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.load_applications.main import load_applications
from src.functions.load_pdfs.main import load_pdfs
from src.functions.download_pdf.main import download_file
from src.util.process_applications import get_application_ids
from src.functions.delete_temp_tables.main import delete_temp_tables


@task
@log_execution_info
def execute_delete_temp_tables_task():
    """
        This task drops all the temporary tables in the database
    """
    delete_temp_tables()


@task
@log_execution_info
def execute_load_applications_task():
    """
        This task reads the input csv file and upsert application attributes to database table
    """
    load_applications()


@task
@log_execution_info
def execute_load_pdfs_task():
    """
        This task reads the input csv file and upsert pdf attributes to database table
    """
    load_pdfs()


@task
@log_execution_info
def execute_download_all_pdfs_task():
    """
        This task reads download url from the Application table
        and download all the pdf files
    """
    app_ids = get_application_ids()
    for app_id in app_ids:
        download_file(app_id)
