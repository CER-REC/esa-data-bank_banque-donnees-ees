import shutil
from pathlib import Path
import zipfile
import pandas as pd

from src.functions.create_output_files.folders import download_folder_internal_en, download_folder_external_en, \
    download_folder_external_en_tables, download_folder_external_en_projects
from src.functions.create_output_files.folders import download_folder_external_fr, \
    download_folder_internal_fr, download_folder_external_fr_tables, download_folder_external_fr_projects
from src.functions.create_output_files.columns import common_column_map_en, common_column_map_fr
from src.functions.create_output_files.internal.helper import create_zip_folder
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.functions.create_output_files.language import Language


def create_external_folder(language=Language.EN.value):
    """
        This function is to create the external dataset by copying 
        over the internal dataset and deleting IK content

        Parameters
        -----------------
        language (enum): indicates translated language
    """
    download_folder_external = download_folder_external_en if language == Language.EN.value \
        else download_folder_external_fr
    download_folder_internal = download_folder_internal_en if language == Language.EN.value \
        else download_folder_internal_fr
    download_folder_external_tables = download_folder_external_en_tables if language == Language.EN.value \
        else download_folder_external_fr_tables
    download_folder_external_projects = download_folder_external_en_projects if language == Language.EN.value \
        else download_folder_external_fr_projects
    common_column_map = common_column_map_en if language == Language.EN.value else common_column_map_fr
    index_file = "ESA_website_ENG.csv" if language == Language.EN.value else "ESA_website_FRA.csv"

    if download_folder_external.exists():
        # if output_directory/external/[en|fr] folder exists already, delete it
        # so that we can create external/[en|fr] folder starting from scratch
        shutil.rmtree(download_folder_external)

    # 1) copy over output_directory/internal/en to output_directory/external/en
    with ExceptionHandler(f"Error copying {download_folder_internal} to {download_folder_external}"):
        shutil.copytree(download_folder_internal, download_folder_external)

    # read the project index file into a dataframe, which has a IK_Labels column
    df_index = pd.read_csv(download_folder_internal.joinpath(index_file), encoding="utf-8-sig")
    df_ik_tables = df_index[df_index[common_column_map["TableDownloadPath"]].notna() & df_index["IK_Labels"]]

    # 2) delete IK tables from output_directory/external/[en|fr]/tables
    for table_download_path in df_ik_tables[common_column_map["TableDownloadPath"]].tolist():
        
        # iterate all the table download zip folders with IK, and delete each one
        table_download_zipfolder_path = download_folder_external_tables.joinpath(Path(table_download_path).name)
        with ExceptionHandler(f"Error deleting {table_download_zipfolder_path}"):
            if not table_download_zipfolder_path.exists():
                # If the table download file does exist, raise error
                raise FileNotFoundError(f"{table_download_zipfolder_path} does not exist")
            # delete the table download file with IK
            table_download_zipfolder_path.unlink()

    # 3) delete IK tables in project download zip folders
    project_index_file_columns = common_column_map.values()
    for project_download_path in df_ik_tables[common_column_map["ProjectDownloadPath"]].unique().tolist():
        project_download_zipfolder_filepath = download_folder_external_projects\
            .joinpath(Path(project_download_path).name)

        with ExceptionHandler(f"Missing {project_download_zipfolder_filepath}"):
            if not project_download_zipfolder_filepath.exists():
                # If the table download file does exist, raise error
                raise FileNotFoundError(f"{project_download_zipfolder_filepath} does not exist")
        
        # Unzip the project zip file to project_folder
        project_folder = download_folder_external_projects.joinpath(Path(project_download_path).name
                                                                       .replace(".zip", ""))
        with zipfile.ZipFile(project_download_zipfolder_filepath, "r") as zip_ref:
            zip_ref.extractall(project_folder)

        # Delete IK tables in the unpacked project folder
        table_files_to_delete = df_ik_tables[df_ik_tables[common_column_map["ProjectDownloadPath"]] ==
                                             project_download_path][common_column_map["TableDownloadPath"]]\
                                             .apply(lambda x: Path(x).name).tolist()
        for filepath in table_files_to_delete:
            absolute_filepath = project_folder.joinpath(filepath)
            with ExceptionHandler(f"Error deleting {absolute_filepath}"):
                if not absolute_filepath.exists():
                    # If the table zip file does exist inside the project folder, raise error
                    raise FileNotFoundError(f"{absolute_filepath} does not exist")
                # delete the table zip file with IK
                absolute_filepath.unlink()

        # Rewrite INDEX_PROJECT.csv with a new index file with no IK rows
        project_index_filepath = project_folder.joinpath("INDEX_PROJECT.csv")
        df_index[df_index[common_column_map["TableDownloadPath"]].notna() & (df_index["IK_Labels"] == 0) &
                (df_index[common_column_map["ProjectDownloadPath"]] == project_download_path)] \
                [project_index_file_columns] \
                .to_csv(project_index_filepath, index=False)
        
        # Create a zip folder with non-ik files for the project
        # within this function, files will be deleted after being moved to the zipfolder
        create_zip_folder(project_download_zipfolder_filepath, [(f, f.name) for f in project_folder.glob('**/*')])

        # Delete the empty project folder after the zip folder is created
        project_folder.rmdir()  # Remove this directory. The directory must be empty.
    
    # 4) create the new index file excluding IK rows
    master_index_filepath = download_folder_external.joinpath(index_file)
    with ExceptionHandler(f"Error creating project index file {master_index_filepath}"):
        df_index.loc[df_index["IK_Labels"] == 0, df_index.columns != "IK_Labels"] \
            .to_csv(master_index_filepath, index=False, encoding="utf-8-sig")
