import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import sys

sys.path.append(str(Path(__file__).parents[2].resolve()))

from berdi.Database_Connection_Files.connect_to_sqlserver_database import connect_to_db

# paths to data
REPO_ROOT = Path(__file__).parents[2].resolve()
RAW_DATA_PATH = REPO_ROOT / "data" / "raw"
INTERMEDIATE_INDEX_PATH = REPO_ROOT / "data" / "interim" / "Intermediate_Index_Files"
projects_path = str(INTERMEDIATE_INDEX_PATH / "Phase3_Index_of_PDFs_for_Major_Projects_with_ESAs.csv")
#save_dir = REPO_ROOT / "data" / "output"

# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=REPO_ROOT / "berdi/Database_Connection_Files" / ".env", override=True
)
conn = connect_to_db()


table_info_csv_path = str(INTERMEDIATE_INDEX_PATH / "all_tables-final.csv")
df_table_info = pd.read_csv(table_info_csv_path, encoding = 'utf-8-sig')
df_table_info = df_table_info[df_table_info['titleFinal'].notna()][['csvFileName', 'csvFullPath', 'pdfId', 'page', 'tableNumber', 'titleFinal']]

# Get the interim application index file (with columns topics, PDF Outline, PDF Size (bytes), PDF Page Count)
df_app = pd.read_csv(projects_path)


# Organize pdf attributes
['Application Name', 'Application Short Name', 'Application Filing Date',
 'Company Name', 'Commodity',
 'File Name', 'ESA Folder URL', 'Document Number', 'Data ID', 'PDF Download URL',
 'Application Type', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
 'ESA Section(s)', 'ESA Section(s) Index', 'ESA Section(s) Topics',
 'PDF Page Count', 'PDF Size', 'PDF Outline']


df_app = df_app[['Application Name', 'Application Short Name', 'Application Filing Date',
                 'Company Name', 'Commodity',
                 'File Name', 'ESA Folder URL', 'Document Number', 'Data ID', 'PDF Download URL',
                 'Application Type', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
                 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
                 'ESA Section(s)', 'ESA Section(s) Index', 'Topics', 'PDF Size (bytes)', 'Number of Pages',
                'Outline Present']]
df_app = df_app.rename(columns={'Number of Pages': 'PDF Page Count'})

# Compose pdf and csv table attributes
df_table_app = df_table_info.merge(df_app, left_on='pdfId', right_on='Data ID')
df_table_app = df_table_app.rename(columns={'page': 'PDF Page Number', 'titleFinal': 'Title'})
df_table_app = df_table_app.drop(labels=['pdfId'], axis=1)

df_table_index = df_table_app[['Title', 'Application Name', 'Application Short Name', 'Application Filing Date',
                 'Company Name', 'Commodity', 'File Name', 'ESA Folder URL', 'Document Number', 'Data ID', 
                 'PDF Download URL', 'Application Type', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
                 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
                 'ESA Section(s)', 'ESA Section(s) Index', 'Topics', 'PDF Page Number', 'tableNumber', 'csvFileName', 'PDF Size (bytes)', 'PDF Page Count',
                'Outline Present']]

# Get Figure Titles
df_fig_titles = pd.read_sql('''SELECT pdfId, page_num, block_order, titleTag FROM [DS_TEST].[BERDI].blocks
                    WHERE (bbox_area_image/bbox_area) > 0.1 and titleTag is not null ;''', conn)
# Compose pdf and figure attributes
df_figure_app = df_fig_titles.merge(df_app, left_on='pdfId', right_on='Data ID')
df_figure_app = df_figure_app.rename(columns={'page_num': 'PDF Page Number', 'block_order': 'figureNumber', 'titleTag': 'Title'})
df_figure_app = df_figure_app.drop(labels=['pdfId'], axis=1)

df_figure_index = df_figure_app[['Title', 'Application Name', 'Application Short Name', 'Application Filing Date',
                 'Company Name', 'Commodity', 'File Name', 'ESA Folder URL', 'Document Number', 'Data ID', 
                 'PDF Download URL', 'Application Type', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
                 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
                 'ESA Section(s)', 'ESA Section(s) Index', 'Topics', 'PDF Page Number', 'figureNumber','PDF Size (bytes)', 'PDF Page Count',
                'Outline Present']]

# df_table_index.columns
# df_table_index.shape (473, 27)
# df_figure_index.columns
# df_figure_index.shape (19, 27)

df_table_fig_index = df_table_index.append(df_figure_index, ignore_index=True)

# df_table_fig_index.columns
# df_table_fig_index.shape (492, 28)

df_table_fig_index['Content Type'] = ['Table' if x.lower().startswith('table') else 'Figure' for x in df_table_fig_index['Title']]

df_table_fig_index.to_csv(str(INTERMEDIATE_INDEX_PATH) + "/"
            "table_figs_index.csv",
            index=False,
            encoding="utf-8-sig",
        )
