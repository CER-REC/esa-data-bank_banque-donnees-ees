from prefect.deployments import Deployment
from src.prefect.flows.data_ingestion import execute_data_ingestion_flow
from src.prefect.main_flow import execute_main_processing_flow
from src.prefect.flows.translation import execute_creating_translation_file_flow, execute_loading_translation_flow
from src.prefect.output_flow import execute_output_flow

if __name__ == "__main__":

    deployments = [
        {
            "order": 1,
            "name": "ingest data",
            "flow": execute_data_ingestion_flow
        },
        {
            "order": 2,
            "name": "process main section",
            "flow": execute_main_processing_flow
        },
        {
            "order": 3,
            "name": "prepare translation file to be sent",
            "flow": execute_creating_translation_file_flow
        },
        {
            "order": 4,
            "name": "load translated file in the database",
            "flow": execute_loading_translation_flow
        },
        {
            "order": 5,
            "name": "generate output files",
            "flow": execute_output_flow
        }
    ]
    
    for deployment in deployments:
        Deployment.build_from_flow(
            flow=deployment['flow'],
            name=f"step_{deployment['order']}_{deployment['name']}"
        ).apply()
