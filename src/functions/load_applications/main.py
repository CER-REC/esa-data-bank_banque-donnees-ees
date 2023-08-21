import os
import pandas as pd

from src.util.check_input_csv import check_input_csv
from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def load_applications():
    """
    This function is to read the input csv file and upsert application attributes to database table
    """
    with ExceptionHandler("Error accessing the input csv file"):
        df_csv = pd.read_csv(os.getenv("INPUT_CSV_FILE_PATH"))

    columns = ["Application ID", "application_name", "Application Short Name", "Application Name Abbrev",
               "Application Filing Date", "Application Type", "Application URL", "Company Name", "Commodity",
               "Decision URL", "Hearing Order", "Pipeline Location", "Pipeline Status"]

    check_input_csv(df_csv, columns)

    df_application = df_csv[columns].drop_duplicates()

    # Rename the columns to the corresponding Application table columns
    df_application = df_application.rename(columns={
        "Application ID": "RTSApplicationId",
        "application_name": "ApplicationName",
        "Application Short Name": "ApplicationShortName",
        "Application Name Abbrev": "ApplicationNameAbbrev",
        "Application Filing Date": "ApplicationFilingDate",
        "Application Type": "ApplicationType",
        "Application URL": "ApplicationURL",
        "Company Name": "CompanyName",
        "Commodity": "Commodity",
        "Decision URL": "DecisionURL",
        "Hearing Order": "HearingOrder",
        "Pipeline Location": "PipelineLocation",
        "Pipeline Status": "PipelineStatus"})

    # name the temporary table
    application_temp_table_name = get_temp_table_name()
    
    with ExceptionHandler("Error upserting sql statement during load applications"), engine.begin() as conn:

        # step 1 - insert application dataframe to a temporary table in the database
        df_application.to_sql(application_temp_table_name, schema=schema, con=conn, index=False,
                              if_exists="replace")

        # step 2 - merge temp table into Application table
        conn.exec_driver_sql(
            f'''
            MERGE {schema}.Application AS Target
            USING {schema}.{application_temp_table_name} AS Source
            ON Target.RTSApplicationId = Source.RTSApplicationId
            
            /* insert new application rows */
            WHEN NOT MATCHED BY Target THEN
                INSERT (RTSApplicationId, 
                        ApplicationName, 
                        ApplicationShortName, 
                        ApplicationNameAbbrev, 
                        ApplicationFilingDate, 
                        ApplicationType, 
                        ApplicationURL, 
                        CompanyName, 
                        Commodity, 
                        DecisionURL, 
                        HearingOrder, 
                        PipelineLocation, 
                        PipelineStatus)
                VALUES (Source.RTSApplicationId, 
                        Source.ApplicationName, 
                        Source.ApplicationShortName,
                        Source.ApplicationNameAbbrev, 
                        Source.ApplicationFilingDate, 
                        Source.ApplicationType, 
                        Source.ApplicationURL, 
                        Source.CompanyName, 
                        Source.Commodity, 
                        Source.DecisionURL, 
                        Source.HearingOrder,
                        Source.PipelineLocation, 
                        Source.PipelineStatus)

            /* update existing application columns */
            WHEN MATCHED
                AND (ISNULL(Target.ApplicationName, '') <> ISNULL(Source.ApplicationName, '') 
                OR ISNULL(Target.ApplicationShortName, '') <> ISNULL(Source.ApplicationShortName, '')
                OR ISNULL(Target.ApplicationNameAbbrev, '') <> ISNULL(Source.ApplicationNameAbbrev, '')
                OR ISNULL(Target.ApplicationFilingDate, '') <> ISNULL(Source.ApplicationFilingDate, '')
                OR ISNULL(Target.ApplicationType, '') <> ISNULL(Source.ApplicationType, '')
                OR ISNULL(Target.ApplicationURL, '') <> ISNULL(Source.ApplicationURL, '')
                OR ISNULL(Target.CompanyName, '') <> ISNULL(Source.CompanyName, '')
                OR ISNULL(Target.Commodity, '') <> ISNULL(Source.Commodity, '')
                OR ISNULL(Target.DecisionURL, '') <> ISNULL(Source.DecisionURL, '')
                OR ISNULL(Target.HearingOrder, '') <> ISNULL(Source.HearingOrder, '')
                OR ISNULL(Target.PipelineLocation, '') <> ISNULL(Source.PipelineLocation, '')
                OR ISNULL(Target.PipelineStatus, '') <> ISNULL(Source.PipelineStatus, '')) THEN
                UPDATE SET 
                ModifiedDateTime = GETDATE()
                , Target.ApplicationName = Source.ApplicationName
                , Target.ApplicationShortName = Source.ApplicationShortName
                , Target.ApplicationNameAbbrev = Source.ApplicationNameAbbrev                
                , Target.ApplicationFilingDate = Source.ApplicationFilingDate
                , Target.ApplicationType = Source.ApplicationType
                , Target.ApplicationURL = Source.ApplicationURL
                , Target.CompanyName = Source.CompanyName
                , Target.Commodity = Source.Commodity
                , Target.DecisionURL = Source.DecisionURL
                , Target.HearingOrder = Source.HearingOrder                    
                , Target.PipelineLocation = Source.PipelineLocation       
                , Target.PipelineStatus = Source.PipelineStatus             
            ;'''
        )

        # step 3 - delete temp table from the database
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{application_temp_table_name}")
