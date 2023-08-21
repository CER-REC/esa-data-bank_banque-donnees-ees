from collections import defaultdict
import pandas as pd
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.functions.extract_table_element_title_using_text_matching.upsert_table_element_title_text \
    import upsert_table_element_title_text
from src.util.extract_titles_from_text import TitleType, extract_titles_from_text


def extract_table_element_title_using_text_matching(pdf_id):
    """
        This function updates the TitleText column of the DB Table 'Content'
        
        Params:
        ------------------------------
        pdf_id (integer): pdf Id number

        Returns:
        ------------------------------
        None
    """
    query = f"""
        SELECT te.TableElementId
            , pg.PageNumber
            , ROW_NUMBER() OVER (PARTITION BY pg.PageNumber ORDER BY cmt.OrderNumber) AS NewOrder
            , pg.RawText
            , pg.RawTextRotated90
            , te.TitleText
        FROM {schema}.TableElement te 
            INNER JOIN {schema}.PdfPage pg 
                ON te.PdfPageId = pg.PdfPageId AND pg.PdfId = {pdf_id}
            INNER JOIN {schema}.CamelotTable cmt
                ON te.CamelotTableId = cmt.CamelotTableId; 
    """
    
    with ExceptionHandler(f"Failed to query TableElements for PdfId - {pdf_id}"), engine.begin() as conn:
        df_table = pd.read_sql(query, conn)
    
    # no need to proceed if there are no table elements 
    if df_table.empty:
        return
    
    # to maintain a quick lookup table 
    # for titles located in the same page
    titles_db = defaultdict(list)

    for _, row in df_table.iterrows():
        # check whether titles for the current page is already calculated
        page_number = row["PageNumber"]
        if page_number not in titles_db:
            titles_db[page_number] = extract_titles_from_text(row["RawText"], TitleType.TABLE.value)
            if not titles_db[page_number]:
                # if no titles are extracted from text, try using rotated text to extract titles
                titles_db[page_number] = extract_titles_from_text(row["RawTextRotated90"], TitleType.TABLE.value)

        # update TitleText based on page number and table order number
        order_number = row["NewOrder"]  # order_number value starts from 1
        candidate_table_titles = titles_db[page_number]
        if order_number <= len(candidate_table_titles):
            df_table.loc[(df_table["PageNumber"] == page_number) &
                         (df_table["NewOrder"] == order_number), "TitleText"] = candidate_table_titles[order_number - 1]
        
    df_table.drop(columns=["PageNumber", "NewOrder", "RawText", "RawTextRotated90"], inplace=True)

    if not df_table.empty:
        upsert_table_element_title_text(pdf_id, df_table)
