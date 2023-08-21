import shutil
from pathlib import Path

from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.functions.create_output_files.internal.helper import get_table_elements, get_table_element_groups, \
    create_csv_files, create_zip_folder
from src.functions.create_output_files.columns import common_column_map_en, common_column_map_fr
from src.functions.create_output_files.readme_files import project_readme_filepath_en, project_readme_filepath_fr
from src.functions.create_output_files.folders import download_folder_internal_en_projects, \
    download_folder_internal_fr_projects
from src.functions.create_output_files.language import Language


def create_project_download_zip_folder(application_id, language=Language.EN.value):
    """
        This function creates the project download zip folder for the given application id
        The created zip folder is stored in output_directory/en/projects folder
        The zip folder includes one or multiple table element group zip folders, a readme file and a project index file
        Inside each table element zip folder, there are one or multiple csv files of the table elements
    """
    df_table_element_groups = get_table_element_groups(application_id, language)
    df_table_elements = get_table_elements(application_id, language)

    # We only create zip folders for users to download for tables marked as good quality
    df_good_table_element_groups = df_table_element_groups[df_table_element_groups["HasGoodQualityTable"] == 1]
    df_good_table_elements = df_table_elements[df_table_elements["TableElementGroupId"].isin(
        df_good_table_element_groups["TableElementGroupId"].tolist())]

    # Create csv files of all the good quality table elements in output_directory/internal/en/projects or
    # output_directory/internal/fr/projects folder
    download_folder_projects = download_folder_internal_fr_projects if language == Language.FR.value else \
        download_folder_internal_en_projects
    if not download_folder_projects.exists():
        download_folder_projects.mkdir(parents=True)
    create_csv_files(df_good_table_elements, download_folder_projects)

    project_file_items = []  # stores a list of (original filepath, filename) pairs for files in project zip folder

    # Iterate over the table element groups and create a zip folder for each table element group
    for _, row in df_good_table_element_groups.iterrows():
        table_element_group_id = row["TableElementGroupId"]

        # Get the list of all the csv files that need to be included in a table zip folder
        table_file_items = df_good_table_elements.loc[
            df_good_table_elements["TableElementGroupId"] == table_element_group_id, "CSVFilePath"].tolist()
        table_file_items = [(path, path.name) for path in table_file_items]

        # Create a table zip folder with all the csv files of the table element group
        # In the table zip folders enclosed in the project zip folder, we don't need a readme file in each table zip
        # folder, the metadata will be included in the project index file
        table_zip_folder_filepath = download_folder_projects.joinpath(Path(row["TableDownloadPath"]).name)
        create_zip_folder(table_zip_folder_filepath, table_file_items)

        # Add the table zip file item to the list of files that will be included in the project zip folder
        project_file_items.append((table_zip_folder_filepath, table_zip_folder_filepath.name))

    # Copy a project readme file to the projects folder
    tmp_project_readme_filepath = download_folder_projects.joinpath(f"readme_{application_id}.txt")
    readme_filepath = project_readme_filepath_fr if language == Language.FR.value else project_readme_filepath_en
    with ExceptionHandler(f"Error copying files from {readme_filepath} to {tmp_project_readme_filepath}"):
        shutil.copy(readme_filepath, tmp_project_readme_filepath)
    readme_filename = "lisezmoi.txt" if language == Language.FR.value else "readme.txt"
    project_file_items.append((tmp_project_readme_filepath, readme_filename))

    # Create a project index file
    index_file_column_map = common_column_map_fr if language == Language.FR.value else common_column_map_en
    tmp_project_index_filepath = download_folder_projects.joinpath(f"INDEX_PROJECT_{application_id}.csv")
    with ExceptionHandler(f"Error creating file {tmp_project_index_filepath}"):
        df_good_table_element_groups[index_file_column_map.keys()].rename(columns=index_file_column_map)\
            .to_csv(tmp_project_index_filepath, encoding="utf-8-sig", index=False)
    index_filename = "INDEX_PROJET.csv" if language == Language.FR.value else "INDEX_PROJECT.csv"
    project_file_items.append((tmp_project_index_filepath, index_filename))

    # Create the project zip folder
    # "ProjectDownloadPath" is like "/projects/ngtl.zip"
    project_zip_folder_filepath = download_folder_projects.joinpath(
        Path(df_good_table_element_groups["ProjectDownloadPath"].iloc[0]).name)
    create_zip_folder(project_zip_folder_filepath, project_file_items)
