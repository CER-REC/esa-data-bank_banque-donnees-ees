import pandas as pd
import os
import shutil

index_filepath_eng = 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv'
# 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv'

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

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})
df_index = df_index.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# TODO: delete 'CSV Download URL' col, replace the usage of it with 'filename'
# TODO: create master index file

columns_index = df_index.columns.to_list()
columns_index.remove('CSV Download URL')  # TODO: ???

# =============================== Create Project Download Files ===============================
for project_folder_name in df_index['Download folder name'].unique():
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
    df_project_index = df_project.groupby('Table ID').first().reset_index()[columns_index]
    df_project_index.to_csv(os.path.join(new_project_folder, 'INDEX_PROJECT.csv'), index=False)

    # Create readme.txt
    shutil.copy(readme_project_filepath, os.path.join(new_project_folder, 'readme.txt'))

    # Create project zip file
    shutil.make_archive(new_project_folder, 'zip', new_folder_projects, project_folder_name)

    # Delete project folder
    shutil.rmtree(new_project_folder, ignore_errors=True)


# =============================== Create Table Download Files ===============================
for table_id in df_index['Table ID'].unique():
    df_table = df_index[df_index['Table ID'] == table_id]

    # Create a temporary folder in the new tables folder for zipping csv files
    temp_folder_for_bundling = os.path.join(new_folder_tables, 'temp-{}'.format(table_id))
    os.mkdir(temp_folder_for_bundling)

    # Copy the csv files of one table to the temporary folder in the new tables folder
    for _, row in df_table.iterrows():
        csv = row['CSV Download URL'].split('/')[-1]
        shutil.copy(os.path.join(old_folder, row['Download folder name'], csv),
                    os.path.join(temp_folder_for_bundling, csv))

    # Create readme.txt by append table metadata to the generic readme file
    readme_table_filepath = os.path.join(temp_folder_for_bundling, 'readme.txt')
    shutil.copy(readme_project_filepath, readme_table_filepath)
    with open(readme_table_filepath, 'a') as file:
        metadata = ''
        for col in columns_index:
            if col == 'PDF Page Number' and df_table[col].min() != df_table[col].max():
                metadata += '{}: {} - {}\n'.format(col, df_table[col].min(), df_table[col].max())
            else:
                metadata += '{}: {}\n'.format(col, df_table.iloc[0][col])
        file.write(metadata)

    # Create a zip file of the table csvs and readme.txt
    # Use the name of the first csv file in the series
    zipfile_name = df_table['CSV Download URL'].iloc[0].split('/')[-1]
    shutil.make_archive(os.path.join(new_folder_tables, zipfile_name), 'zip', temp_folder_for_bundling)

    # Delete temp folder
    shutil.rmtree(temp_folder_for_bundling, ignore_errors=True)

