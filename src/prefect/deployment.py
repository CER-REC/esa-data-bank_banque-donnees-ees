from prefect.deployments import Deployment
# from src.prefect.flows.data_ingestion import execute_data_ingestion_flow
# from src.prefect.flows.data_preprocessing import execute_preprocessing_flow
# from src.prefect.flows.table_extraction import execute_table_extraction_flow
# from src.prefect.flows.figure_extraction import execute_figure_extraction_flow
# from src.prefect.flows.alignment_sheet_extraction import execute_alignment_sheet_extraction_flow
# from src.prefect.flows.content_classification import execute_content_classification_flow
from src.prefect.main_flow import execute_main_processing_flow


deployment = Deployment.build_from_flow(
    flow=execute_main_processing_flow,
    name="main_processing_flow",
    version=1, 
    work_queue_name="default"
)

if __name__ == "__main__":
    deployment.apply()
