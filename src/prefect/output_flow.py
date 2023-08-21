from prefect import flow

from src.prefect.flows.output_files_generation import execute_internal_dataset_generation_flow
from src.prefect.flows.output_files_generation import execute_external_dataset_generation_flow
from src.prefect.flows.create_thumbnail import execute_create_thumbnail_flow
from src.util.process_applications import get_application_ids, check_empty_ik_content
# we first need to execute the translation flows before generating output files
# to conduct translation:
# 1) run execute_creating_translation_file_flow flow
# 2) send the file produced from step 1 to the translation team
# 3) after receiving translation results, run execute_loading_translation_flow(filepath) flow

@flow(name="generate output files")
def execute_output_flow(application_id):
    """
    After translation is done, run this flow to generate internal, external datasets in English and French
    """

    # check if there exist a content for which the classification task 
    # is not performed [hint: 'ContainsIk' field in 'Content' table would be NULL]
    # raise an error if even a single content exist 
    check_empty_ik_content(application_id)

    execute_create_thumbnail_flow(application_id)
    execute_internal_dataset_generation_flow(application_id)

    execute_external_dataset_generation_flow()


if __name__ == "__main__":

    application_ids = get_application_ids()
    # use the following approach if you want to specify the
    # application id manually
    # application_ids = [1]

    for app_id in application_ids:
        execute_output_flow(app_id)
