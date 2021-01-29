import os
import shutil


def filename_to_tablename(filename):
    return filename.replace('.csv', '').replace('-pt1', '').replace('--', '-')


def bundle_for_project(df_index, project_folder_name, new_folder_projects, csv_file_folder, columns_index, readme_project_filepath):
    print('Start processing for project: {}'.format(project_folder_name))

    df_project = df_index[df_index['Download folder name'] == project_folder_name]

    # Create new project folder
    new_project_folder = os.path.join(new_folder_projects, project_folder_name)
    if not os.path.exists(new_project_folder):
        os.mkdir(new_project_folder)

    # Iterate over the table ids and create zip files of tables
    for table_id in df_project['Table ID'].unique():
        # Create a temporary folder in the new project folder for zipping csv files
        temp_folder_for_bundling = os.path.join(new_project_folder, 'temp-{}'.format(table_id))
        if not os.path.exists(temp_folder_for_bundling):
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


def bundle_for_table(df_index, table_id, new_folder_tables, csv_file_folder, columns_index, readme_project_filepath):
    print('Start processing table - table id: {}'.format(table_id))
    df_table = df_index[df_index['Table ID'] == table_id]

    # Create a temporary folder in the new tables folder for zipping csv files
    temp_folder_for_bundling = os.path.join(new_folder_tables, 'temp-{}'.format(table_id))
    if not os.path.exists(temp_folder_for_bundling):
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
