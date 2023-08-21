import pandas as pd
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def get_application_ids():
    """
        This function returns application ids for all applications

        Parameters
        --------------
        None

        Returns
        --------------
        application ids as a list of string values

    """
    query = f"""SELECT ApplicationId FROM {schema}.Application; """
    with ExceptionHandler("Error executing select sql statement to get application ids"), engine.begin() as conn:
        applications = pd.read_sql(query, conn)
        return applications["ApplicationId"].tolist()
    

def get_pdf_ids(application_id):
    """
        This function returns pdf ids for a specific application

        Parameters
        --------------
        application_id: application_id

        Returns
        --------------
        pdf ids as a list of string values

    """
    query = f"""SELECT PdfId FROM {schema}.Pdf WHERE ApplicationId = {application_id};"""
    with ExceptionHandler(f"Error executing select sql statement to pdf for application id - {application_id}"), \
        engine.begin() as conn:
        applications = pd.read_sql(query, conn)
        return applications["PdfId"].tolist()
    
def get_pdf_status(pdf_id):
    """
        This function returns pdf status for a specific pdf

        Parameters
        --------------
        pdf_id: id of a pdf document

        Returns
        --------------
        a dictionary with keys in the following order:
            PageTextExtracted 
            RotatedPageTextExtracted
            CamelotTableExtracted
            BlockExtracted
            PageMetadataExtracted
            ContainsIK
            HasGoodQualityTable

    """
    statuses = ["is_page_text_extracted",
                "is_rotated_page_text_extracted",
                "is_camelot_table_extracted",
                "is_block_extracted",
                "is_toc_item_extracted",
                "is_page_metadata_extracted",
                "contains_ik",
                "has_good_quality_table"]
    pdf_status = {status: False for status in statuses}
    
    query = f"""
                SELECT  PageTextExtracted, 
                        RotatedPageTextExtracted, 
                        CamelotTableExtracted,
                        BlockExtracted,
                        TOCItemExtracted,
                        PageMetadataExtracted,
                        ContainsIK,
                        HasGoodQualityTable
                FROM {schema}.Pdf WHERE PdfId = {pdf_id};"""
    with ExceptionHandler(f"Error executing select sql statement to get pdf status for PdfId id - {pdf_id}"), \
        engine.begin() as conn:
        df_status = pd.read_sql(query, conn)
    
    pdf_status["is_page_text_extracted"] = df_status.loc[0, "PageTextExtracted"]
    pdf_status["is_rotated_page_text_extracted"] = df_status.loc[0, "RotatedPageTextExtracted"]
    pdf_status["is_camelot_table_extracted"] = df_status.loc[0, "CamelotTableExtracted"]
    pdf_status["is_block_extracted"] = df_status.loc[0, "BlockExtracted"]
    pdf_status["is_toc_item_extracted"] = df_status.loc[0, "TOCItemExtracted"]
    pdf_status["is_page_metadata_extracted"] = df_status.loc[0, "PageMetadataExtracted"]
    pdf_status["contains_ik"] = df_status.loc[0, "ContainsIK"]
    pdf_status["has_good_quality_table"] = df_status.loc[0, "HasGoodQualityTable"]
    return pdf_status

def check_empty_ik_content(application_id):
    """
        This function returns whether a

        Parameters
        --------------
        application_id: application id of the application to be processed 

        Returns
        --------------
        None

    """
    query = f'''
        SELECT COUNT(*) as count
        FROM {schema}.Content ct
        INNER JOIN {schema}.PdfPage pg ON pg.PdfPageId = ct.PdfPageId
        INNER JOIN {schema}.Pdf pd ON pd.PdfId = pg.PdfId AND pd.ApplicationId = {application_id}
        WHERE ct.ContainsIK IS NULL;
    '''
    with ExceptionHandler(f"Error querying Pdf with ApplicationId - {application_id}"), engine.begin() as conn:
        df_count = pd.read_sql(query, conn)

    with ExceptionHandler(f"Not all contents with ApplicationId - {application_id} have processed IK contents"):
        if df_count.shape[0] < 1 or df_count.iloc[0]["count"] > 0:
            # if the count of contents that haven't had labels for ik, raise an error
            raise ValueError(f"ContainsIk field in the Content table is null for ApplicationId - {application_id}")
