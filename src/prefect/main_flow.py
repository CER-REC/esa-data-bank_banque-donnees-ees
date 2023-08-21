from prefect import flow

from src.util.process_applications import get_pdf_ids
from src.prefect.flows.data_ingestion import execute_data_ingestion_flow
from src.prefect.flows.data_preprocessing import execute_preprocessing_flow
from src.prefect.flows.table_extraction import execute_table_extraction_flow
from src.prefect.flows.figure_extraction import execute_figure_extraction_flow
from src.prefect.flows.alignment_sheet_extraction import execute_alignment_sheet_extraction_flow
from src.prefect.flows.content_classification import execute_content_classification_flow
from src.util.process_applications import get_application_ids


@flow(name="main processing flow")
def execute_main_processing_flow(application_id):
    """
        Start BERDI task orchestration process
        The main flow will extract all the content and populate the database
    """
    pdf_ids = get_pdf_ids(application_id)
    execute_preprocessing_flow(pdf_ids)

    execute_table_extraction_flow(application_id)

    execute_figure_extraction_flow(application_id)

    execute_alignment_sheet_extraction_flow(application_id)

    execute_content_classification_flow(application_id)


if __name__ == "__main__":
    execute_data_ingestion_flow()

    # TODO: to get only applications that need to be processed instead of all the applications # pylint: disable=W0511
    application_ids = get_application_ids()
    # use the following approach if you want to specify the
    # application id manually
    # application_ids = [1]

    for app_id in application_ids:
        execute_main_processing_flow(app_id)
