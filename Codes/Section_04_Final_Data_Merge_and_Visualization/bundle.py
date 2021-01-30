import pandas as pd
import os
import multiprocessing

from Codes.Section_04_Final_Data_Merge_and_Visualization.bundle_utilites \
    import filename_to_tablename, bundle_for_project, bundle_for_table


index_filepath_eng = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG_2021_01_28.csv'

csv_file_folder = 'F:/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_latest_ENG'
readme_project_filepath = 'G:/ESA_downloads/README-ENG-projects.txt'

# Create a new folder as the destination for downloading files
new_folder = os.path.join('G:/ESA_downloads/', 'download_Bingjie_Jan292021_fra')
if not os.path.exists(new_folder):
    os.mkdir(new_folder)

# Create a sub-folder for project download files
new_folder_projects = os.path.join(new_folder, 'projects')
if not os.path.exists(new_folder_projects):
    os.mkdir(new_folder_projects)

# Create a sub-folder for table download files
new_folder_tables = os.path.join(new_folder, 'tables')
if not os.path.exists(new_folder_tables):
    os.mkdir(new_folder_tables)

# =============================== Prepare index dataframe ===============================
df_index_raw = pd.read_csv(index_filepath_eng, encoding='ISO-8859-1')

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index_raw.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})
df_index_raw = df_index_raw.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# Remove bad csvs
df_index = df_index_raw[~df_index_raw['bad_csv']]

# Add a new column - Project Download URL
url_prefix = 'http://www.cer-rec.gc.ca/esa-ees'
df_index['Project Download URL'] = df_index['Download folder name']\
    .apply(lambda x: '{}/projects/{}.zip'.format(url_prefix, x))

# Add a new column - Table Download URL
df_table_filename = df_index.sort_values(['PDF Page Number'])\
    .groupby('Table ID')['filename'].first().reset_index().rename(columns={'filename': 'Table Name'})
df_index = df_index.merge(df_table_filename, left_on='Table ID', right_on='Table ID')
df_index['Table Download URL'] = df_index['Table Name']\
    .apply(lambda x: '{}/tables/{}.zip'.format(url_prefix, filename_to_tablename(x)))

# Prepare a list of column names for the final index files
columns_index = [col for col in df_index.columns.to_list() if col not in (
    'Table ID', 'Table Name', 'CSV Download URL', 'Download folder name', 'Zipped Project Link', 'Unnamed: 0',
    'Unnamed: 0.1', 'Index', 'filename', 'old_filename', 'Content Type', 'Data ID', 'bad_csv')]

# =============================== Create Project Download Files ==============================
pool = multiprocessing.Pool()
args = [(df_index, project_folder_name, new_folder_projects, csv_file_folder, columns_index, readme_project_filepath)
        for project_folder_name in sorted(df_index['Download folder name'].unique().tolist())]
pool.starmap(bundle_for_project, args)
pool.close()

# =============================== Create Table Download Files ===============================
pool = multiprocessing.Pool()
args_table = [(df_index, table_id, new_folder_tables, csv_file_folder, columns_index, readme_project_filepath)
              for table_id in sorted(df_index['Table ID'].unique().tolist())]
pool.starmap(bundle_for_table, args_table)
pool.close()

# =============================== Create Master Index File ===============================
# Added figures back to alpha index file
df_index_with_figure = pd.read_csv('F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv')
figure_columns = columns_index.copy()
figure_columns.insert(1, 'Content Type')
figure_columns.remove('Project Download URL')
figure_columns.remove('Table Download URL')
df_figure = df_index_with_figure[df_index_with_figure['Content Type'] == 'Figure'][figure_columns]

# Add bad tables
bad_table_columns = columns_index.copy()
bad_table_columns.remove('Project Download URL')
bad_table_columns.remove('Table Download URL')
df_table_bad = df_index_raw[df_index_raw['bad_csv']].sort_values(['Table ID', 'PDF Page Number']).groupby('Table ID').first()\
    .reset_index()[bad_table_columns]
df_table_bad['Good Quality'] = False

# Concatenate all tables
df_table = df_index.sort_values(['Table ID', 'PDF Page Number']).groupby('Table ID').first()\
    .reset_index()[columns_index]
df_table['Good Quality'] = True

df_index_new = pd.concat([df_figure, df_table, df_table_bad])

# Export alpha index
df_index_new.to_csv(os.path.join(new_folder, 'ESA_website_ENG.csv'), index=False, encoding='ISO-8859-1')
