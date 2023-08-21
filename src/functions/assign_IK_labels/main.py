import json
import os
import pandas as pd
import requests
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.process_logs import berdi_logger


THRESHOLD_PDF_IK_PAGE_RATIO = 0.5


def assign_ik_labels(pdf_id):
    """
    This function receives PdfId and parses PdfPage and Content tables to retrieve raw page text,
    IK classification service is called to return the binary result of the prediction. ContainsIK value in the Content
    table gets updated with the prediction result.
    -----
    Input:
        pdf_id integer value
    -----
    Returns:
    -----
        None - updates Content table
    """
    with ExceptionHandler(f"Error querying content table and PdfPage table for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        query = f'''
                SELECT DISTINCT cn.PdfPageId, pg.RawText  
                FROM {schema}.Content cn 
                INNER JOIN {schema}.PdfPage pg ON pg.PdfPageId = cn.PdfPageId AND pg.PdfId = {pdf_id}'''
        df_pdf_page_text = pd.read_sql(query, conn)

    # get raw text from the parsed content table
    raw_text = df_pdf_page_text['RawText'].tolist()

    if not raw_text:
        berdi_logger.log_info(f"No page with text content found for PdfId - {pdf_id}")
        return

    # get API url
    url = os.getenv("IK_CLASSIFICATION_URL")
    # define the payload for the request with input data for the prediction
    payload = json.dumps({"value": raw_text})
    # define the headers for the request
    headers = {'Content-Type': 'application/json'}

    # make a POST request to the API with the input data and headers, and a timeout of 5 seconds
    # example of output JSON response:
    # {   "predictions": [
    #         0
    #     ],
    #     "prediction_probabilities": [
    #         [
    #             0.9419311406222871,
    #             0.05806885937771271
    #         ],
    #     ] }
    with ExceptionHandler("API encountered an error processing the POST request, resulting in an unsuccessful "
                          "response"):
        response = requests.request("POST", url, headers=headers, data=payload, timeout=120)
        # parse the prediction result from the JSON response
        result = response.json()['predictions']

    # update ContainsIK column in the Content table for the corresponding content
    df_pdf_page_text["ContainsIK"] = result
    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error updating ContainsIK column of Content table for PdfId - {pdf_id}"), \
            engine.begin() as conn:
        # create a temp table
        df_pdf_page_text[["PdfPageId", "ContainsIK"]] \
            .to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # update ContainsIK in Content with data in tmp table
        conn.exec_driver_sql(f"""
            UPDATE {schema}.Content
            SET Content.ContainsIK = tmp.ContainsIK
            FROM {schema}.{temp_table_name} tmp
            WHERE Content.PdfPageId = tmp.PdfPageId;
        """)

        # delete the temp table from the database
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")

    if sum(result) / len(result) > THRESHOLD_PDF_IK_PAGE_RATIO:
        # if the ratio of IK pages with content over total number pages with content is over the threshold, mark the pdf
        # as containing IK
        with ExceptionHandler(f"Error updating ContainsIK column of Pdf table for PdfId - {pdf_id}"), \
                engine.begin() as conn:
            conn.exec_driver_sql(f"""
                UPDATE {schema}.Pdf
                SET ContainsIK = 1
                WHERE PdfId = {pdf_id};
            """)
