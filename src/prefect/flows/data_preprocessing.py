from prefect import flow

from src.util.process_applications import get_pdf_status
from src.prefect.tasks.data_preprocessing import execute_extract_pdf_page_text_task, \
    execute_clean_pdf_page_text_task, \
    execute_extract_toc_items_task, \
    execute_extract_rotated_pdf_page_text_task, \
    execute_clean_rotated_pdf_page_text_task, \
    execute_extract_pdf_page_metadata_task, \
    execute_extract_camelot_table_task, \
    execute_extract_block_task


@flow(name="preprocess data")
def execute_preprocessing_flow(pdf_ids):
    """
        This flow includes the following tasks:-
        - extract and load pdf page text
        - clean and load pdf page text
        - rotate pdf, extract and load rotated pdf page text
        - clean and load rotated pdf page text
        - extract and load TOC items
        - extract tables using camelot
        - extract blocks using pymupdf
        - extract pdf page metadata (for alignment sheet classification)

        refer to the following link:-
        https://miro.com/app/board/uXjVPpTQGgo=/
    """
    for pdf_id in pdf_ids:
        pdf_status = get_pdf_status(pdf_id)
        if not pdf_status["is_page_text_extracted"]:
            execute_extract_pdf_page_text_task(pdf_id)
            execute_clean_pdf_page_text_task(pdf_id)

        if not pdf_status["is_rotated_page_text_extracted"]:
            execute_extract_rotated_pdf_page_text_task(pdf_id)
            execute_clean_rotated_pdf_page_text_task(pdf_id)

        if not pdf_status["is_toc_item_extracted"]:
            execute_extract_toc_items_task(pdf_id)

        if not pdf_status["is_camelot_table_extracted"]:
            execute_extract_camelot_table_task(pdf_id)

        if not pdf_status["is_block_extracted"]:
            execute_extract_block_task(pdf_id)

        if not pdf_status["is_page_metadata_extracted"]:
            execute_extract_pdf_page_metadata_task(pdf_id)
