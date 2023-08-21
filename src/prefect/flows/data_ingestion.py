from prefect import flow

from src.prefect.tasks.data_ingestion import \
    execute_delete_temp_tables_task, \
    execute_load_applications_task, \
    execute_load_pdfs_task, \
    execute_download_all_pdfs_task


@flow(name="data ingestion")
def execute_data_ingestion_flow():
    """
        This flow includes the following tasks:
        1. deletes all the temporary tables in the database
        2. read applications from a csv file and upsert the Applications table
        3. read Applications table and update the Pdf table
        4. download all the pdf files read from the Pdf table
    """
    execute_delete_temp_tables_task()
    execute_load_applications_task()
    execute_load_pdfs_task()
    execute_download_all_pdfs_task()
