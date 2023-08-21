import json
import pandas as pd
from fuzzywuzzy import fuzz
from src.util.database_connection import schema, engine
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.content.content_type import ContentType
from src.util.content.remove_contents_with_empty_titles import remove_contents_with_empty_titles
from src.functions.extract_final_table_element_title.update_content_title import update_content_title


def extract_final_table_element_title(pdf_id):
    """
        This function updates the Title column of the DB Table 'Content'
        and then delete all the rows of DB Table 'Content' and 'TableElement'
        where Title field is empty 
        
        Params:
        ------------------------------
        pdf_id (integer): pdf Id number

        Returns:
        ------------------------------
        None
    """
    query = f"""
        SELECT te.TableElementId AS ContentId
            , te.TitleTOC
            , te.TitleText
            , cmt.JsonText
            , pp.PageNumber
            , RANK() OVER (PARTITION BY pp.PageNumber ORDER BY cmt.OrderNumber) AS NewOrder
        FROM {schema}.TableElement te 
            LEFT JOIN {schema}.CamelotTable cmt 
                ON te.CamelotTableId = cmt.CamelotTableId
            INNER JOIN {schema}.PdfPage pp 
                ON pp.PdfPageId = cmt.PdfPageId
                    AND pp.PdfId = {pdf_id};
        """
    
    with ExceptionHandler(f"Failed to execute sql statement for PdfId - {pdf_id}"), engine.begin() as conn:
        df_table = pd.read_sql(query, conn)
    
    # no need to proceed if there are no contents 
    if df_table.empty:
        return
    
    # if TitleToc exists, replace final title with TitleToc
    # if TitleToc is null, replace final title with TitleText
    # finally if the final title is also null, replace title with empty string
    df_table["Title"] = df_table["TitleText"].fillna(df_table["TitleTOC"]).fillna("")

    # sort df_table by PageNumber and then OrderNumber
    df_table.sort_values(["PageNumber", "NewOrder"], ignore_index=True, inplace=True)

    prev_title = ""
    prev_cols_list = []

    # fill titles that are continuation of tables
    for index, row in df_table.iterrows():

        # json_data data type is 2D list
        json_data = json.loads(row["JsonText"])
        
        # take the first list item if exist
        cols_list = json_data[0] if len(json_data) > 0 else []
        title = row["Title"]

        # if there is no title for the table
        # or the word 'cont' exist in the title
        if title == "" or "cont" in title.lower():
            cols = ", ".join(cols_list)
            prev_cols = ", ".join(prev_cols_list)
            ratio_similarity = fuzz.token_sort_ratio(cols, prev_cols)
            if not set(prev_cols_list).difference(set(cols_list)) or \
               len(prev_cols_list) == len(cols_list) or ratio_similarity > 89:
                title = prev_title
                df_table.loc[index, "Title"] = title

        prev_title = title
        prev_cols_list = cols_list

    # update the title column of the table 'Content'
    update_content_title(pdf_id, df_table[["ContentId", "Title"]])
    
    # remove records of 'Content' and 'TableElement' if
    # title is empty or ''
    remove_contents_with_empty_titles(pdf_id, ContentType.TABLE_ELEMENT.value)
