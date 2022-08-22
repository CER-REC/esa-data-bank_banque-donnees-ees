import pandas as pd
import os
import zipfile
import tempfile


index_en = pd.read_csv('data/download_internal_Aug2022_merged/en/ESA_website_ENG.csv', encoding='utf-8-sig')  # 21643, 47

# Update English project readme
folder_en = 'data/download_internal_Aug2022_merged/en'
readme_project_filepath_en = 'berdi/Section_04_Final_Data_Merge_and_Visualization/update_readme/README-ENG-projects.txt'
for project_path in index_en['Project Download Path'].dropna().unique().tolist():
    print(project_path)
    project_zipfile = folder_en + project_path
    tmpfd, tmpfile = tempfile.mkstemp(dir=os.path.dirname(project_zipfile))
    os.close(tmpfd)
    with zipfile.ZipFile(project_zipfile, 'r') as zin:
        with zipfile.ZipFile(tmpfile, 'w') as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                if not item.filename.endswith('.txt'):
                    # copy all the files to the temp zip file except the readme.txt file
                    zout.writestr(item, zin.read(item.filename))
    os.remove(project_zipfile)  # delete the old project zip file
    os.rename(tmpfile, project_zipfile)  # rename the temp file to the project zip file

    metadata = open(readme_project_filepath_en, 'r', encoding="utf-8-sig").read()
    # save the table readme file to the new table zip file
    project = project_zipfile.split('/')[-1].replace('.zip', '')
    with zipfile.ZipFile(project_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(project + '/readme.txt', metadata)


# Update English table readme
readme_table_filepath_en = 'berdi/Section_04_Final_Data_Merge_and_Visualization/update_readme/README-ENG-tables.txt'
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
for table_path in index_en['Table Download Path'].dropna().unique().tolist():
    print(table_path)
    table_zipfile = folder_en + table_path
    tmpfd, tmpfile = tempfile.mkstemp(dir=os.path.dirname(table_zipfile))
    os.close(tmpfd)
    with zipfile.ZipFile(table_zipfile, 'r') as zin:
        with zipfile.ZipFile(tmpfile, 'w') as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                if not item.filename.endswith('.txt'):
                    # copy all the files to the temp zip file except the readme.txt file
                    zout.writestr(item, zin.read(item.filename))
    os.remove(table_zipfile)  # delete the old table zip file
    os.rename(tmpfile, table_zipfile)  # rename the temp file to the table zip file

    # create the table readme.txt
    df_table = index_en[index_en['Table Download Path'] == table_path]
    metadata = open(readme_table_filepath_en, 'r', encoding="utf-8-sig").read()
    for col in columns:
        if col == 'PDF Page Number' and df_table.iloc[0]['Page Count'] > 1:
            metadata += '{}: {} - {}\n'.format(col, df_table.iloc[0][col],
                                               int(df_table.iloc[0][col] + df_table.iloc[0]['Page Count'] - 1))
        else:
            metadata += '{}: {}\n'.format(col, df_table.iloc[0][col])
    # save the table readme file to the new table zip file
    with zipfile.ZipFile(table_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('readme.txt', metadata)
