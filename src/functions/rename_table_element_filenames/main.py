import pandas as pd
from src.util.database_connection import engine, schema
from src.util.process_text import clean_text_content
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.temp_table import get_temp_table_name
from src.functions.create_output_files.language import Language


def _compose_filename(row):
    return (row["ApplicationNameAbbrev"] +
            "_" + clean_text_content(row["Title"], lower_case=True, special_character=True, extra_whitespace=True,
                                     trailing_whitespace=True).replace(" ", "-")[:50] +
            "_pt-" + str(row["NewOrder"]) +
            "_pg-" + str(row["PageNumber"]) +
            "_num-du-doc-" + str(row["RegdocsDataId"]))


def rename_table_element_filenames(pdf_id, language=Language.EN):
    """
    This function updates the FileName column of the DB Table TableElement

    Args:
        pdf_id (integer): pdf id number
        language (Language): to indicate to rename FileName or FrenchFileName

    """
    # query table elements with columns needed for composing file names
    # NewOrder values reflect the orders of table elements with the same title on the same page
    title_column = "FrenchTitle" if language == Language.FR.value else "Title"
    filename_column = "FrenchFileName" if language == Language.FR.value else "FileName"

    query = f"""
        SELECT te.TableElementId
            , a.ApplicationNameAbbrev
            , c.{title_column} AS Title
            , pp.PageNumber
            , p.RegdocsDataId  
            , ROW_NUMBER() OVER (PARTITION BY PageNumber, Title ORDER BY ct.OrderNumber) AS NewOrder
        FROM {schema}.TableElement te 
            LEFT JOIN {schema}.Content c ON te.TableElementId = c.ContentId
            INNER JOIN {schema}.PdfPage pp ON te.PdfPageId = pp.PdfPageId AND pp.PdfId = {pdf_id}
            LEFT JOIN {schema}.CamelotTable ct ON te.CamelotTableId = ct.CamelotTableId
            LEFT JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId
            LEFT JOIN {schema}.Application a ON p.ApplicationId = a.ApplicationId
        ;
    """

    with ExceptionHandler(f"Error executing sql with PdfId - {pdf_id}"), engine.begin() as conn:
        df_table_info = pd.read_sql(query, conn)

    if df_table_info.empty:
        return
    
    # Compose FileName
    df_table_info["FileName"] = df_table_info.apply(_compose_filename, axis=1)

    temp_table_name = get_temp_table_name()
    with ExceptionHandler(f"Error updating FileName of TableElement for PdfId - {pdf_id}"), engine.begin() as conn:
        # create a temp table
        df_table_info[["TableElementId", "FileName"]]\
            .to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        # update FileName in TableElement with data in tmp table
        conn.exec_driver_sql(f"""
            UPDATE {schema}.TableElement
            SET TableElement.{filename_column} = tmp.FileName
            FROM {schema}.{temp_table_name} tmp
            WHERE TableElement.TableElementId = tmp.TableElementId;
        """)

        # delete the temp table from the database
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
