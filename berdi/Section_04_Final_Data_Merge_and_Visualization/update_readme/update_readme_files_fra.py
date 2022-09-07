import pandas as pd
import os
import zipfile
import tempfile


df_index = pd.read_csv('data/download_internal_Aug2022_merged/fr/ESA_website_FRA.csv', encoding='utf-8-sig')  # 21643, 49

# Update French project readme
folder_fr = 'data/download_internal_Aug2022_merged/fr'
readme_project_filepath_fr = 'berdi/Section_04_Final_Data_Merge_and_Visualization/update_readme/README-FRA-projects.txt'
for project_path in df_index["Chemin d'accès pour télécharger le projet"].dropna().unique().tolist():
    print(project_path)
    project_zipfile = folder_fr + project_path
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

    metadata = open(readme_project_filepath_fr, 'r', encoding="utf-8-sig").read()
    # save the table readme file to the new table zip file
    project = project_zipfile.split('/')[-1].replace('.zip', '')
    with zipfile.ZipFile(project_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(project + '/lisezmoi.txt', metadata)


# Update English table readme
readme_table_filepath_fr = 'berdi/Section_04_Final_Data_Merge_and_Visualization/update_readme/README-FRA-tables.txt'
columns = ['Titre',
           'Type de contenu',
           'Nom de la demande',
           'Nom abrégé de la demande',
           'Dépôt de la demande',
           'Nom de la société',
           'Produit de base',
           'Nom de fichier',
           'URL du dossier de l\'ÉES',
           'URL de téléchargement PDF',
           'Type de demande',
           'Emplacement du pipeline',
           'Ordonnance d\'audience',
           'Nom du consultant',
           'État d\'avancement',
           'URL de la demande',
           'URL de la décision',
           'Sections de l\'EES',
           'Numéro de page PDF',
           'Chemin d\'accès pour télécharger le projet',
           'Chemin d\'accès pour télécharger le tableau']

for table_path in df_index['Chemin d\'accès pour télécharger le tableau'].dropna().unique().tolist():
    print(table_path)
    table_zipfile = folder_fr + table_path
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
    df_table = df_index[df_index['Chemin d\'accès pour télécharger le tableau'] == table_path]
    metadata = open(readme_table_filepath_fr, 'r', encoding="utf-8-sig").read()
    for col in columns:
        if col == 'Numéro de page PDF' and df_table.iloc[0]['Nombre de pages'] > 1:
            metadata += '{}: {} - {}\n'.format(col, df_table.iloc[0][col],
                                               int(df_table.iloc[0][col] + df_table.iloc[0]['Nombre de pages'] - 1))
        else:
            metadata += '{}: {}\n'.format(col, df_table.iloc[0][col])
    # save the table readme file to the new table zip file
    with zipfile.ZipFile(table_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('lisezmoi.txt', metadata)
