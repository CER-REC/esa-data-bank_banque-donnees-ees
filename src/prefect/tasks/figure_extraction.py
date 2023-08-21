from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.identify_valid_figures.main import identify_valid_figures
from src.functions.extract_TOCs.main import TOCType
from src.functions.find_TOC_referred_pdf_pages.main import find_toc_referred_pdf_pages
from src.functions.extract_figure_title_using_text_matching.main import extract_figure_title_using_text_matching
from src.functions.extract_figure_title_using_TOC.main import extract_figure_title_using_toc
from src.functions.extract_final_figure_title.main import extract_final_figure_title


@task
@log_execution_info
def execute_identify_valid_figures_task(pdf_id):
    """
        This task filters out valid figures from records in Block table,
        and then inserts valid figures into Content and Figure tables using a stored procedure
    """
    identify_valid_figures(pdf_id)


@task
@log_execution_info
def execute_find_toc_referred_pdf_pages_for_figures_task(application_id):
    """
        This task finds the referred pdf pages for all the Figure TOC items and adds to TOCReferredPdfPage table
    """
    find_toc_referred_pdf_pages(application_id, TOCType.FIGURE.value)


@task
@log_execution_info
def execute_extract_figure_title_using_text_matching_task(pdf_id):
    """
        This task finds figure titles of a pdf using text matching and updates TitleText in Figure table
    """
    extract_figure_title_using_text_matching(pdf_id)


@task
@log_execution_info
def execute_extract_figure_title_using_toc_task(pdf_id):
    """
        This task finds figure titles of a pdf using TOC matching and updates TitleTOC in Figure table
    """
    extract_figure_title_using_toc(pdf_id)


@task
@log_execution_info
def execute_extract_final_figure_title_task(pdf_id):
    """
        This task updates the Title column of the DB Table 'Content'
        and then delete all the rows of DB Table 'Content' and 'Figure'
        where Title field is empty
    """
    extract_final_figure_title(pdf_id)
