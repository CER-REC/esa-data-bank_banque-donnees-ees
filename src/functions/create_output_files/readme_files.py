import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env", override=True)


table_readme_filepath_en = Path(os.getenv("TABLE_DOWNLOAD_README_FILEPATH_EN"))
project_readme_filepath_en = Path(os.getenv("PROJECT_DOWNLOAD_README_FILEPATH_EN"))
table_readme_filepath_fr = Path(os.getenv("TABLE_DOWNLOAD_README_FILEPATH_FR"))
project_readme_filepath_fr = Path(os.getenv("PROJECT_DOWNLOAD_README_FILEPATH_FR"))
