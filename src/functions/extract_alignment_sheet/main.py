# pylint: disable = unused-import
import json
import os
import pandas as pd
import requests
from src.util.database_connection import schema, engine
from src.functions.extract_alignment_sheet.mock_response import send_mock_request
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.exception_and_logging.process_logs import berdi_logger
from src.util.attribute_types import AttributeType
from src.util.content.content_type import ContentType


def get_payload(df_page_metadata: pd.DataFrame):
    """
        takes page metadata for a page in a pdf, create
        the payload required by the alignment sheet service

        Input:
        ------------------
            df_page_metadata: pandas dataframe with the following columns
                PageMetadataId, PdfPageId, AttributeKey, AttributeValue, AttributeType
        
        Returns:
        ------------------
            payload_dict: a dictotionary where key indicates feature name
                and associated value indicates value of the corresponding 
                feature
            page_id_list: a list of integer values indicating page ids
    
    """

    payload_dict = {"value": []}
    page_id_list = []

    for page_id in df_page_metadata.PdfPageId.unique():
        # extract metadata content based on pdf page id 
        df_page_id = df_page_metadata[df_page_metadata.PdfPageId == page_id]

        feature = {}
        for _, row in df_page_id.iterrows():
            if AttributeType.STRING.value == row["AttributeType"]:
                feature[row["AttributeKey"]] = row["AttributeValue"]
            elif AttributeType.INTEGER.value == row["AttributeType"]:
                feature[row["AttributeKey"]] = int(row["AttributeValue"])
            elif AttributeType.FLOAT.value == row["AttributeType"]:
                feature[row["AttributeKey"]] = float(row["AttributeValue"])
            elif AttributeType.BOOLEAN.value == row["AttributeType"]:
                feature[row["AttributeKey"]] = bool(row["AttributeValue"])
        
        payload_dict["value"].append(feature)
        page_id_list.append(int(page_id))

    return payload_dict, page_id_list


def extract_alignment_sheet(pdf_id):
    """
       This function takes pdf_id as a parameter, then it metadata for
       each page separately to detect whether that page contains an 
       alignment sheet using alignment sheet classification service. If an
       alignment sheet is found it populates the 'Content' and 
       'AlignmentSheet' table.

    Input:
    ------------------
        pdf_id integer value
    
    Returns:
    ------------------
        None 
    """

    with ExceptionHandler(f"Error removing existing alignment sheet content for PdfId = {pdf_id}"), \
            engine.begin() as conn:
        remove_stmt = f"""
            DELETE c
            FROM {schema}.Content c 
                INNER JOIN {schema}.PdfPage pp 
                    ON c.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            WHERE Type = '{ContentType.ALIGNMENT_SHEET.value}';
        """
        
        # Execute the SQL UPDATE statement
        conn.exec_driver_sql(remove_stmt)

    with ExceptionHandler(f"Error querying PageMetadata for PdfId = {pdf_id}"), engine.begin() as conn:
        # mapping between PdfPageId and PageNumber
        # need this information to extract PdfPageId from PageNumber for a given pdf with a PdfId
        query = f"""SELECT PageMetadata.*
                    FROM {schema}.PageMetadata AS PageMetadata
                        INNER JOIN {schema}.PdfPage AS PdfPage
                            ON PageMetadata.PdfPageId = PdfPage.PdfPageId
                                AND PdfPage.PdfId = {pdf_id};"""
        df_page_metadata = pd.read_sql(query, con=conn)

    if df_page_metadata.empty:
        # return None if there is no page metadata for alignment sheet classification
        berdi_logger.log_info(f"No PageMetadata to classify alignment sheet on for PdfId - {pdf_id}")
        return

    # get alignment sheet classification url
    url = os.getenv("ALIGNMENT_SHEET_CLASSIFICATION_URL")

    payload_dict, page_id_list = get_payload(df_page_metadata)
    
    # define the payload for the request with input data for the prediction
    # check sample_input.json for the requested input data format
    payload = json.dumps(payload_dict)

    # define the headers for the request
    headers = {'Content-Type': 'application/json'}
    
    # check sample_output.json for the response data format
    with ExceptionHandler(f"Error connecting the alignment sheet classification service " \
                          f"for PdfId - {pdf_id}"):
        # uncomment the following line when the alignment sheet classification service is available
        response = requests.request(method="POST", url=url, headers=headers, data=payload, timeout=5)

        # comment the following line out when the alignment sheet classification service is available
        # response = send_mock_request(method="POST", url=url, headers=headers, data=payload, timeout=5)
    
    if response:
        for index, prediction in enumerate(response.json()["predictions"]):
            if prediction == 1:
                stored_proc = f"""Exec {schema}.PR_Load_AlignmentSheet @intPdgPageId = ?;"""
                with ExceptionHandler(f"Error loading Alignment Sheet for PdfPageId - {page_id_list[index]}"), \
                        engine.begin() as conn:
                    conn.exec_driver_sql(stored_proc, (page_id_list[index],))
