from enum import Enum
import re
from collections import defaultdict
import pandas as pd

from src.util.database_connection import schema, engine
from src.util.process_text import remove_empty_lines, clean_text_content
from src.functions.extract_TOCs.upsert_tocs import upsert_tocs
from src.util.exception_and_logging.handle_exception import ExceptionHandler


toc_pattern = re.compile(r"(?im)^(?! *LIST OF\b)(?! *Table of contents\b)(.+?\n?.*?\n?.*?)\.{2,}(.*)$")


class TOCType(Enum):
    """ Enum for TOC Type """
    NO_TYPE = "None"
    FIGURE = "Figure"
    TABLE = "Table"
    PLATE = "Plate"
    ATTACHMENT = "Attachment"
    DETAIL = "Detail"
    DRAWING = "Drawing"
    PHOTOGRAPH = "Photograph"
    PHOTO = "Photo"
    SHEET = "Sheet"
    TABLEAU = "Tableau"
    INDEX = "Index"
    OVERVIEW = "Overview"


def extract_tocs(pdf_id):
    """
    This function is to extract all the Table of Content items from all the pages of one pdf, given the pdf_id.
    """
    # Get all pages with page text of this pdf
    with ExceptionHandler("Error querying PdfPageId and RawText"), engine.begin() as conn:
        query = f"SELECT PdfPageId, RawText from {schema}.PdfPage WHERE PdfId = {pdf_id};"
        df_page_text = pd.read_sql(query, conn)

    # Iterate every page and extract Table of Content items
    toc_dict = defaultdict(list)
    for _, row in df_page_text.iterrows():
        page_text = remove_empty_lines(row["RawText"])

        with ExceptionHandler(f"RawText is null on PdfPageId - {row['PdfPageId']}"):
            if page_text is None:
                raise ValueError(f"RawText is null on PdfPageId - {row['PdfPageId']}")

        tocs = re.findall(toc_pattern, page_text)
        count = 0
        for toc in tocs:
            # An example toc: ('Table 4.1 Land Cover in the LAA and RAA ', ' 4.3 ')
            title = clean_text_content(toc[0], extra_whitespace=True, trailing_whitespace=True)

            # An example title: Table 4.2 Ecological Communities of Management Concern
            # We will extract the first word from the title as the content type
            content_type = title.split(" ", 1)[0] if " " in title else TOCType.NO_TYPE.value

            if content_type.lower() in [toc_type.value.lower() for toc_type in TOCType]:
                toc_dict["PdfPageId"].append(row["PdfPageId"])
                toc_dict["OrderNumber"].append(count)
                toc_dict["ContentType"].append(content_type.capitalize())
                toc_dict["ContentTitle"].append(title)
                count += 1

    if not toc_dict:
        # Update TOCItemExtracted to 1 after TOC extraction, though no TOCs are found
        with ExceptionHandler(f"Error updating TOCItemExtracted column in Pdf table for PdfId - {pdf_id}"), \
                engine.begin() as conn:
            conn.exec_driver_sql(f"UPDATE {schema}.Pdf SET TOCItemExtracted = 1 WHERE PDFId = {pdf_id};")
        return

    upsert_tocs(pdf_id, toc_dict)
