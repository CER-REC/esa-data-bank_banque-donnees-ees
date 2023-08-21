import pandas as pd

from src.util.database_connection import schema, engine
from src.util.temp_table import get_temp_table_name
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def load_translation(filepath):
    """
    This function populates or updates the French columns with the translation results in a csv file, whose filepath is
    the input to this function
    """
    with ExceptionHandler(f"Error reading translation file - {filepath}"):
        df_translation = pd.read_csv(filepath, encoding="utf-8")

    # check if the translation file has the required columns
    with ExceptionHandler(f"Missing required column(s) in the translation file - {filepath}"):
        for col in ("EnglishText", "FrenchTranslation"):
            if col not in df_translation.columns:
                raise ValueError(f"Missing column - {col} - in the translation file - {filepath}")

    # check if there are multiple French translations for the same EnglishText
    df_translation_count = df_translation["EnglishText"].value_counts()\
        .reset_index().rename(columns={"index": "EnglishText", "EnglishText": "count"})
    with ExceptionHandler(f"Multiple French translations for the same EnglishText in translation file - {filepath}"):
        if (df_translation_count["count"] > 1).sum() > 0:
            raise ValueError(f"Multiple French translations for the same EnglishText in translation file - {filepath}")

    temp_table_name = get_temp_table_name()

    with ExceptionHandler("Error loading translation into database"), engine.begin() as conn:
        # insert the translation results into a temporary table in the database
        df_translation[["EnglishText", "FrenchTranslation"]]\
            .to_sql(temp_table_name, schema=schema, con=conn, index=False, if_exists="replace")

        for table_name, english_col, french_col in \
                [("Content", "Title", "FrenchTitle"),
                 ("Pdf", "ESASections", "ESASectionsFrench"),
                 ("Application", "ApplicationName", "ApplicationNameFrench"),
                 ("Application", "ApplicationShortName", "ApplicationShortNameFrench")]:
            # update the French col value in the table by matching the English col value to the translation table
            conn.exec_driver_sql(f"""
                MERGE {schema}.{table_name} AS Target
                USING {schema}.{temp_table_name} AS Source 
                ON Target.{english_col} = Source.EnglishText
                
                WHEN MATCHED THEN
                UPDATE SET Target.{french_col} = Source.FrenchTranslation;
            """)

        # delete the temp table from the database
        conn.exec_driver_sql(f"DROP TABLE IF EXISTS {schema}.{temp_table_name}")
