import shutil
from pathlib import Path

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.functions.create_output_files.internal.helper import get_table_elements, get_table_element_groups, \
    create_csv_files, create_zip_folder
from src.functions.create_output_files.columns import common_column_map_en, common_column_map_fr
from src.functions.create_output_files.readme_files import table_readme_filepath_en, table_readme_filepath_fr
from src.functions.create_output_files.folders import download_folder_internal_en_tables, \
    download_folder_internal_fr_tables
from src.functions.create_output_files.language import Language


def create_table_download_zip_folders(application_id, language=Language.EN.value):
    """
        This function creates all the table download zip folders for the given application id
        The created zip folders are stored in output_directory/internal/en/tables or output_directory/internal/fr/tables
        folder. Each zip folder includes one or multiple table element csv files of one table element group and a readme
        file with the metadata for the table element group
    """
    df_table_element_groups = get_table_element_groups(application_id, language)
    df_table_elements = get_table_elements(application_id, language)

    # We only create zip folders for users to download for tables marked as good quality
    df_good_table_element_groups = df_table_element_groups[df_table_element_groups["HasGoodQualityTable"] == 1]
    df_good_table_elements = df_table_elements[df_table_elements["TableElementGroupId"].isin(
        df_good_table_element_groups["TableElementGroupId"].tolist())]

    # Create csv files of all the good quality table elements in output_directory/internal/en/tables folder or
    # output_directory/internal/fr/tables folder
    download_folder_tables = download_folder_internal_fr_tables if language == Language.FR.value else \
        download_folder_internal_en_tables
    if not download_folder_tables.exists():
        download_folder_tables.mkdir(parents=True)
    create_csv_files(df_good_table_elements, download_folder_tables)

    # Iterate over the table element groups and create a zip folder for each group
    readme_file_column_map = common_column_map_fr if language == Language.FR.value else common_column_map_en
    readme_filepath = table_readme_filepath_fr if language == Language.FR.value else table_readme_filepath_en
    readme_filename = "lisezmoi.txt" if language == Language.FR.value else "readme.txt"
    for _, row in df_good_table_element_groups.iterrows():
        table_element_group_id = row["TableElementGroupId"]

        table_file_items = []  # stores a list of (original filepath, filename) pairs for files in table zip folder

        # Copy a readme file sample to the tables folder
        tmp_table_readme_filepath = download_folder_tables.joinpath(f"readme_{table_element_group_id}.txt")
        with ExceptionHandler(f"Error copying files from {readme_filepath} to {tmp_table_readme_filepath}"):
            shutil.copy(readme_filepath, tmp_table_readme_filepath)

        # Add metadata lines to the end of the readme file
        metadata = ""
        for key, value in readme_file_column_map.items():
            metadata += f"{value}: {row[key]}\n"
        with ExceptionHandler(f"Error updating content in file {tmp_table_readme_filepath}"),\
                open(tmp_table_readme_filepath, "a", encoding="utf-8") as file:
            file.write(metadata)

        table_file_items.append((tmp_table_readme_filepath, readme_filename))

        # Get the list of all the csv files that need to be included in the zip folder
        csv_file_items = df_good_table_elements.loc[
            df_good_table_elements["TableElementGroupId"] == table_element_group_id, "CSVFilePath"].tolist()
        csv_file_items = [(path, path.name) for path in csv_file_items]
        table_file_items.extend(csv_file_items)

        # Create a zip folder with all the csv files and the readme file enclosed
        # row["TableDownloadPath"] is like "/tables/ngtl_table-9-10-comparison-pt-1_pg-82_num-du-doc-4166219.zip"
        table_zip_folder_filepath = download_folder_tables.joinpath(Path(row["TableDownloadPath"]).name)
        create_zip_folder(table_zip_folder_filepath, table_file_items)
