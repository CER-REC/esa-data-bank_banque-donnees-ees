import pandas as pd
import os

# index_filepath_eng = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv'
index_filepath_eng = 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv'

df_index = pd.read_csv(index_filepath_eng)
df_index = df_index.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
columns = df_index.columns.to_list()

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})

df_index = df_index.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# Create a new folder
new_folder = os.path.join('G:/ESA_downloads/', 'download_Bingjie')
os.mkdir(new_folder)

# Create a sub-folder for project download files
new_folder_projects = os.path.join(new_folder, 'projects')
os.mkdir(new_folder_projects)

# Create Project Download Files
folder = 'G:/ESA_downloads/copy_Bingjie/'
for project_folder_name in df_index['Download folder name'].unique():
    print(project_folder_name)
    new_project_folder = os.path.join(new_folder_projects, project_folder_name)
    os.mkdir(new_project_folder)

    df_project = df_index[df_index['Download folder name'] == project_folder_name]

    # Bundle csv tables
    old_project_folder = os.path.join(folder, project_folder_name)
    for table in df_project['Table ID'].unique():
        df_table = df_project[df_project['Table ID'] == table]
        df_table['CSV Download URL']










# check what columns to use for identifying tables
df_index_temp = df_index.head(10000)
columns_unique_for_table = df_index_temp.columns.to_list()
columns_unique_for_table.remove('CSV Download URL')
columns_unique_for_table.remove('PDF Page Number')

for key, group in df_index_temp.groupby(['Title', 'Data ID']):
    # print(key, group)
    # for col in columns_unique_for_table:
    #     if group[col].nunique() > 1:
    #         print(col)
    #         print(key)
    #         break
    pages = group['PDF Page Number'].to_list()
    pages_sorted = sorted(pages)
    pages_range = list(range(min(pages), max(pages) + 1))
    if pages_sorted != pages_range:
        print(key, pages)

df_y = df_index_temp.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

df_z = df_index_temp.join(df_table_id, on=['Title', 'Data ID'], how='left')
