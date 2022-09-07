import pandas as pd
import os
import shutil


new_folder = 'data/download_external_Aug2022_merged/fr'

# Manually copy over the projects and tables folders from internal download package to the external folder

df_index = pd.read_csv('data/download_external_Aug2022_merged/fr/ESA_website_FRA.csv', encoding='utf-8-sig')

# Delete IK tables
for index, row in df_index[df_index["Chemin d'accès pour télécharger le tableau"].notna() & df_index['IK_Labels']].iterrows():
    file_path = new_folder + row["Chemin d'accès pour télécharger le tableau"]
    if not os.path.exists(file_path):
        print('Table file missing: {}'.format(file_path))
        continue
    os.remove(file_path)


# Delete IK tables in project folders
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
projects_folder = new_folder + '/projects'
for project_download_path in df_index[df_index['IK_Labels'] == 1]["Chemin d'accès pour télécharger le projet"].dropna().unique().tolist():
    project_zip_file_path = new_folder + project_download_path
    if not os.path.exists(project_zip_file_path):
        print('Project file missing: {}'.format(project_zip_file_path))
        continue

    # Unzip the project zip file to project_folder
    project_folder = project_zip_file_path.replace('.zip', '')
    shutil.unpack_archive(project_zip_file_path, projects_folder)

    # Delete IK tables in the unpacked project folder
    table_paths_to_delete = df_index[df_index["Chemin d'accès pour télécharger le tableau"].notna() &
                                     df_index['IK_Labels'] &
                                     (df_index["Chemin d'accès pour télécharger le projet"] == project_download_path)]\
        ["Chemin d'accès pour télécharger le tableau"].tolist()
    for table_path in table_paths_to_delete:
        table_file_path = project_folder + '/' + table_path.split('/')[-1]
        if not os.path.exists(table_file_path):
            print('Table file missing: {}'.format(table_file_path))
            continue
        os.remove(table_file_path)

    # Delete IK rows from INDEX_PROJECT.csv
    try:
        df_project = pd.read_csv(project_folder + '/INDEX_PROJET.csv', encoding='utf-8-sig')
    except:
        df_project = pd.read_csv(project_folder + '/INDEX_PROJET.csv', encoding='cp1252')

    # if "Type de demande (Loi sur l'Office national de l'énergie)" in df_project.columns:
    #     df_project = df_project.rename(columns={"Type de demande (Loi sur l'Office national de l'énergie)": 'Type de demande'})

    df_project = df_project[~df_project["Chemin d'accès pour télécharger le tableau"].isin(table_paths_to_delete)]
    df_project[columns].to_csv(project_folder + '/INDEX_PROJET.csv', encoding='utf-8-sig', index=False)

    # Delete the existing project zip file
    os.remove(project_zip_file_path)

    # Create a new project zip file
    shutil.make_archive(project_folder, 'zip', projects_folder, project_folder.split('/')[-1])

    # Delete the project folder
    shutil.rmtree(project_folder, ignore_errors=True)

# Create the index file at the top level
df_index.loc[df_index['IK_Labels'] == 0, df_index.columns != 'IK_Labels']\
    .to_csv(new_folder+'/ESA_website_FRA.csv', index=False, encoding='utf-8-sig')


df_index_external = pd.read_csv(new_folder+'/ESA_website_FRA.csv', encoding='utf-8-sig')
