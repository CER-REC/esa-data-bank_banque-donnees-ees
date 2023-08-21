from collections import defaultdict
import pandas as pd

from src.util.pdf_page.pdf_page import PdfPageTextColumn
from src.util.database_connection import schema, engine
from src.util.process_text import clean_text_content
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def clean_pdf_page_text(pdf_id, page_rotation_degree=0):
    """
        This function takes pdf id and page rotation as inputs. It retrieves the corresponding raw text and cleans the
        text. It returns a dict with page numbers as the keys and the clean text as the values.
    """
    raw_text_col = PdfPageTextColumn.RAW_ROTATED90_TEXT.value if page_rotation_degree == 90 \
        else PdfPageTextColumn.RAW_TEXT.value

    with ExceptionHandler("Error executing select sql statement to get application ids"), engine.begin() as conn:
        # step 1 - get pdf page number and raw text from the database
        query = f"select PageNumber, {raw_text_col} from {schema}.PdfPage where PdfId = {pdf_id};"
        page_data = pd.read_sql(query, conn)

    n_rows, _ = page_data.shape
    with ExceptionHandler(f"No pages found in PdfId - {pdf_id}"):
        if n_rows <= 0:
            raise ValueError(f"No pages found in PdfId - {pdf_id}")

    # step 2 - go through each page and clean content
    page_clean_text_dict = defaultdict(str)
    for _, row in page_data.iterrows():
        page_num, content = row["PageNumber"], row[raw_text_col]
        with ExceptionHandler(f"{raw_text_col} not extracted on Page - {page_num}, PdfId - {pdf_id}"):
            if content is None:
                raise ValueError(f"{raw_text_col} not extracted on Page - {page_num}, PdfId - {pdf_id}")
            page_clean_text_dict[page_num] = clean_text_content(content,
                                                                lower_case=True,
                                                                email=True,
                                                                special_character=True,
                                                                trailing_whitespace=True,
                                                                extra_whitespace=True)

    return page_clean_text_dict
