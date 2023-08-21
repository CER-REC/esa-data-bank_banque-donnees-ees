from prefect import flow

from src.util.process_applications import get_pdf_ids
from src.prefect.tasks.figure_extraction import execute_identify_valid_figures_task, \
    execute_find_toc_referred_pdf_pages_for_figures_task, \
    execute_extract_figure_title_using_text_matching_task, \
    execute_extract_figure_title_using_toc_task, \
    execute_extract_final_figure_title_task


@flow(name="figure extraction")
def execute_figure_extraction_flow(application_id):
    """
        This flow includes the following tasks:-
        - Identify Valid Figures
        - Find TOC referred PDF pages for Figure TOC
        - Extract Figure Titles

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    # This flow is carried out at an application level
    # because the task of finding TOC referred pdf pages scans all the pdf files within an application
    pdf_ids = get_pdf_ids(application_id)
    for pdf_id in pdf_ids:
        execute_identify_valid_figures_task(pdf_id)

    # Task find_toc_referred_pdf_pages needs to be run after the task
    # identify_valid_figures as it has dependency on that task.
    # Task find_toc_referred_pdf_pages is running on application level
    # rather than PDF level and hence it's executed out of for loop.
    execute_find_toc_referred_pdf_pages_for_figures_task(application_id)

    for pdf_id in pdf_ids:
        execute_extract_figure_title_using_text_matching_task(pdf_id)
        execute_extract_figure_title_using_toc_task(pdf_id)
        execute_extract_final_figure_title_task(pdf_id)
