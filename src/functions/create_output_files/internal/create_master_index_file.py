import pandas as pd

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.exception_and_logging.process_logs import berdi_logger
from src.functions.create_output_files.internal.helper import get_table_element_groups, \
    get_figures_and_alignment_sheets, get_value_components_for_figures_and_alignment_sheets, \
    get_value_components_for_table_element_groups
from src.functions.create_output_files.columns import common_column_map_en, master_index_column_map_en, \
    value_component_column_map_en, common_column_map_fr, master_index_column_map_fr, value_component_column_map_fr
from src.functions.create_output_files.folders import download_folder_internal_en, download_folder_internal_fr
from src.functions.create_output_files.language import Language


def _update_alignment_sheet_title(text, prefix):
    if not isinstance(text, str):
        # if the text data type is not str, return prefix text
        return prefix
    if not text.lower().startswith(prefix.lower()):
        # if the text does not start with the prefix, add the prefix at the beginning
        return f"({prefix}) {text}"
    return text


def create_master_index_file(application_id, language=Language.EN.value):
    """
        This function creates the master index file for an application
    """
    df_table_element_groups = get_table_element_groups(application_id, language)
    df_figures_alignment_sheets = get_figures_and_alignment_sheets(application_id, language)
    df_vc_table_element_groups = get_value_components_for_table_element_groups(application_id)
    df_vc_figures_alignment_sheets = get_value_components_for_figures_and_alignment_sheets(application_id)

    # concatenate two dataframes with value components for table element groups and figure/alignment sheets
    df_vc = pd.concat([
        df_vc_table_element_groups.merge(df_table_element_groups[["ContentId", "TableElementGroupId"]]),
        df_vc_figures_alignment_sheets])[["ContentId", "ValueComponent", "FrequencyCount"]]

    # pivot the dataframe so each row is a content and each column is a value component
    # the value is the frequency count
    df_vc = df_vc.pivot(index="ContentId", columns="ValueComponent")
    df_vc.columns = df_vc.columns.get_level_values(1)
    df_vc = df_vc.reset_index().fillna(0)
    # make sure all the required value component columns are included
    value_component_column_map = value_component_column_map_fr if language == Language.FR.value else \
        value_component_column_map_en
    df_vc = df_vc.reindex(df_vc.columns.union(list(value_component_column_map.keys()), sort=False), fill_value=0,
                          axis=1)

    # concatenate the dataframes of table element groups and figures/alignment sheets with metadata columns
    # merge the value component columns
    column_map = common_column_map_fr | master_index_column_map_fr | value_component_column_map_fr \
        if language == Language.FR.value \
        else common_column_map_en | master_index_column_map_en | value_component_column_map_en
    df_project = pd.concat([df_table_element_groups, df_figures_alignment_sheets])\
        .merge(df_vc, how="left")\
        .rename(columns=column_map)[list(column_map.values())]
    df_project.fillna(dict.fromkeys(value_component_column_map.values(), 0), inplace=True)

    # If an alignment sheet title does not start with "Alignment Sheet", we manually add it to differentiate the title
    # from a figure title or other title types
    alignment_sheet = "Carte-tracé" if language == Language.FR.value else "Alignment Sheet"
    if alignment_sheet not in df_project[column_map["ContentType"]].unique().tolist():
        berdi_logger.log_warning(f"Updating alignment sheet titles. Default value '{alignment_sheet}' not in "
                                 f"content types. Need to confirm the content type of alignment sheet is correct and "
                                 f"there is no alignment sheet extracted for application id - {application_id}.")

    df_project.loc[df_project[column_map["ContentType"]] == alignment_sheet, column_map["Title"]] = \
        df_project.loc[df_project[column_map["ContentType"]] == alignment_sheet, column_map["Title"]]\
            .apply(lambda x: _update_alignment_sheet_title(x, alignment_sheet))

    # Output the metadata to an index file
    download_folder = download_folder_internal_fr if language == Language.FR.value else download_folder_internal_en
    if not download_folder.exists():
        download_folder.mkdir()
    master_index_filepath = download_folder.joinpath("ESA_website_FRA.csv") if language == Language.FR.value else \
        download_folder.joinpath("ESA_website_ENG.csv")
    with ExceptionHandler(f"Error creating internal master index file {master_index_filepath} for ApplicationId - "
                          f"{application_id}"):
        df_project.to_csv(master_index_filepath, encoding="utf-8-sig", index=False)
