from datetime import datetime
import pandas as pd

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.database_connection import engine, schema
from src.functions.create_output_files.folders import root_folder

# There are three types of text in terms of translation
# 1) Text values that are to be translated by looking up in the generic translation database table
# 2) For values that are to be translated by the translation team, where we have corresponding translation columns in
# the database tables
# 3) The columns that can be translated within python code
# The functions in this file mainly prepare translation for type 2)


def _update_french_title():
    """
    Before we compose a list of English titles to be translated by the translation team, we will try to find the values
    for FrenchTitle, if not populated yet, by finding matches from the existing FrenchTitle in the Content table
    """
    with ExceptionHandler("Error updating FrenchTitle in Content table"), engine.begin() as conn:
        conn.exec_driver_sql(f"""
            UPDATE {schema}.Content 
            SET Content.FrenchTitle = tmp.FrenchTitleTarget
            FROM (
                SELECT c1.ContentId, c2.FrenchTitle as FrenchTitleTarget 
                FROM {schema}.Content c1
                    INNER JOIN (
                        SELECT DISTINCT Title, FrenchTitle 
                        FROM {schema}.Content 
                        WHERE FrenchTitle IS NOT NULL
                    ) c2 
                    ON c1.Title = c2.Title
                WHERE c1.FrenchTitle IS NULL
            ) tmp
            WHERE Content.ContentId = tmp.ContentId;
        """)


def _update_french_esa_sections():
    """
    Before we compose a list of text of Esa sections to be translated by the translation team, we will try to find the
    values for ESASectionsFrench, if not populated yet, by finding matches from the existing ESASectionsFrench in the
    Pdf table
    """
    with ExceptionHandler("Error updating ESASectionsFrench in Pdf table"), engine.begin() as conn:
        conn.exec_driver_sql(f"""
             UPDATE {schema}.Pdf 
             SET Pdf.ESASectionsFrench = tmp.ESASectionsFrenchTarget
             FROM (
                 SELECT p1.PdfId, p2.ESASectionsFrench as ESASectionsFrenchTarget 
                 FROM {schema}.Pdf p1
                     INNER JOIN (
                         SELECT DISTINCT ESASections, ESASectionsFrench
                         FROM {schema}.Pdf 
                         WHERE ESASectionsFrench IS NOT NULL
                     ) p2 
                     ON p1.ESASections = p2.ESASections
                 WHERE p1.ESASectionsFrench IS NULL
             ) tmp
             WHERE Pdf.PdfId = tmp.PdfId;
         """)


def _update_french_alignment_sheet_title():
    """
    For Alignment Sheet Titles that are composed using a conversion - 'Alignment Sheet (RegdocsDataId) (PageNumber)'
    we will translate them directly
    """
    with ExceptionHandler("Error updating FrenchTitle for alignment sheets in Content table"), engine.begin() as conn:
        conn.exec_driver_sql(f"""
            UPDATE {schema}.Content
            SET Content.FrenchTitle = tmp.FrenchTitleTarget
            FROM (
                SELECT ContentId
                    , FrenchTitleTarget = 'Carte-tracé ' + CAST(p.RegdocsDataId AS varchar) + ' ' 
                        + CAST(pp.PageNumber AS varchar)
                FROM {schema}.Content c
                    INNER JOIN {schema}.PdfPage pp ON c.PdfPageId = pp.PdfPageId
                    INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId
                WHERE FrenchTitle IS NULL 
                    AND TITLE = 'Alignment Sheet ' + CAST(p.RegdocsDataId AS varchar) + ' ' + CAST(pp.PageNumber AS varchar)
            ) tmp 
            WHERE Content.ContentId = tmp.ContentId;
        """)


def _retrieve_english_text_for_translation():
    """
    This functions retrieves a list of English text to be translated and returns a dataframe with a column - EnglishText
    """
    with ExceptionHandler("Error retrieving English text for translation"), engine.begin() as conn:
        return pd.read_sql(f"""
            SELECT DISTINCT EnglishText
            FROM (
                SELECT Title AS EnglishText
                FROM {schema}.Content
                WHERE FrenchTitle IS NULL
                
                UNION
                SELECT ESASections AS EnglishText
                FROM {schema}.Pdf
                WHERE ESASectionsFrench IS NULL
                
                UNION
                SELECT ApplicationName AS EnglishText
                FROM {schema}.Application
                WHERE ApplicationNameFrench IS NULL
                
                UNION
                SELECT ApplicationShortName AS EnglishText
                FROM {schema}.Application
                WHERE ApplicationShortNameFrench IS NULL
            ) a
            WHERE EnglishText IS NOT NULL AND EnglishText != '';
        """, conn)


def create_translation_file():
    """
    This function orchestrates the steps sequentially to output a csv file with EnglishText column listing the text to
    be translated
    """
    _update_french_title()
    _update_french_esa_sections()
    _update_french_alignment_sheet_title()
    df_translation = _retrieve_english_text_for_translation()

    translation_filepath = root_folder.joinpath(f"translation_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    with ExceptionHandler(f"Error saving file: {translation_filepath}"):
        df_translation.to_csv(translation_filepath,  encoding="utf-8-sig")
