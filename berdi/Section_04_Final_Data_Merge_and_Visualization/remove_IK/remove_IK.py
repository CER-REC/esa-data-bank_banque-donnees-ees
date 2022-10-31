import pandas as pd
import os
import shutil


new_folder = 'G:/Board/ESA_downloads/NEBC/external/en'

# Manually copy over the projects and tables folders from internal download package the internal folder

df_index = pd.read_csv('G:/Board/ESA_downloads/NEBC/external/en/ESA_website_ENG.csv', encoding='utf-8-sig')  # 21643, 49
print(df_index.shape)

# Delete IK tables
for index, row in df_index[df_index['Table Download Path'].notna() & df_index['IK_Labels']].iterrows():
    file_path = new_folder + row['Table Download Path']
    if not os.path.exists(file_path):
        print('Table file missing: {}'.format(file_path))
        continue
    os.remove(file_path)

# df_index[df_index['Table Download Path'].notna() & (df_index['IK_Labels'] == 0)].shape  # 13775


# Delete IK tables in project folders
columns = ['Title',
           'Content Type',
           'Application Name',
           'Application Short Name',
           'Application Filing Date',
           'Company Name',
           'Commodity',
           'File Name',
           'ESA Folder URL',
           'PDF Download URL',
           'Application Type',
           'Pipeline Location',
           'Hearing order',
           'Consultant Name',
           'Pipeline Status',
           'Application URL',
           'Decision URL',
           'ESA Section(s)',
           'PDF Page Number',
           'Project Download Path',
           'Table Download Path']
projects_folder = new_folder + '/projects'
for project_download_path in df_index[df_index['Project Download Path'].notna() & df_index['IK_Labels']]\
        ['Project Download Path'].unique().tolist():
    project_zip_file_path = new_folder + project_download_path
    if not os.path.exists(project_zip_file_path):
        print('Project file missing: {}'.format(project_zip_file_path))
        continue

    # Unzip the project zip file to project_folder
    project_folder = project_zip_file_path.replace('.zip', '')
    shutil.unpack_archive(project_zip_file_path, projects_folder)

    # Delete IK tables in the unpacked project folder
    table_paths_to_delete = df_index[df_index['Table Download Path'].notna() & df_index['IK_Labels'] &
                                     (df_index['Project Download Path'] == project_download_path)]['Table Download Path'].tolist()
    for table_path in table_paths_to_delete:
        table_file_path = project_folder + '/' + table_path.split('/')[-1]
        if not os.path.exists(table_file_path):
            print('Table file missing: {}'.format(table_file_path))
            continue
        os.remove(table_file_path)

    # Delete IK rows from INDEX_PROJECT.csv
    df_project = pd.read_csv(project_folder + '/INDEX_PROJECT.csv', encoding='utf-8-sig')
    df_project = df_project[~df_project['Table Download Path'].isin(table_paths_to_delete)]
    df_project[columns].to_csv(project_folder + '/INDEX_PROJECT.csv', encoding='utf-8-sig', index=False)

    # Delete the existing project zip file
    os.remove(project_zip_file_path)

    # Create a new project zip file
    shutil.make_archive(project_folder, 'zip', projects_folder, project_folder.split('/')[-1])

    # Delete the project folder
    shutil.rmtree(project_folder, ignore_errors=True)


# Create the index file at the top level
df_index.loc[df_index['IK_Labels'] == 0, df_index.columns != 'IK_Labels']\
    .to_csv(new_folder+'/ESA_website_ENG.csv', index=False, encoding='utf-8-sig')


# QA
df_index_external = pd.read_csv(new_folder+'/ESA_website_ENG.csv')  # 20630, 48
print(df_index_external.shape)

