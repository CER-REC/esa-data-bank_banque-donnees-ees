# How to use Prefect
----------------------------------------------------------------------------------------

Follow the steps below sequentially to deploy Prefect flows and execute BERDI tasks at 
a scheduled time or repeatedly after some intervals:

1. To run a Prefect server open a new terminal and use the following command:
   > prefect server start

   Visit the Prefect UI at http://127.0.0.1:4200/

3. Before running the deployment at a scheduled time, open a new terminal and
   use the following command to start a prefect agent to process the deployment 
   flows / tasks:
   > prefect agent start -p default-agent-pool

   (-p option indicates the name of the work pool for the flow. more options regarding
   the Prefect deployment commands can be found at 
   https://docs.prefect.io/concepts/deployments/)

4. Create prefect deployment flows using the following command:
   > python -m src.prefect.create_deployment_flows

   Make sure the following line appears in the terminal:-

   Agent started! Looking for work from work pool 'default-agent-pool'...

   Visit Prefect UI at http://127.0.0.1:4200/deployments to customize the deployment.

5. Visit the Prefect UI at http://127.0.0.1:4200/deployments and select the flow that
   needs to be scheduled to run. The step number indicates the order in which the flows 
   need to be executed.

   The following deployment flows are executed in sequence:

   1. data ingestion/step_1_ingest data - (input) not applicable
   2. main processing flow/step_2_process main section - (input) applicaion id [retrieve this
      value from the database]
   3. prepare translation file to be sent to the translation team/step_3_prepare translation file to be sent - (input)
      not applicable [send this file the translation team]
   4. load translation and update FrenchFileName/step_4_load translated file in the database - (input) 
      absolute filepath as a string pointing to the translated file after receiving the file from
      the french translation team.
   5. generate output files/step_5_generate output files - (input) application id


6. Visit http://127.0.0.1:4200/flow-runs to ensure successful run of the selected flow.


# Special instructions about the Prefect
----------------------------------------------------------------------------------------

1. If there is any issue regarding the visualization of flow and task, recommended
   approach is to reset the local Prefect database. Most issues would be automatically
   resolved. Use the following command to reset the database:

   > prefect server database reset -y

2. Prefect deployment can not work when the absolute path to the deployment script
   contains spaces. For example:

   (wrong) C:\CER Projects\BERDI\BERDIDataProcessing
   (correct) C:\BerdiRefactoring\BERDIDataProcessing

   [N.B] Please refer to https://discourse.prefect.io/t/prefect-agent-c-program-is-not-recognized-as-an-internal-or-external-command-on-windows/2127
   where this issue was raised.

3. To use a different port number for Prefect server. Use the following command to set the port number:
   > prefect config set PREFECT_SERVER_API_PORT=4201
   The following command need to be executed everytime the port number is changed:
   > prefect config set PREFECT_API_URL="http://127.0.0.1:4201/api"
