from collections import defaultdict
import fitz
import pandas as pd

from src.functions.extract_block.upsert_block import upsert_block
from src.util.database_connection import engine, schema
from src.util.file_location import get_pdf_file_location
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def extract_block(pdf_id):
    """
        This function extracts all the block data from a pdf document.
    """
    # absolute file path (network shared directory) of the pdf document
    pdf_file_path = get_pdf_file_location(pdf_id)

    # read entire pdf using the PymuPdf library
    with ExceptionHandler(f"Error using PymuPdf library for PdfId - {pdf_id}"):
        pdf = fitz.open(pdf_file_path)

    # mapping between PdfPageId and PageNumber
    # need this information to extract PdfPageId from PageNumber for a given pdf with a PdfId
    query = f"SELECT PdfPageId, PageNumber FROM {schema}.PdfPage WHERE PdfId = {pdf_id}"
    with ExceptionHandler(f"Error executing select sql statement for PdfId - {pdf_id}"), engine.begin() as conn:
        df_page_info = pd.read_sql(query, con=conn, index_col=["PageNumber"])

    block_data = defaultdict(list)

    for page in pdf:
        page_text = page.get_text("dict")

        with ExceptionHandler("Handle missing page numbers for PdfId - {pdf_id}"):
            if (page.number+1) not in df_page_info.index:
                raise ValueError(f"Missing page number in PdfPage for PdfId = {pdf_id}")

        # get PdfPageId from PageNumber
        page_id = df_page_info.loc[page.number+1, "PdfPageId"]

        for ord_num, block in enumerate(page_text["blocks"]):
            bbox_type = block["type"]
            bbox = block["bbox"]

            bbox_x0, bbox_y0, bbox_x1, bbox_y1 = bbox

            if bbox_x0 >= 0 and bbox_x1 >= 0 and bbox_y0 >= 0 and bbox_y1 >= 0:
                bbox_width = bbox_x1 - bbox_x0
                bbox_height = bbox_y1 - bbox_y0
                bbox_area = bbox_width * bbox_height

                block_data["PdfPageId"].append(page_id)
                # order_num refers to a number that includes both valid and invalid blocks
                # for further computation in other sections the only aspect that matters is
                # that these values are in increasing order like 1, 3, 5 etc.
                # also missing numbers in the sequence can help identify the invalid blocks
                block_data["OrderNumber"].append(ord_num)
                block_data["BboxArea"].append(bbox_area)
                block_data["IsImage"].append(bbox_type)

    # update the block table
    upsert_block(pdf_id, block_data)
