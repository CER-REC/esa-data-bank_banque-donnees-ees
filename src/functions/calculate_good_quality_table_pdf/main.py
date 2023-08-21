import json
import pandas as pd
import numpy as np
from src.util.database_connection import engine, schema
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.exception_and_logging.process_logs import berdi_logger
from src.functions.calculate_good_quality_table_pdf.update_table_element_good_quality \
    import update_table_element_good_quality


def calculate_good_quality_table_elements(pdf_id):
    """
    This function calculates QA metrics for all TableElementId tagged to the 
    PdfId mentioned in the function argument and updates IsGoodQuality column
    of DB table TableElement.
    """
    with ExceptionHandler(f"Error querying TableElements of PdfId - {pdf_id}"), engine.begin() as conn:
        query = f'''
        SELECT te.TableElementId
            , te.CamelotTableId
            , te.PdfPageId
            , ct.NumberOfRows
            , ct.NumberOfColumns
            , ct.JsonText
            , c.Title 
        FROM {schema}.TableElement te 
            LEFT JOIN {schema}.CamelotTable ct ON te.CamelotTableId = ct.CamelotTableId
            INNER JOIN {schema}.PdfPage pp ON te.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            LEFT JOIN {schema}.Content c ON te.TableElementId = c.ContentId;
        '''
        
        df_table_info = pd.read_sql(query, conn)

    # read in table text and calculate number of null cells and number of cells with 'cid'
    for col in ["csv_null_cell_count", "csv_cid_cell_count"]:
        df_table_info[col] = np.nan
    
    for index, row in df_table_info.iterrows():
        count_null_cell = 0
        count_cid_cell = 0
        for line in json.loads(row["JsonText"]):
            for cell in line:
                if cell == "":
                    count_null_cell += 1
                elif "cid:" in cell:
                    count_cid_cell += 1
        df_table_info.loc[index, "csv_null_cell_count"] = count_null_cell
        df_table_info.loc[index, "csv_cid_cell_count"] = count_cid_cell

    # Calculate qa metrics
    # - qa_single_row_or_col: if a table has only one row or one column
    # - qa_blank_cell_percent: percentage of empty cells in a table
    # - qa_cid_cell_percent: percentage of cells with 'cid:'
    # - qa_duplicate: if this table is a duplicate (there are other tables with the same title on the same pdf page)

    df_table_info["qa_single_row_or_col"] = df_table_info[["NumberOfRows", "NumberOfColumns"]].apply(
        lambda x: x["NumberOfRows"] == 1 or x["NumberOfColumns"] == 1, axis=1
    )
    df_table_info["qa_blank_cell_percent"] = df_table_info[["NumberOfRows", "NumberOfColumns", "csv_null_cell_count"]]\
        .apply(lambda x: round(100 * x["csv_null_cell_count"] / (x["NumberOfRows"] * x["NumberOfColumns"]), 2), axis=1)
    df_table_info["qa_cid_cell_percent"] = df_table_info[["NumberOfRows", "NumberOfColumns", "csv_null_cell_count",
                                                          "csv_cid_cell_count"]].apply(
        lambda x: round(100 * x["csv_cid_cell_count"] / (x["NumberOfRows"] * x["NumberOfColumns"] -
                                                         x["csv_null_cell_count"]), 2), axis=1
    )
    df_table_count = df_table_info.groupby(["Title", "PdfPageId"])["CamelotTableId"].count()\
        .reset_index().rename(columns={"CamelotTableId": "count"})
    df_duplicate = df_table_count[df_table_count["count"] > 1]

    df_table_info = df_table_info.merge(df_duplicate, how="left", on=["Title", "PdfPageId"])
    df_table_info["qa_duplicate"] = df_table_info["count"].notna()
    
    # Check if more than 72% cells are blank and if more than 80% of the cells have cid:
    df_table_info["qa_blank"] = df_table_info["qa_blank_cell_percent"] > 72
    df_table_info["qa_cid"] = df_table_info["qa_cid_cell_percent"] > 80
    
    # If any of the condition is TRUE, then populate IsGoodQuality column with value 0, otherwise 1
    df_table_info["isGoodQuality"] = ~df_table_info[["qa_blank", "qa_cid", "qa_duplicate", "qa_single_row_or_col"]]\
        .any(axis=1)

    update_table_element_good_quality(pdf_id, df_table_info[["TableElementId", "isGoodQuality"]])


def calculate_good_quality_pdf(pdf_id, thresh):
    """
    This function updates the PDF DB Table HasGoodQuality column value to 1 if a PDF
    generated over threshold % (defined by function argument "thresh") of problematic tables and 0 otherwise.

    Args:
        pdf_id (integer): pdf Id number
        thresh (integer): Percentage threshold above which a pdf is to be considered having bad
        quality tables. In case of 20%, just mention the argument value as integer i.e. 20

    """
    with ExceptionHandler(f"Error querying TableElements of PdfId - {pdf_id}"), engine.begin() as conn:
        query = f'''
            SELECT te.IsGoodQuality
                , pp.PdfId 
            FROM {schema}.TableElement te 
                INNER JOIN {schema}.PdfPage pp 
                    ON te.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id};
        '''
        
        df_table_info = pd.read_sql(query, conn)

    if not df_table_info.shape[0]:
        berdi_logger.log_info(f"No TableElements extracted for PdfId - {pdf_id}")
        return

    bad_tables_prob = 100*round((~df_table_info["IsGoodQuality"]).values.sum()/df_table_info.shape[0], 2)

    # We will mark the HasGoodQualityTable column in Pdf table as 0 if the PDF generated over 20% problematic csv files
    with ExceptionHandler(f"Error updating Pdf HasGoodQualityTable column of PdfId - {pdf_id}"), engine.begin() as conn:
        if bad_tables_prob > thresh:
            conn.exec_driver_sql(f'''UPDATE {schema}.Pdf SET HasGoodQualityTable = 0
                                                    WHERE PdfId = {pdf_id};''')
            berdi_logger.log_info(f"PdfId - {pdf_id} has bad quality tables")
        else:
            conn.exec_driver_sql(f'''UPDATE {schema}.Pdf  SET HasGoodQualityTable = 1
                                                    WHERE PdfId = {pdf_id};''')
            berdi_logger.log_info(f"PdfId - {pdf_id} has good quality tables")


def check_good_quality_table_pdf(pdf_id, thresh):
    """
    This function runs functions calculate_good_quality_table_elements(pdf_id) and
    calculate_good_quality_pdf(pdf_id) in a sequential order.

    Args:
        pdf_id (integer): pdf Id number
        thresh (integer): Percentage threshold above which a pdf is to be considered having bad
        quality tables. In case of 20%, just mention the argument value as integer i.e. 20 

    """
    return calculate_good_quality_table_elements(pdf_id), calculate_good_quality_pdf(pdf_id, thresh)
