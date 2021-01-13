import pandas as pd
import os
import shutil
import multiprocessing

from Codes.Section_04_Final_Data_Merge_and_Visualization.bundle_utilites import bundle_for_project

index_filepath_eng = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG_12302020.csv'
# 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv'
# 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv'

csv_file_folder = 'F:/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_renamed'
# 'G:/ESA_downloads/copy_Bingjie/'
readme_project_filepath = 'G:/ESA_downloads/README-ENG-projects.txt'

# Create a new folder as the destination for downloading files
new_folder = os.path.join('G:/ESA_downloads/', 'download_Bingjie_test')
os.mkdir(new_folder)

# Create a sub-folder for project download files
new_folder_projects = os.path.join(new_folder, 'projects')
os.mkdir(new_folder_projects)

# Create a sub-folder for table download files
new_folder_tables = os.path.join(new_folder, 'tables')
os.mkdir(new_folder_tables)

# =============================== Prepare index dataframe ===============================
df_index = pd.read_csv(index_filepath_eng)

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})
df_index = df_index.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# Add a new column - Project Download URL
url_prefix = 'http://www.cer-rec.gc.ca/esa-ees'
df_index['Project Download URL'] = df_index['Download folder name']\
    .apply(lambda x: '{}/projects/{}.zip'.format(url_prefix, x))


# Add a new column - Table Download URL
def filename_to_tablename(filename):
    return filename.replace('.csv', '').replace('-pt1', '').replace('--', '-')


df_table_filename = df_index.sort_values(['PDF Page Number'])\
    .groupby('Table ID')['filename'].first().reset_index().rename(columns={'filename': 'Table Name'})
df_index = df_index.merge(df_table_filename, left_on='Table ID', right_on='Table ID')
df_index['Table Download URL'] = df_index['Table Name']\
    .apply(lambda x: '{}/tables/{}.zip'.format(url_prefix, filename_to_tablename(x)))

# Prepare a list of column names for the final index files
columns_index = [col for col in df_index.columns.to_list() if col not in (
    'Table ID', 'Table Name', 'CSV Download URL', 'Download folder name', 'Zipped Project Link', 'Unnamed: 0',
    'Unnamed: 0.1', 'Index', 'filename', 'old_filename', 'Content Type', 'Data ID')]

# =============================== Create Project Download Files ===============================
pool = multiprocessing.Pool()
args = [(df_index, project_folder_name, new_folder_projects, csv_file_folder, columns_index, readme_project_filepath)
        for project_folder_name in sorted(df_index['Download folder name'].unique().tolist())[:5]]
pool.starmap(bundle_for_project, args)
pool.close()

# =============================== Create Project Download Files ===============================
for project_folder_name in sorted(df_index['Download folder name'].unique().tolist()):
    df_project = df_index[df_index['Download folder name'] == project_folder_name]

    # old_project_folder = os.path.join(csv_file_folder, project_folder_name)

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
        for csv in df_table['filename']:
            shutil.copy(os.path.join(csv_file_folder, csv), os.path.join(temp_folder_for_bundling, csv))

        # Create a zip file of the table csvs
        zipfile_name = filename_to_tablename(df_table['filename'].iloc[0])
        shutil.make_archive(os.path.join(new_project_folder, zipfile_name), 'zip', temp_folder_for_bundling)

        # Delete the temporary folder after zipping csv files of a table
        shutil.rmtree(temp_folder_for_bundling, ignore_errors=True)

    # Create index file for the project
    df_project_index = df_project.sort_values(['Table ID', 'PDF Page Number'])\
        .groupby('Table ID').first().reset_index()[columns_index]
    df_project_index.to_csv(os.path.join(new_project_folder, 'INDEX_PROJECT.csv'), index=False)

    # Create readme.txt
    shutil.copy(readme_project_filepath, os.path.join(new_project_folder, 'readme.txt'))

    # Create project zip file
    shutil.make_archive(new_project_folder, 'zip', new_folder_projects, project_folder_name)

    # Delete project folder
    shutil.rmtree(new_project_folder, ignore_errors=True)


# =============================== Create Table Download Files ===============================
for table_id in sorted(df_index['Table ID'].unique().tolist()):
    df_table = df_index[df_index['Table ID'] == table_id]

    # Create a temporary folder in the new tables folder for zipping csv files
    temp_folder_for_bundling = os.path.join(new_folder_tables, 'temp-{}'.format(table_id))
    os.mkdir(temp_folder_for_bundling)

    # Copy the csv files of one table to the temporary folder in the new tables folder
    for _, row in df_table.iterrows():
        csv = row['filename']
        shutil.copy(os.path.join(csv_file_folder, csv),
                    os.path.join(temp_folder_for_bundling, csv))

    # Create readme.txt by append table metadata to the generic readme file
    readme_table_filepath = os.path.join(temp_folder_for_bundling, 'readme.txt')
    shutil.copy(readme_project_filepath, readme_table_filepath)
    with open(readme_table_filepath, 'a', encoding="utf-8") as file:
        metadata = ''
        for col in columns_index:
            if col == 'PDF Page Number' and df_table[col].min() != df_table[col].max():
                metadata += '{}: {} - {}\n'.format(col, df_table[col].min(), df_table[col].max())
            else:
                metadata += '{}: {}\n'.format(col, df_table.iloc[0][col])
        file.write(metadata)

    # Create a zip file of the table csvs and readme.txt
    zipfile_name = filename_to_tablename(df_table.sort_values('PDF Page Number')['filename'].iloc[0])
    shutil.make_archive(os.path.join(new_folder_tables, zipfile_name), 'zip', temp_folder_for_bundling)

    # Delete temp folder
    shutil.rmtree(temp_folder_for_bundling, ignore_errors=True)


# =============================== Create Master Index File ===============================
df_index.sort_values(['Table ID', 'PDF Page Number']).groupby('Table ID').first()\
    .reset_index()[columns_index].to_csv(os.path.join(new_folder, 'ESA_website_ENG.csv'), index=False)
