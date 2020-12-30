import pandas as pd
import os
import shutil

index_filepath_eng = 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv' # 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv'

old_folder = 'G:/ESA_downloads/copy_Bingjie/'
readme_project_filepath = 'G:/ESA_downloads/README-ENG-projects.txt'

# Create a new folder as the destination for downloading files
new_folder = os.path.join('G:/ESA_downloads/', 'download_Bingjie')
os.mkdir(new_folder)

# Create a sub-folder for project download files
new_folder_projects = os.path.join(new_folder, 'projects')
os.mkdir(new_folder_projects)

# Create a sub-folder for table download files
new_folder_tables = os.path.join(new_folder, 'tables')
os.mkdir(new_folder_tables)

# =============================== Prepare index dataframe ===============================
df_index = pd.read_csv(index_filepath_eng)
df_index = df_index.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
columns = df_index.columns.to_list()

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})
df_index = df_index.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# =============================== Create Project Download Files ===============================
columns_project_index = columns
columns_project_index.remove('CSV Download URL')
columns_project_index.remove('PDF Page Number')

for project_folder_name in df_index['Download folder name'].unique():
    print(project_folder_name)
    df_project = df_index[df_index['Download folder name'] == project_folder_name]

    old_project_folder = os.path.join(old_folder, project_folder_name)

    # Create new project folder
    new_project_folder = os.path.join(new_folder_projects, project_folder_name)
    os.mkdir(new_project_folder)

    # Iterate over the table ids and create zip files of tables
    for table_id in df_project['Table ID'].unique():
        # Create a temporary folder in the new project folder for zipping csv files
        temp_folder_for_bundling = os.path.join(new_project_folder, 'temp-{}'.format(table_id))
        os.mkdir(temp_folder_for_bundling)

        # Copy the csv files of one table to the temporary folder in the new project folder
        df_table = df_project[df_project['Table ID'] == table_id]
        for csv in df_table['CSV Download URL'].apply(lambda x: x.split('/')[-1]):
            shutil.copy(os.path.join(old_project_folder, csv), os.path.join(temp_folder_for_bundling, csv))

        # Create a zip file of the table csvs
        # Use the name of the first csv file in the series  # TODO: decide on the zip file name of a table
        zipfile_name = df_table['CSV Download URL'].iloc[0].split('/')[-1]
        shutil.make_archive(os.path.join(new_project_folder, zipfile_name), 'zip', temp_folder_for_bundling)

        # Delete the temporary folder after zipping csv files of a table
        shutil.rmtree(temp_folder_for_bundling, ignore_errors=True)

    # Create index file for the project
    # TODO: add a column for table zip files
    # TODO: update master index file download url links
    df_project_index = df_project.groupby('Table ID').first().reset_index()[columns_project_index]
    df_project_index.to_csv(os.path.join(new_project_folder, 'INDEX_PROJECT.csv'), index=False)

    # Create readme.txt
    shutil.copy(readme_project_filepath, os.path.join(new_project_folder, 'readme.txt'))

    # Create project zip file
    shutil.make_archive(new_project_folder, 'zip', new_folder_projects, project_folder_name)

    # Delete project folder
    shutil.rmtree(new_project_folder, ignore_errors=True)


# =============================== Create Table Download Files ===============================




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
