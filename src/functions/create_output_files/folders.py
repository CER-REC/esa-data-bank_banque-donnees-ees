import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(".env", override=True)

root_folder = Path(os.getenv("OUTPUT_ROOT_DIRECTORY"))

# external folders
download_folder_external = root_folder.joinpath("external")

# English folders
download_folder_external_en = download_folder_external.joinpath("en")
download_folder_external_en_tables = download_folder_external_en.joinpath("tables")
download_folder_external_en_projects = download_folder_external_en.joinpath("projects")

# French folders
download_folder_external_fr = download_folder_external.joinpath("fr")
download_folder_external_fr_tables = download_folder_external_fr.joinpath("tables")
download_folder_external_fr_projects = download_folder_external_fr.joinpath("projects")

# internal folders
download_folder_internal = root_folder.joinpath("internal")

# English folders
download_folder_internal_en = download_folder_internal.joinpath("en")
download_folder_internal_en_tables = download_folder_internal_en.joinpath("tables")
download_folder_internal_en_projects = download_folder_internal_en.joinpath("projects")

# French folders
download_folder_internal_fr = download_folder_internal.joinpath("fr")
download_folder_internal_fr_tables = download_folder_internal_fr.joinpath("tables")
download_folder_internal_fr_projects = download_folder_internal_fr.joinpath("projects")
