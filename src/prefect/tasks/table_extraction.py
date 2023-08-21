from prefect import task

from src.prefect.helper import log_execution_info
from src.functions.identify_valid_table_elements.main import identify_valid_table_elements
from src.functions.find_TOC_referred_pdf_pages.main import find_toc_referred_pdf_pages
from src.functions.extract_TOCs.main import TOCType
from src.functions.extract_table_element_title_using_text_matching.main \
    import extract_table_element_title_using_text_matching
from src.functions.extract_table_element_title_using_TOC.main import extract_table_element_title_using_toc
from src.functions.extract_final_table_element_title.main import extract_final_table_element_title
from src.functions.calculate_good_quality_table_pdf.main import check_good_quality_table_pdf
from src.functions.rename_table_element_filenames.main import rename_table_element_filenames
from src.functions.group_table_elements.main import group_table_elements


@task
@log_execution_info
def execute_identify_valid_table_elements_task(pdf_id):
    """
        This task checks if the tables in CamelotTable are valid and then uses a stored procedure
        to insert TableElementId, CamelotTableId, PdfPageId into TableElement table
        and insert PdfPageId, Type values in Content table
    """
    identify_valid_table_elements(pdf_id)


@task
@log_execution_info
def execute_find_toc_referred_pdf_pages_task(application_id):
    """
        This task finds the referred pdf pages for all the Table TOC items,
        and upserts the TOCReferredPdfPage table
    """
    find_toc_referred_pdf_pages(application_id, TOCType.TABLE.value)


@task
@log_execution_info
def execute_extract_table_element_title_text_task(pdf_id):
    """
        This task updates the TitleText column of the DB Table 'TableElement'
    """
    extract_table_element_title_using_text_matching(pdf_id)


@task
@log_execution_info
def execute_extract_table_element_title_using_toc_task(pdf_id):
    """
        This task finds the title of all the table elements using TOC titles
        for a given pdf_id and update TitleTOC column of TableElement table
    """
    extract_table_element_title_using_toc(pdf_id)


@task
@log_execution_info
def execute_extract_final_table_element_title_task(pdf_id):
    """
        This task updates the Title column of the DB Table 'Content'
        and then delete all the rows of DB Table 'Content' and 'TableElement'
        where Title field is empty
    """
    extract_final_table_element_title(pdf_id)


@task
@log_execution_info
def execute_calculate_good_quality_table_pdf_task(pdf_id):
    """
        This task calculates QA metrics for all TableElementId tagged to the
        PdfId mentioned in the function argument and updates IsGoodQuality column
        of DB table TableElement and then updates the Pdf DB Table HasGoodQuality
        column value to 1 if a PDF generated over 20 % of problematic tables and 0 otherwise.
    """
    check_good_quality_table_pdf(pdf_id, 20)


@task
@log_execution_info
def execute_rename_table_element_filenames_task(pdf_id):
    """
        This task updates the FileName column of the DB Table TableElement
    """
    rename_table_element_filenames(pdf_id)


@task
@log_execution_info
def execute_group_table_elements_task(pdf_id):
    """
        This task finds table element groups - groups of table elements that
        have the same title and appear on consecutive pdf pages, and create
        new table element rows and update the TableElementGroupId values in TableElement
        table accordingly.
    """
    group_table_elements(pdf_id)
