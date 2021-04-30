import pandas as pd
import os
import multiprocessing

from Codes.Section_04_Final_Data_Merge_and_Visualization.bundle.bundle_utilites \
    import bundle_for_project, bundle_for_table

index_filepath_eng = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG_2021_01_28.csv'
index_filepath_fra = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_FRA_2021_03_04_final.csv'

csv_file_folder = 'F:/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_latest_FRA'
readme_project_filepath = 'G:/ESA_downloads/README-FRA-projects.txt'
readme_table_filepath = '//luxor/data/Board/ESA_downloads/README-FRA-tables.txt'

# Create a new folder as the destination for downloading files
new_folder = os.path.join('G:/ESA_downloads/', 'download_Bingjie_Apr202021_fra')
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
df_index_raw_eng = pd.read_csv(index_filepath_eng)
df_index_raw_fra = pd.read_csv(index_filepath_fra, encoding='latin-1')

df_eng_index_final = pd.read_csv('G:/ESA_downloads/download_Bingjie_Mar262021/ESA_website_ENG.csv')

# Clean up unrecognized characters
for col in df_index_raw_fra.columns:
    df_index_raw_fra.rename(columns={col: col.replace('\x92', '\'')}, inplace=True)
df_index_raw_fra = df_index_raw_fra.applymap(lambda x: x.replace('\x92', '\'') if type(x) is str else x)

df_merge = pd.merge(df_index_raw_eng, df_index_raw_fra, left_on=['Index'], right_on=['Indice'])
df_merge_id = pd.merge(df_merge, df_eng_index_final, left_on=['Document Number', 'Title'], right_on=['Document Number', 'Title'], how='left')
df_x = df_merge_id[df_merge_id['ID'].isna()]  # empty dataframe

# # Create a temporary column in the index dataframe as table identification
# df_table_id = df_index_raw_eng.groupby(['Title', 'Data ID']).size()\
#     .reset_index().drop(columns=[0])\
#     .reset_index().rename(columns={'index': 'ID'})
# df_index_raw_eng = df_index_raw_eng.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# Add table id to french index (table id is identified by Title and Data ID from English index file
df_index_raw_fra = df_index_raw_fra.merge(df_merge_id[['Indice', 'ID']])

# Remove bad csvs
df_index = df_index_raw_fra[~df_index_raw_fra['CSV Manquant']]

# Add a new column - Project Download Path
df_index["Chemin d'accès pour télécharger le projet"] = df_index['Télécharger le nom du dossier']\
    .apply(lambda x: '/projects/{}.zip'.format(x))

# Add a new column - Table Download Path
df_table_filename = df_index.sort_values(['Numéro de page PDF'])\
    .groupby('ID')['Nom du CSV'].first().reset_index().rename(columns={'Nom du CSV': 'Table Name'})
df_table_filename['Table Name'] = df_table_filename['Table Name']\
    .apply(lambda x: x.replace('.csv', '').replace('--', '-'))
df_index = df_index.merge(df_table_filename, left_on='ID', right_on='ID')
df_index["Chemin d'accès pour télécharger le tableau"] = df_index['Table Name']\
    .apply(lambda x: '/tables/{}.zip'.format(x))

# Update ESA Download URLs
df_index['URL du dossier de l\'ÉES'] = df_index['URL du dossier de l\'ÉES'].apply(lambda x: x.replace('LoadResult', 'View'))
# Update Application Short Name
df_short_name_translated = pd.read_csv('G:/ESA_downloads/application_short_name_translation.csv', encoding='latin-1')
short_name_translation = dict()
for item in df_short_name_translated.itertuples():
    short_name_translation[item.English] = item.French
df_index['Nom abrégé de la demande'] = df_index['Nom abrégé de la demande'].apply(lambda x: short_name_translation[x.strip()])
# Update location Colombie-Britannique, Territoires du Nord-Ouest
df_index['Emplacement du pipeline'] = df_index['Emplacement du pipeline']\
    .apply(lambda x: ', '.join([location.replace('Colombie britannique', 'Colombie-Britannique')
                               .replace('Territoires du nord-ouest', 'Territoires du Nord-Ouest') for location in x.split(', ')]))

# Prepare a list of column names for the final index files
columns_index = [col for col in df_index.columns.to_list() if col not in (
    'Unnamed: 0', 'Unnamed: 0.1', 'Table Name',
    'Data ID', 'Identificateur de données',
    'CSV Download URL', 'URL de téléchargement CSV',
    'Download folder name', 'Télécharger le nom du dossier',
    'Zipped Project Link', 'Lien vers le projet compressé',
    'Indice', 'Index',
    'filename', 'Nom du CSV',
    'bad_csv', 'CSV Manquant',
    'Vieux Nom du CSV')]


# =============================== Create Project Download Files ==============================
pool = multiprocessing.Pool()
args = [(df_index, project_folder_name, new_folder_projects, csv_file_folder, columns_index, readme_project_filepath, True)
        for project_folder_name in sorted(df_index['Télécharger le nom du dossier'].unique().tolist())]
pool.starmap(bundle_for_project, args)
pool.close()

# =============================== Create Table Download Files ===============================
pool = multiprocessing.Pool()
args_table = [(df_index, table_id, new_folder_tables, csv_file_folder, columns_index, readme_table_filepath, True)
              for table_id in sorted(df_index['ID'].unique().tolist())]
pool.starmap(bundle_for_table, args_table)
pool.close()

# =============================== Create Master Index File ===============================
# Added figures back to alpha index file
df_index_with_figure = pd.read_csv('F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_FRA_03032021.csv', encoding='latin-1')
df_index_with_figure = df_index_with_figure[df_index_with_figure['Type de contenu'] == 'Figure']
for col in df_index_with_figure.columns:
    df_index_with_figure.rename(columns={col: col.replace('\x92', '\'')}, inplace=True)
df_index_with_figure = df_index_with_figure.applymap(lambda x: x.replace('\x92', '\'') if type(x) is str else x)

# for column in df_index_with_figure.columns:
#     if '\u2019' in column:
#         df_index_with_figure.rename(columns={column: column.replace('\u2019', '\'')}, inplace=True)
# for column in df_index_with_figure.columns:
#     df_index_with_figure[column] = df_index_with_figure[column]\
#         .apply(lambda x: x.replace('\u2013', '-').replace('\u2014', '-').replace('\u2019', '\'') if type(x) is str else x)
#     df_index_with_figure[column] = df_index_with_figure[column] \
#         .apply(lambda x: x.encode('latin-1', errors='ignore').decode('latin-1', errors='ignore') if type(x) is str else x)

figure_columns = columns_index.copy()
figure_columns.remove('ID')
figure_columns.remove("Chemin d'accès pour télécharger le projet")
figure_columns.remove("Chemin d'accès pour télécharger le tableau")
df_figure = df_index_with_figure[figure_columns]
df_figure['ID'] = df_figure.index + df_index_raw_fra['ID'].max() + 1

# Add bad tables
bad_table_columns = columns_index.copy()
bad_table_columns.remove("Chemin d'accès pour télécharger le projet")
bad_table_columns.remove("Chemin d'accès pour télécharger le tableau")
df_table_bad = df_index_raw_fra[df_index_raw_fra['CSV Manquant']].sort_values(['ID', 'Numéro de page PDF']).groupby('ID').first()\
    .reset_index()[bad_table_columns]
df_table_bad['Bonne qualité'] = False

# Concatenate all tables
df_table = df_index.sort_values(['ID', 'Numéro de page PDF']).groupby('ID').first()\
    .reset_index()[columns_index]
df_table['Bonne qualité'] = True

df_index_new = pd.concat([df_figure, df_table, df_table_bad])

# Update ESA Download URLs
df_index_new['URL du dossier de l\'ÉES'] = df_index_new['URL du dossier de l\'ÉES'].apply(lambda x: x.replace('LoadResult', 'View'))
# Translate 'Nom de la demande'
df_index_new.loc[df_index_new['Nom de la demande'] == 'Application for the Keystone Pipeline', 'Nom de la demande'] = \
    'Demande relative au projet de Keystone Pipeline'
# Translate 'Nom abrégé de la demande'
df_index_new['Nom abrégé de la demande'] = df_index_new['Nom abrégé de la demande'].apply(lambda x: short_name_translation[x.strip()] if x.strip() in short_name_translation else x)
# Update location
df_index_new['Emplacement du pipeline'] = df_index_new['Emplacement du pipeline']\
    .apply(lambda x: ', '.join([location.replace('Colombie britannique', 'Colombie-Britannique')
                               .replace('Territoires du nord-ouest', 'Territoires du Nord-Ouest') for location in x.split(', ')]))
# Export alpha index
df_index_new.to_csv(os.path.join(new_folder, 'ESA_website_FRA.csv'), index=False, encoding='latin-1')


# ------ Check if English and French IDs match ------
df_index_merge = pd.merge(df_eng_index_final, df_index_new, on='ID')

# English to French translation
translation = {
    'Title': 'Titre',
    'Content Type': 'Type de contenu',
    'Application Name': 'Nom de la demande',
    'Application Short Name': 'Nom abrégé de la demande',
    'Application Filing Date': 'Dépôt de la demande',
    'Company Name': 'Nom de la société',
    'Commodity': 'Produit de base',
    'File Name': 'Nom de fichier',
    'ESA Folder URL': 'URL du dossier de l\'ÉES',
    'Document Number': 'Numéro de document',
    'Data ID': 'Identificateur de données',
    'PDF Download URL': 'URL de téléchargement PDF',
    'Application Type (NEB Act)': 'Type de demande (Loi sur l\'Office national de l\'énergie)',
    'Pipeline Location': 'Emplacement du pipeline',
    'Hearing order': 'Ordonnance d\'audience',
    'Consultant Name': 'Nom du consultant',
    'Pipeline Status': 'État d\'avancement',
    'Regulatory Instrument(s)': 'Instruments réglementaires',
    'Application URL': 'URL de la demande',
    'Decision URL': 'URL de la décision',
    'ESA Section(s)': 'Sections de l\'EES',
    'ESA Section(s) Index': 'Index des sections de l\'ÉES',
    'ESA Section(s) Topics': 'Sujets des sections de l\'ÉES',
    'CSV Download URL': 'URL de téléchargement CSV',
    'PDF Page Number': 'Numéro de page PDF',
    'PDF Page Count': 'Nombre de pages PDF',
    'PDF Size': 'Taille PDF',
    'PDF Outline': 'Aperçu PDF',
    'Download folder name': 'Télécharger le nom du dossier'
}
for eng in translation:
    french = translation[eng]
    if eng in df_index_merge.columns and french in df_index_merge.columns:
        match_sum = df_index_merge[[eng, french]].apply(lambda x: x[eng] == x[french], axis=1).sum()
        print(eng, match_sum)

# quality check; delete temp files

df_index_new = pd.read_csv(os.path.join(new_folder, 'ESA_website_FRA.csv'), encoding='latin-1')

for project_path in df_index_new["Chemin d'accès pour télécharger le projet"].unique():
    if type(project_path) is str:
        project_folder = project_path.split('/')[-1]
        if project_folder not in os.listdir(new_folder_projects):
            print('Missing project folder: {}'.format(project_folder))

for table_path in df_index_new["Chemin d'accès pour télécharger le tableau"]:
    if type(table_path) is str:
        table_folder = table_path.split('/')[-1]
        if table_folder not in os.listdir(new_folder_tables):
            print('Missing table folder: {}'.format(table_folder))
