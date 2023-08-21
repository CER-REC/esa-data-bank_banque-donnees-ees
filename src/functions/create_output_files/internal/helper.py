import zipfile
import pandas as pd

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.database_connection import engine, schema
from src.functions.create_output_files.language import Language


def _get_language_column_mapping(language):
    if language == Language.FR.value:
        return {
            "Title": "FrenchTitle",
            "ApplicationName": "ApplicationNameFrench",
            "ApplicationShortName": "ApplicationShortNameFrench",
            "ESASections": "ESASectionsFrench",
            "TableElementFileName": "FrenchFileName"
        }
    return {
            "Title": "Title",
            "ApplicationName": "ApplicationName",
            "ApplicationShortName": "ApplicationShortName",
            "ESASections": "ESASections",
            "TableElementFileName": "FileName"
        }


def _translate_generic_expressions(df_content):
    with ExceptionHandler("Error querying translation table in the database"), engine.begin() as conn:
        # query the translation table in the database
        df_generic_translation = pd.read_sql(f"""
                SELECT EnglishExpression, FrenchTranslation
                FROM {schema}.Translation;
            """, conn)

    # get a dictionary of translation, example: {"Table": "Tableau", "Oil", "Pétrole"}
    translation = {row["EnglishExpression"]: row["FrenchTranslation"] for _, row in df_generic_translation.iterrows()}

    # the following columns need to be translated by directly looking up the translation dict
    columns_en = ["ContentType", "Commodity", "ApplicationType", "PipelineStatus"]

    with ExceptionHandler("Missing translation in the translation table"):
        for exp in pd.unique(df_content[columns_en].values.ravel("K")).tolist() \
                   + pd.unique(", ".join(df_content["PipelineLocation"].unique()).split(", ")).tolist():
            # going over the unique values from the columns_en and the PipelineLocation column, and check if the
            # translation is provided. PipelineLocation can be multiple locations joint by ", ";
            # for example: "Alberta, Ontario", so we are extract individual locations from the strings for checking
            # if translation exists
            if exp and exp not in translation:
                raise ValueError(f"Missing translation in the translation table for expression: {exp}")

    # translate by using the translation dictionary
    df_content[columns_en] = df_content[columns_en].replace(translation)
    # translate "PipelineLocation" by splitting into individual locations, translating and then joining back together
    df_content["PipelineLocation"] = df_content["PipelineLocation"] \
        .apply(lambda x: ", ".join([translation[loc] for loc in x.split(", ")]))

    return df_content


def _translate_urls(df_content):
    df_content["PDFDownloadURL"] = df_content["PDFDownloadURL"]\
        .apply(lambda x: x.replace("https://apps.cer-rec.gc.ca/REGDOCS/File/Download/",
                                   "https://apps.cer-rec.gc.ca/REGDOCS/Fichier/Téléchargement/") if isinstance(x, str)
                         else "")
    for col in ["ESAFolderURL", "ApplicationURL", "DecisionURL"]:
        df_content[col] = df_content[col] \
            .apply(lambda x: x.replace("https://apps.cer-rec.gc.ca/REGDOCS/Item/View/",
                                       "https://apps.cer-rec.gc.ca/REGDOCS/Élément/Afficher/") if isinstance(x, str)
                             else "")


def get_table_element_groups(application_id, language=Language.EN.value):
    """
        This function queries all the table element groups of an application and returns a dataframe
    """
    columns = _get_language_column_mapping(language)

    with ExceptionHandler(f"Error querying table element groups for ApplicationId - {application_id}"), \
            engine.begin() as conn:
        df_table_element_groups = pd.read_sql(f"""
            WITH TableElement AS (
                SELECT c.ContentId
                    , te.TableElementGroupId
                    , c.{columns["Title"]} AS Title
                    , ContentType = 'Table'
                    , {columns["ApplicationName"]} AS ApplicationName
                    , {columns["ApplicationShortName"]} AS ApplicationShortName
                    , ApplicationFilingDate
                    , CompanyName
                    , Commodity
                    , p.FileName
                    , ESAFolderURL
                    , PDFDownloadURL
                    , ApplicationType
                    , PipelineLocation
                    , HearingOrder
                    , ConsultantName
                    , PipelineStatus
                    , ApplicationURL
                    , DecisionURL
                    , {columns["ESASections"]} AS ESASections
                    , ApplicationNameAbbrev
                    , te.{columns["TableElementFileName"]} AS TableElementFileName
                    , p.HasGoodQualityTable
                    , pp.PageNumber
                    , ROW_NUMBER() OVER (PARTITION BY TableElementGroupId ORDER BY PageNumber, ct.OrderNumber) 
                        AS NewOrder
                    , p.RegdocsDataId as DataID
                    , ContainsIK = CASE WHEN p.ContainsIK = 1 THEN 1 ELSE c.ContainsIK END 
                    , RTSApplicationId as ApplicationID
                FROM {schema}.TableElement te
                    INNER JOIN {schema}.Content c ON te.TableElementId = c.ContentId
                    INNER JOIN {schema}.PdfPage pp ON te.PdfPageId = pp.PdfPageId
                    INNER JOIN {schema}.CamelotTable ct ON te.CamelotTableId = ct.CamelotTableId
                    INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId 
                    INNER JOIN {schema}.Application a 
                        ON p.ApplicationId = a.ApplicationId AND a.ApplicationId = {application_id}
            ), PageNumber AS  (
                SELECT TableElementGroupId
                    , PDFPageNumber = MIN(PageNumber)
                    , PageCount = COUNT(*)
                    , SUM(CAST(ContainsIK AS INT)) AS IKCount
                FROM TableElement
                GROUP BY TableElementGroupId
            )
    
            SELECT Title
                , ContentType 
                , ApplicationName
                , ApplicationShortName
                , ApplicationFilingDate
                , CompanyName
                , Commodity
                , FileName
                , ESAFolderURL
                , PDFDownloadURL
                , ApplicationType
                , PipelineLocation
                , HearingOrder
                , ConsultantName
                , PipelineStatus
                , ApplicationURL
                , DecisionURL
                , ESASections
                , PDFPageNumber
                , PageCount
                , HasGoodQualityTable
                , ProjectDownloadPath = CASE HasGoodQualityTable WHEN 0 THEN '' 
                                            ELSE '/projects/' + ApplicationNameAbbrev + '.zip' END
                , TableDownloadPath = CASE HasGoodQualityTable WHEN 0 THEN '' 
                                        ELSE '/tables/' + TableElementFileName + '.zip' END
                , ThumbnailLocation = 'thumbnails/' + cast(DataID as varchar) + '_' + cast(PDFPageNumber as varchar) +
                                      '.jpg'
                , IK_Labels = (CASE IKCount WHEN 0 THEN 0 ELSE 1 END)
                , ApplicationID
                , DataID
                , te.TableElementGroupId
                , ContentId
            FROM TableElement te
                LEFT JOIN PageNumber pn ON te.TableElementGroupId = pn.TableElementGroupId
            WHERE NewOrder = 1                                      
            ;                               
            """, conn)

    if language == Language.FR.value:
        # translate other columns
        _translate_generic_expressions(df_table_element_groups)
        _translate_urls(df_table_element_groups)

    return df_table_element_groups


def get_table_elements(application_id, language=Language.EN.value):
    """
        This function queries all the table elements of an application and returns a dataframe with columns:
        TableElementId, TableElementGroupId, TableElementFileName, JsonText
    """
    col_file_name = "FrenchFileName" if language == Language.FR.value else "FileName"
    with ExceptionHandler(f"Error querying table elements for ApplicationId - {application_id}"), \
            engine.begin() as conn:
        return pd.read_sql(f"""
            SELECT TableElementId
                , te.TableElementGroupId
                , te.{col_file_name} as TableElementFileName
                , ct.JsonText
            FROM {schema}.TableElement te                          
                INNER JOIN {schema}.Content c ON te.TableElementId = c.ContentId
                INNER JOIN {schema}.PdfPage pp ON te.PdfPageId = pp.PdfPageId
                INNER JOIN {schema}.CamelotTable ct ON te.CamelotTableId = ct.CamelotTableId
                INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId AND p.ApplicationId = {application_id}
        """, con=conn)


def create_csv_files(df_table_elements, destination_folder):
    """
        This functions receives a dataframe of table elements and create csv files from the text in "JsonText" column
        and name the csv files using the values in "TableElementFileName" column.
        A new column "CSVFilePath" is added to the dataframe indicating the absolute file paths of the created csv
        files. The data type is WindowsPath using Path class from pathlib library
    """
    # create a new column "CSVFilePath" for storing the file path of the csv files; default value is nan
    df_table_elements["CSVFilePath"] = pd.Series(dtype="str")
    for index, row in df_table_elements.iterrows():
        # iterate each table element and create a csv file from "JsonText" where the table content is stored in json
        # format in a text string
        with ExceptionHandler(f"Error reading JsonText for TableElementFileName - {row['TableElementFileName']}"):
            df_table = pd.read_json(row["JsonText"], orient="values")
        # pylint: disable=no-member
        if df_table.shape[0] > 1:
            # use the first row cells as the column names
            df_table = df_table.rename(columns=df_table.iloc[1]).drop(df_table.index[1])
        # pylint: enable=no-member
        csv_filepath = destination_folder.joinpath(row["TableElementFileName"] + ".csv")
        with ExceptionHandler(f"Error creating csv file - {csv_filepath}"):
            df_table.to_csv(csv_filepath, encoding="utf-8-sig", index=False)
        # update the "CSVFilePath" value for the table element
        df_table_elements.loc[index, "CSVFilePath"] = csv_filepath


def create_zip_folder(zip_filepath, file_items):
    """
        This function creates a zip folder with all the file items.
        file_items is a list of (filepath, filename) pairs
    """
    with ExceptionHandler(f"Error creating zip folder - {zip_filepath}"), \
            zipfile.ZipFile(zip_filepath, mode="w") as zip_file:
        for filepath, filename in file_items:
            zip_file.write(filepath, filename, compress_type=zipfile.ZIP_DEFLATED)

    # Delete the files that are already in the zip file
    for filepath, _ in file_items:
        filepath.unlink()


def get_figures_and_alignment_sheets(application_id, language=Language.EN.value):
    """
        This function queries all the figures and alignment sheets of an application and returns a dataframe
    """
    columns = _get_language_column_mapping(language)

    with ExceptionHandler(f"Error querying figures and alignment sheets for ApplicationId - {application_id}"), \
            engine.begin() as conn:
        # not include figures that are also identified as alignment sheets
        df_figures_and_alignment_sheets = pd.read_sql(f"""
            SELECT ContentId
        		, c.{columns["Title"]} AS Title
        		, ContentType =  (CASE c.Type WHEN 'Figure' THEN 'Figure' ELSE 'Alignment Sheet' END)
                , {columns["ApplicationName"]} AS ApplicationName
                , {columns["ApplicationShortName"]} AS ApplicationShortName
        		, ApplicationFilingDate
        		, CompanyName
        		, Commodity
        		, p.FileName
        		, ESAFolderURL
        		, PDFDownloadURL
        		, ApplicationType
        		, PipelineLocation
        		, HearingOrder
        		, ConsultantName
        		, PipelineStatus
        		, ApplicationURL
        		, DecisionURL
                , {columns["ESASections"]} AS ESASections
        		, PageNumber as PDFPageNumber
        		, PageCount = 1
        		, ThumbnailLocation = 'thumbnails/' + CAST(RegdocsDataId AS varchar) + '_' + CAST(PageNumber AS varchar)
        		                        +'.jpg'
        		, RTSApplicationId AS ApplicationID
        		, p.RegdocsDataId AS DataID
        		, IK_Labels = CASE WHEN p.ContainsIK = 1 THEN 1 ELSE c.ContainsIK END
        FROM {schema}.Content c 
        	INNER JOIN {schema}.PdfPage pp ON c.PdfPageId = pp.PdfPageId
        	INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId
        	INNER JOIN {schema}.Application a ON p.ApplicationId = a.ApplicationId AND a.ApplicationId = {application_id}
        WHERE c.Type IN ('Figure', 'AlignmentSheet') 
            AND NOT EXISTS (
                SELECT 1 
                FROM {schema}.AlignmentSheet al
                WHERE c.ContentId = al.FigureId
            );""", conn)

    if language == Language.FR.value:
        # translate other columns
        _translate_generic_expressions(df_figures_and_alignment_sheets)
        _translate_urls(df_figures_and_alignment_sheets)

    return df_figures_and_alignment_sheets


def get_value_components_for_figures_and_alignment_sheets(application_id):
    """
        This function queries all the value components of figures and alignment sheets of an application and returns a
        dataframe
    """
    with ExceptionHandler(f"Error querying value components of figures and alignment sheets for ApplicationId - "
                          f"{application_id}"), engine.begin() as conn:
        # not include figures that are also identified as alignment sheets
        return pd.read_sql(f"""
            SELECT m.ContentId, ValueComponent, FrequencyCount
                FROM {schema}.ContentValueComponentMapping m 
                    LEFT JOIN {schema}.ValueComponent v ON m.ValueComponentId = v.ValueComponentId
                    INNER JOIN {schema}.Content c 
                        ON m.ContentId = c.ContentId AND c.Type in ('Figure', 'AlignmentSheet') AND NOT EXISTS (
                            SELECT 1 
                            FROM {schema}.AlignmentSheet al
                            WHERE c.ContentId = al.FigureId
                        )
                    LEFT JOIN {schema}.PdfPage pp ON c.PdfPageId = pp.PdfPageId
        	        INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId AND p.ApplicationId = {application_id};
            """, conn)

    
def get_value_components_for_table_element_groups(application_id):
    """
        This function queries all the value components of table element groups of an application and returns a dataframe
    """
    with ExceptionHandler(f"Error querying value components of table element groups for ApplicationId - "
                          f"{application_id}"), engine.begin() as conn:
        return pd.read_sql(f"""
                SELECT TableElementGroupId, ValueComponent, SUM(ISNULL(FrequencyCount, 0)) AS FrequencyCount
                FROM {schema}.ContentValueComponentMapping m
                    LEFT JOIN {schema}.ValueComponent v on m.ValueComponentId = v.ValueComponentId
                    LEFT JOIN {schema}.TableElement t ON t.TableElementId = m.ContentId
                    LEFT JOIN {schema}.PdfPage pp ON t.PdfPageId = pp.PdfPageId
        	        INNER JOIN {schema}.Pdf p ON pp.PdfId = p.PdfId AND p.ApplicationId = {application_id}
                GROUP BY t.TableElementGroupId, ValueComponent;
            """, conn)
