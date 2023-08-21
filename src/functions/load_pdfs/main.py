import os
import pandas as pd

from src.util.check_input_csv import check_input_csv
from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler

def load_pdfs():
    """
    This function is to read the input csv file and upsert pdf attributes to database table
    """
    with ExceptionHandler("Error accessing the input csv file"):
        df_csv = pd.read_csv(os.getenv("INPUT_CSV_FILE_PATH"))

    columns = ["Application ID", "Data ID", "File Name", "ESA Folder URL", "PDF Download URL",
               "Consultant Name", "ESA Section(s)"]

    check_input_csv(df_csv, columns)

    df_pdf = df_csv[columns].drop_duplicates()

    # Rename the columns to the corresponding Pdf table columns
    df_pdf = df_pdf.rename(columns={
        "Application ID": "RTSApplicationId",
        "Data ID": "RegdocsDataId",
        "File Name": "FileName",
        "ESA Folder URL": "ESAFolderURL",
        "PDF Download URL": "PDFDownloadURL",
        "Consultant Name": "ConsultantName",
        "ESA Section(s)": "ESASections"})

    pdf_temp_table_name = get_temp_table_name()
    
    with ExceptionHandler("Error upserting sql statement during load applications"), engine.begin() as conn:
        
        # step 1 - insert pdf dataframe to a temporary table in the database
        df_pdf.to_sql(pdf_temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # step 2 - merge temp table into Pdf table
        conn.exec_driver_sql(
            f'''
            MERGE {schema}.Pdf AS Target
            USING (
                SELECT ApplicationId, RegdocsDataId, FileName, ESAFolderURL, 
                    PDFDownloadURL, ConsultantName, ESASections 
                FROM {schema}.{pdf_temp_table_name} p LEFT JOIN {schema}.Application a 
                ON p.RTSApplicationId = a.RTSApplicationId
                ) AS Source
            ON Target.RegdocsDataId = Source.RegdocsDataId
            
            /* insert new pdf rows */
            WHEN NOT MATCHED BY Target THEN
                INSERT (ApplicationId, RegdocsDataId, FileName, ESAFolderURL, PDFDownloadURL, 
                    ConsultantName, ESASections)
                VALUES (Source.ApplicationId, Source.RegdocsDataId, Source.FileName, 
                    Source.ESAFolderURL, Source.PDFDownloadURL, Source.ConsultantName, 
                    Source.ESASections)
            
            /* update existing pdf columns */
            WHEN MATCHED 
                AND (ISNULL(Target.FileName, '') <> ISNULL(Source.FileName, '') 
                OR ISNULL(Target.ESAFolderURL, '') <> ISNULL(Source.ESAFolderURL, '')
                OR ISNULL(Target.PDFDownloadURL, '') <> ISNULL(Source. PDFDownloadURL, '')
                OR ISNULL(Target.ConsultantName, '') <> ISNULL(Source.ConsultantName, '')
                OR ISNULL(Target.ESASections, '') <> ISNULL(Source.ESASections, '')) THEN
                UPDATE SET 
                ModifiedDateTime = GETDATE()
                , Target.FileName = Source.FileName
                , Target.ESAFolderURL = Source.ESAFolderURL
                , Target.PDFDownloadURL = Source. PDFDownloadURL
                , Target.ConsultantName = Source.ConsultantName
                , Target.ESASections = Source.ESASections
            ;
            '''
        )
        # step 3 - delete temp table from the database
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{pdf_temp_table_name}")
