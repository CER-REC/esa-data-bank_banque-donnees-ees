import pandas as pd
import numpy as np

from src.functions.label_VCs.upsert_vc_mapping import upsert_vcmapping_table
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.database_connection import engine, schema
from src.util.value_components.calculate_vcs import calculate_vcs_count
from src.util.exception_and_logging.process_logs import berdi_logger


def add_strings(str1, str2):
    """
        This function concatenates two strings and if one or both are any
        data type other than string they will be converted to string first.

        Args:
            str1 (string): first string; title
            str2 (string): second string; json text
    """
    if isinstance(str1, str) and isinstance(str2, str):
        return f"{str1} {str2}"
    str1 = "" if isinstance(str1, float) and np.isnan(str1) else str(str1)
    str2 = "" if isinstance(str2, float) and np.isnan(str2) else str(str2)
    return f"{str1} {str2}"


def label_vcs(pdf_id):
    """
        This function extracts the vcs and their count from the table text (including table final title),
        and from figure and alignment sheet titles and upserts the extracted data in
        ContentValueComponentMapping table

        Args:
            pdf_id (integer): pdf id number
    """
    query = f"""
        SELECT c.ContentId
            , ct.JsonText
            , c.Title
        FROM {schema}.Content c
            INNER JOIN {schema}.PdfPage pp ON c.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            LEFT JOIN {schema}.TableElement te ON te.TableElementId = c.ContentId
            LEFT JOIN {schema}.CamelotTable ct ON te.CamelotTableId = ct.CamelotTableId;
    """

    with ExceptionHandler(f"Error executing sql with PdfId - {pdf_id}"), engine.begin() as conn:
        df_content_text = pd.read_sql(query, conn)
    
    if df_content_text.empty:
        berdi_logger.log_info(f"No content found for VC calculation for PdfId - {pdf_id}")
        return
    
    df_content_text["ContentText"] = df_content_text\
        .apply(lambda row: add_strings(row["Title"], row["JsonText"]), axis=1)

    vcs_data = calculate_vcs_count(df_content_text, "ContentText")
    upsert_vcmapping_table(pdf_id, vcs_data)
