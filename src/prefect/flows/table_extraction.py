from prefect import flow

from src.prefect.helper import log_execution_info
from src.util.process_applications import get_pdf_ids
from src.prefect.tasks.table_extraction import execute_identify_valid_table_elements_task, \
    execute_find_toc_referred_pdf_pages_task, \
    execute_extract_table_element_title_text_task, \
    execute_extract_table_element_title_using_toc_task, \
    execute_extract_final_table_element_title_task, \
    execute_calculate_good_quality_table_pdf_task, \
    execute_rename_table_element_filenames_task, \
    execute_group_table_elements_task


@flow(name="table extraction")
@log_execution_info
def execute_table_extraction_flow(application_id):
    """
        This flow includes the following tasks:-
        - Identify Valid CSV Tables
        - Find TOC referred PDF pages
        - Extract Table Titles
        - Find Good Quality CSV Tables
        - Rename CSV Files
        - Identify Mapping of Multiple CSV Tables to Tables

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    # This flow is carried out at an application level
    # because the task of finding TOC referred pdf pages scans all the pdf files within an application

    pdf_ids = get_pdf_ids(application_id)
    for pdf_id in pdf_ids:
        execute_identify_valid_table_elements_task(pdf_id)

    # Task find_toc_referred_pdf_pages needs to be run after the task
    # identify_valid_table_elements as it has dependency on that task.
    # Task find_toc_referred_pdf_pages is running on application level
    # rather than PDF level and hence it's executed out of for loop.
    execute_find_toc_referred_pdf_pages_task(application_id)

    # Task extract_table_element_title_using_toc should be run after
    # find_toc_referred_pdf_pages task
    for pdf_id in pdf_ids:
        execute_extract_table_element_title_text_task(pdf_id)
        execute_extract_table_element_title_using_toc_task(pdf_id)
        execute_extract_final_table_element_title_task(pdf_id)
        execute_calculate_good_quality_table_pdf_task(pdf_id)
        execute_rename_table_element_filenames_task(pdf_id)
        execute_group_table_elements_task(pdf_id)
