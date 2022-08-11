import pandas as pd
import numpy as np
import os
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))

# paths to data
REPO_ROOT = Path(__file__).parents[2].resolve()
INTERMEDIATE_INDEX_PATH = REPO_ROOT / "data" / "interim" / "Intermediate_Index_Files"
CSVS_PATH = REPO_ROOT / "data" / "processed" / "csvs" / "new_projects"
RENAMED_CSVS_PATH = "G:/ESA_downloads/BERDI_FR/rename_csv/"

df_index = pd.read_csv(str(INTERMEDIATE_INDEX_PATH / "esa_vecs_labeled_FR.csv"), encoding = 'cp1252')  # 502, 55

df_index['Download folder name'] = 'snclr'

df_index_table = df_index[df_index['Content Type'] == 'Table']  # 473, 56


# # #################### add Good Quality column ##########################
# # read in csv files and calculate row count, column count, number of null cells and number of cells with 'cid'
for col in ['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']:
    df_index_table[col] = np.nan

for index, (csv_file_name) in df_index_table[['csvFileName']].itertuples():
    path = str(CSVS_PATH / "{}").format(csv_file_name)
    try:
        df_csv_temp = pd.read_csv(path, header=None)

        df_index_table.loc[index, 'csv_row_count'] = df_csv_temp.shape[0]
        df_index_table.loc[index, 'csv_column_count'] = df_csv_temp.shape[1]
        df_index_table.loc[index, 'csv_null_cell_count'] = df_csv_temp.isnull().sum().sum()

        count_cid_cell = 0
        for col in df_csv_temp.columns:
            if str(df_csv_temp[col].dtype) == 'object':
                count_cid_cell += df_csv_temp[col].contains('cid:').sum()
        df_index_table.loc[index, 'csv_cid_cell_count'] = count_cid_cell
    except:
        #print(path)
        continue

# Calculate qa metrics
# - single row or col: if a csv file has only one row or one column
# - blank cell percent: percentage of empty cells
# - cid cell percent: percentage of cells with 'cid'
df_index_table['qa_single_row_or_col'] = df_index_table[['csv_row_count', 'csv_column_count']].apply(
    lambda x: x['csv_row_count'] == 1 or x['csv_column_count'] == 1, axis=1
)
df_index_table['qa_blank_cell_percent'] = df_index_table[['csv_row_count', 'csv_column_count', 'csv_null_cell_count']].apply(
    lambda x: round(100 * x['csv_null_cell_count'] / (x['csv_row_count'] * x['csv_column_count']), 2), axis=1
)
df_index_table['qa_cid_cell_percent'] = df_index_table[['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']].apply(
    lambda x: round(100 * x['csv_cid_cell_count'] / (x['csv_row_count'] * x['csv_column_count'] - x['csv_null_cell_count']), 2), axis=1
)

# Calculate qa metric:
# - duplicate: if this csv file is a duplicate (there are other csv files with the same title on the same pdf page)
df_table_count = df_index_table.groupby(['Titre', 'Data ID', 'PDF Page Number'])['csvFileName'].count()\
    .reset_index().rename(columns={'csvFileName': 'count'})
df_duplicate = df_table_count[df_table_count['count'] > 1]

df_index_table = df_index_table.merge(df_duplicate, how='left', on=['Titre', 'Data ID', 'PDF Page Number'])
df_index_table['qa_duplicate'] = df_index_table['count'].notna()

# Calculate metrics at PDF level
# i.e. single_%: the percentage of csv files with  one row or one column out of all the csv files extracted from the PDF
df_index_table['qa_blank'] = df_index_table['qa_blank_cell_percent'] > 72
df_index_table['qa_cid'] = df_index_table['qa_cid_cell_percent'] > 80
df_index_table['qa_any'] = df_index_table[['qa_blank', 'qa_cid', 'qa_duplicate', 'qa_single_row_or_col']].any(axis=1)


df_pdf = df_index_table.groupby('PDF Download URL')[['qa_single_row_or_col', 'qa_blank', 'qa_cid', 'qa_duplicate','qa_any']].sum().reset_index()
df_pdf_count = df_index_table.groupby('PDF Download URL')['csvFileName'].count().reset_index().rename(columns={'csvFileName': 'total_csv'})

df_pdf = df_pdf.merge(df_pdf_count)
df_pdf['single_%'] = df_pdf[['qa_single_row_or_col', 'total_csv']].apply(lambda x: 100*round(x['qa_single_row_or_col']/x['total_csv'], 2), axis=1)
df_pdf['blank_%'] = df_pdf[['qa_blank', 'total_csv']].apply(lambda x: 100*round(x['qa_blank']/x['total_csv'], 2), axis=1)
df_pdf['cid_%'] = df_pdf[['qa_cid', 'total_csv']].apply(lambda x: 100*round(x['qa_cid']/x['total_csv'], 2), axis=1)
df_pdf['duplicate_%'] = df_pdf[['qa_duplicate', 'total_csv']].apply(lambda x: 100*round(x['qa_duplicate']/x['total_csv'], 2), axis=1)
df_pdf['any_%'] = df_pdf[['qa_any', 'total_csv']].apply(lambda x: 100*round(x['qa_any']/x['total_csv'], 2), axis=1)

# df_pdf.sort_values('any_%', ascending=False)
# We will mark the csv files from one PDF as bad quality if the PDF generated over 20% problematic csv files
bad_pdf_lst = df_pdf[df_pdf['any_%'] > 20]['PDF Download URL'].tolist()
df_index['Good Quality'] = df_index.apply(lambda x:
                                          x['Content Type'] == 'Table' and x['PDF Download URL'] not in bad_pdf_lst, axis=1)
df_index.loc[df_index['Content Type'] != 'Table', 'Good Quality'] = None
df_index[df_index['Good Quality'] == True].shape  # 378, 57
print(df_index[df_index['Good Quality'] == True].shape)

# #################### rename csv file names ##########################
df_index_table_good_quality = df_index[df_index['Good Quality'] == True]
# Create a column csvFileNameRenamed for the new csv file name
df_index_table_good_quality['csvFileNameRenamedTemp'] = \
    df_index_table_good_quality.apply(lambda x: x['Download folder name'] + '_' +
                                      x['Titre'].lower().replace('(', '').replace(')', '').replace(' ', '-')\
                                      .replace('.', '-').replace(',', '').replace('\\', '').replace('/', '').replace('[^\w+-]', '')[:50],
                                      axis=1)
df_index_table_good_quality['rownumber'] = df_index_table_good_quality.groupby(['csvFileNameRenamedTemp']).cumcount() + 1
df_index_table_good_quality['csvFileNameRenamed'] = \
    df_index_table_good_quality.apply(lambda x: x['csvFileNameRenamedTemp'] +
                                                '_pt-' + str(x['rownumber']) +
                                                '_pg-' + str(x['PDF Page Number']) +
                                                '_num-du-doc-' + str(x['Document Number']) + '.csv', axis=1)

for index, row in df_index_table_good_quality.iterrows():
    if os.path.isfile(str(CSVS_PATH) + '/' + row['csvFileName']):
        shutil.copy(str(CSVS_PATH) + '/' + row['csvFileName'], RENAMED_CSVS_PATH + row['csvFileNameRenamed'])

df_index_all = pd.concat([df_index_table_good_quality,   # 378, 60  good quality table
                          df_index[df_index['Content Type'] != 'Table'],  # 29, 57  figures & alignment sheets
                          df_index[(df_index['Content Type'] == 'Table') & (df_index['Good Quality'] == False)]]
                         # 95, 57 bad quality table
                         )

df_index_all.to_csv(RENAMED_CSVS_PATH + 'index_csv_renamed.csv', encoding = 'utf-8-sig', index=False)

# #################################### Preprocess before creating bundles ####################################
# Remove columns
# o	Document Number
# o	Regulatory Instrument(s)
# o	ESA Section(s) Index
# o	ESA Section(s) Topics
# o	PDF Page Count
# o	PDF Size
# o	PDF Outline
# o	Good Quality

readme_project_filepath = 'G:/ESA_downloads/README-FRA-projects.txt'
readme_table_filepath = 'G:/ESA_downloads/README-FRA-tables.txt'

new_folder = os.path.join('G:/ESA_downloads/BERDI_FR/', 'fr')
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

# Create a temporary column in the index dataframe as table identification - Table ID
df_index_all = pd.read_csv('G:/ESA_downloads/BERDI_FR/rename_csv/index_csv_renamed.csv')
df_index_all = df_index_all.drop(columns=['ID'])
df_index_all['Hearing Order'] = None
df_index_all.rename(columns={
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
    'Application Type': 'Type de demande',
    'Pipeline Location': 'Emplacement du pipeline',
    'Hearing Order': 'Ordonnance d\'audience',
    'Consultant Name': 'Nom du consultant',
    'Pipeline Status': 'État d\'avancement',
    'Regulatory Instrument(s)': 'Instruments réglementaires',
    'Application URL': 'URL de la demande',
    'Decision URL': 'URL de la décision',
    'ESA Section(s) Index': 'Index des sections de l\'ÉES',
    'Topics': 'Sujets des sections de l\'ÉES',
    'PDF Page Number': 'Numéro de page PDF',
    'PDF Page Count': 'Nombre de pages PDF',
    'PDF Size (bytes)': 'Taille PDF',
    'Outline Present': 'Aperçu PDF',
    'Landscape, terrain, and weather': 'Paysage, terrain et conditions météorologiques',
    'Soil': 'Sol',
    'Plants': 'Plantes',
    'Water': 'Eau',
    'Fish': 'Poissons',
    'Wetlands': 'Milieux humides',
    'Wildlife': 'Faune',
    'Species at Risk': 'Espèces en péril',
    'Greenhouse gas emissions': 'Émissions de gaz à effet de serre',
    'Air emissions': 'Émissions atmosphériques',
    'Noise': 'Bruit',
    'Electricity and electromagnetism': 'Électricité et électromagnétisme',
    'Proximity to people': 'Lieux habités à proximité',
    'Archaeological, paleontological, historical, and culturally significant sites and resources': 'Sites et ressources archéologiques, paléontologiques, historiques ou importants sur le plan culturel',
    'Human access to boats and waterways': 'Activités à bord d\'embarcation ou sur des voies navigables',
    'Indigenous land, water, and air use': 'Utilisation des terres, de l\'eau et du plein air par les Autochtones',
    'Impact to social and cultural well-being': 'Incidences sur le bien-être social et culturel',
    'Impact to human health and viewscapes': 'Incidence sur la santé humaine et le panorama',
    'Social, cultural, economic infrastructure and services': 'Infrastructure et services sociaux, culturels et économiques',
    'Economic Offsets and Impact': 'Compensations et répercussions économiques',
    'Environmental Obligations': 'Obligations en matière d\'environnement',
    'Treaty and Indigenous Rights': 'Droits ancestraux et issus de traités',
    'Download folder name': 'Télécharger le nom du dossier'
}, inplace = True)
# Update French ESA Folder URL
df_index_all['URL du dossier de l\'ÉES'] = df_index_all['URL du dossier de l\'ÉES']\
    .apply(lambda x: x.replace('https://apps.cer-rec.gc.ca/REGDOCS/Item/View/','https://apps.cer-rec.gc.ca/REGDOCS/Élément/Afficher/'))

# Update French Application URL
df_index_all['URL de la demande'] = df_index_all['URL de la demande']\
    .apply(lambda x: x.replace('https://apps.cer-rec.gc.ca/REGDOCS/Item/View/','https://apps.cer-rec.gc.ca/REGDOCS/Élément/Afficher/'))

# Update French Decision URL
df_index_all['URL de la décision'] = df_index_all['URL de la décision']\
    .apply(lambda x: x.replace('https://apps.cer-rec.gc.ca/REGDOCS/Item/View/','https://apps.cer-rec.gc.ca/REGDOCS/Élément/Afficher/'))

# Update Commodity Labels
df_index_all['Produit de base'].replace({'Gas': 'Gaz', 'Oil': 'Pétrole'}, inplace = True)

# Update Content Type Labels
df_index_all['Type de contenu'].replace({'Table': 'Tableau', 'Alignment Sheet': 'Carte-tracé'}, inplace = True)
print(df_index_all.columns)

df_index_all_table = df_index_all[df_index_all['Type de contenu'] == 'Tableau']
df_table_id = df_index_all_table.groupby(['Titre', 'Identificateur de données']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'Table ID'})
df_index_all_table = df_index_all_table.merge(df_table_id, left_on=['Titre', 'Identificateur de données'], right_on=['Titre', 'Identificateur de données'])

# Add a new column - Project Download Path
df_index_all_table_good = df_index_all_table[df_index_all_table['Good Quality'] == True]
df_index_all_table_good['Chemin d\'accès pour télécharger le projet'] = df_index_all_table_good['Télécharger le nom du dossier']\
    .apply(lambda x: '/projects/{}.zip'.format(x))

# Add a new column - Table Download Path
df_table_filename = df_index_all_table_good.sort_values(['Numéro de page PDF'])\
    .groupby('Table ID')['csvFileNameRenamed'].first()\
    .reset_index().rename(columns={'csvFileNameRenamed': 'Table Name'})
df_table_filename['Table Name'] = df_table_filename['Table Name']\
    .apply(lambda x: x.replace('.csv', '').replace('--', '-'))
df_index_all_table_good = df_index_all_table_good.merge(df_table_filename, left_on='Table ID', right_on='Table ID')
df_index_all_table_good['Chemin d\'accès pour télécharger le tableau'] = df_index_all_table_good['Table Name']\
    .apply(lambda x: '/tables/{}.zip'.format(x))

df_index_all_table_good.rename(columns={"csvFileNameRenamed": "Nom du CSV"}, inplace = True)

# Columns: the data of these columns will be added to read files and project index files
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


#################### Create Project and Table Download Files ####################
# import multiprocessing
from berdi.Section_04_Final_Data_Merge_and_Visualization.bundle.bundle_utilites import bundle_for_project, bundle_for_table

# Create project download zip files
# is_french = True
# args = [(df_index_all_table_good, project_folder_name, new_folder_projects, RENAMED_CSVS_PATH, columns, readme_project_filepath, is_french)
#          for project_folder_name in sorted(df_index_all_table_good['Télécharger le nom du dossier'].unique().tolist())]
# pool = multiprocessing.Pool()
# pool.starmap(bundle_for_project, args)
# pool.close()

for project_folder_name in sorted(df_index_all_table_good['Télécharger le nom du dossier'].unique().tolist()):
    bundle_for_project(df_index_all_table_good, project_folder_name, new_folder_projects, RENAMED_CSVS_PATH, columns, readme_project_filepath, is_french = True)

# Create table download zip files
# args_table = [(df_index_all_table_good, table_id, new_folder_tables, RENAMED_CSVS_PATH, columns, readme_table_filepath, is_french)
#              for table_id in sorted(df_index_all_table_good['Table ID'].unique().tolist())]
# pool = multiprocessing.Pool()
# pool.starmap(bundle_for_table, args_table)
# pool.close()

for table_id in sorted(df_index_all_table_good['Table ID'].unique().tolist()):
    bundle_for_table(df_index_all_table_good, table_id, new_folder_tables, RENAMED_CSVS_PATH, columns, readme_table_filepath, is_french = True)


# #################### Prepare final index file ###########################
vec_columns = [
    'Paysage, terrain et conditions météorologiques',
    'Sol',
    'Plantes',
    'Eau',
    'Poissons',
    'Milieux humides',
    'Faune',
    'Espèces en péril',
    'Émissions de gaz à effet de serre',
    'Émissions atmosphériques',
    'Bruit',
    'Électricité et électromagnétisme',
    'Lieux habités à proximité',
    'Sites et ressources archéologiques, paléontologiques, historiques ou importants sur le plan culturel',
    'Activités à bord d\'embarcation ou sur des voies navigables',
    'Utilisation des terres, de l\'eau et du plein air par les Autochtones',
    'Incidences sur le bien-être social et culturel',
    'Incidence sur la santé humaine et le panorama',
    'Infrastructure et services sociaux, culturels et économiques',
    'Compensations et répercussions économiques',
    'Obligations en matière d\'environnement',
    'Droits ancestraux et issus de traités'
]

# Create column Page Count per table
df_page_count = df_index_all_table.groupby('Table ID')\
    .apply(lambda x: x['Numéro de page PDF'].max() - x['Numéro de page PDF'].min() + 1)\
    .reset_index().rename(columns={0: 'Page Count'})

# Create vec values per table (aggregating vec values of the csvs belonging to the same table)
df_vec = df_index_all_table.groupby('Table ID')[vec_columns].sum().reset_index()

# Create a dataframe for the bad quality tables
df_index_table_bad = df_index_all_table[(df_index_all_table['Type de contenu'] == 'Tableau') &
                                        (df_index_all_table['Good Quality'] == False)]\
    .sort_values(['Table ID', 'Numéro de page PDF']).groupby('Table ID').first().reset_index()
df_index_table_bad = df_index_table_bad.merge(df_page_count, on='Table ID')
df_index_table_bad = df_index_table_bad.drop(columns=vec_columns)
df_index_table_bad = df_index_table_bad.merge(df_vec, on='Table ID')

columns_table_bad = [col for col in columns if col not in ('Chemin d\'accès pour télécharger le projet', 'Chemin d\'accès pour télécharger le tableau')]
columns_table_bad.append('Page Count')
columns_table_bad.extend(vec_columns)
df_index_table_bad = df_index_table_bad[columns_table_bad]

# Create a dataframe for figure & alignment sheets
df_index_figure = df_index_all[df_index_all['Type de contenu'] != 'Tableau']
df_index_figure['Page Count'] = 1
df_index_figure = df_index_figure[columns_table_bad]

# Create a dataframe for the good quality tables
df_index_table_good = df_index_all_table_good \
    .sort_values(['Table ID', 'Numéro de page PDF']).groupby('Table ID').first().reset_index()
df_index_table_good = df_index_table_good.merge(df_page_count, on='Table ID')
df_index_table_good = df_index_table_good.drop(columns=vec_columns)
df_index_table_good = df_index_table_good.merge(df_vec, on='Table ID')
columns_table_good = columns_table_bad + ['Chemin d\'accès pour télécharger le projet', 'Chemin d\'accès pour télécharger le tableau']
df_index_table_good = df_index_table_good[columns_table_good]

# Concatenate three dataframes
df_index_final = pd.concat([df_index_table_good, df_index_table_bad, df_index_figure])
print(df_index_final.columns)

# Add columns ID, Data ID, Thumbnail Location
df_index_final['ID'] = df_index_final.index + 21425 ## make sure index matches with english
df_index_final['Data ID'] = df_index_final['URL de téléchargement PDF'].apply(lambda x: x.split('/')[-1])
df_index_final['Thumbnail Location'] = df_index_final.apply(lambda x: 'thumbnails/{}_{}.jpg'.format(x['Data ID'], x['Numéro de page PDF']), axis=1)

# Save the final index file (per row per table)
df_index_final.to_csv('G:/ESA_downloads/BERDI_FR/fr/ESA_website_FRA.csv', index=False, encoding = 'utf-8-sig')


# # ############################# create thumbnails #############################
# import fitz

# for data_id in df_index_final['Data ID'].unique().tolist():
#     pdf_file_path = 'data/raw/pdfs/{}.pdf'.format(data_id)
#     for page_number in df_index_final[df_index_final['Data ID'] == data_id]['PDF Page Number'].unique().tolist():
#         doc = fitz.open(pdf_file_path)
#         page = doc.load_page(page_number-1)
#         pix = page.get_pixmap(dpi=96)
#         pix.save('data/download_internal_Aug2022/thumbnails/{}_{}.jpg'.format(data_id, page_number))


# ############################# Clean the old project files #############################
import zipfile
import tempfile

df_index_last = pd.read_csv('G:/ESA_downloads/ESA_website_FRA_20210923.csv')

df_index_last = df_index_last.rename(columns={'Type de demande (Loi sur l\'Office national de l\'énergie)': 'Type de demande'})
df_index_last_tmp = df_index_last[columns]

# Clean the project index files to only include the required columns
for project_file in df_index_last[df_index_last['Chemin d\'accès pour télécharger le projet'].notna()]['Chemin d\'accès pour télécharger le projet'].unique().tolist():
    print(project_file)
    project_zipfile = 'data/download_internal_July2022/en' + project_file
    tmpfd, tmpfile = tempfile.mkstemp(dir=os.path.dirname(project_zipfile))
    os.close(tmpfd)
    with zipfile.ZipFile(project_zipfile, 'r') as zin:
        with zipfile.ZipFile(tmpfile, 'w') as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                if not item.filename.endswith('.csv'):
                    # copy all the files to the temp zip file except the project index csv file
                    zout.writestr(item, zin.read(item.filename))
    os.remove(project_zipfile)  # delete the old project zip file
    os.rename(tmpfile, project_zipfile)  # rename the temp file to the project zip file
    project = project_zipfile.split('/')[-1].replace('.zip', '')
    with zipfile.ZipFile(project_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        csvdata = df_index_last_tmp[df_index_last_tmp['Project Download Path'] == project_file].to_csv(index=False)
        zf.writestr(project + '/INDEX_PROJECT.csv', csvdata)  # save a new index file to the project zip file

# # Clean the table read files to only include the required columns
# for table_file in df_index_last[df_index_last['Table Download Path'].notna()]['Table Download Path'].unique().tolist():
#     print(table_file)
#     table_zipfile = 'data/download_internal_July2022/en' + table_file
#     tmpfd, tmpfile = tempfile.mkstemp(dir=os.path.dirname(table_zipfile))
#     os.close(tmpfd)
#     with zipfile.ZipFile(table_zipfile, 'r') as zin:
#         with zipfile.ZipFile(tmpfile, 'w') as zout:
#             zout.comment = zin.comment
#             for item in zin.infolist():
#                 if not item.filename.endswith('.txt'):
#                     # copy all the files to the temp zip file except the readme.txt file
#                     zout.writestr(item, zin.read(item.filename))
#     os.remove(table_zipfile)  # delete the old table zip file
#     os.rename(tmpfile, table_zipfile)  # rename the temp file to the table zip file

#     # create the table readme.txt
#     df_table = df_index_last_tmp[df_index_last_tmp['Table Download Path'] == table_file]
#     metadata = open(readme_table_filepath, 'r').read()
#     for col in columns:
#         if col == 'PDF Page Number' and df_table[col].min() != df_table[col].max():
#             metadata += '{}: {} - {}\n'.format(col, df_table[col].min(), df_table[col].max())
#         else:
#             metadata += '{}: {}\n'.format(col, df_table.iloc[0][col])
#     # save the table readme file to the new table zip file
#     with zipfile.ZipFile(table_zipfile, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
#         zf.writestr('readme.txt', metadata)

# columns_indexfile = pd.read_csv('data/download_internal_Aug2022/en/ESA_website_ENG.csv').columns.tolist()
# # Save only the required columns for the index file of data update #1&2
# df_index_last[columns_indexfile].to_csv('data/download_internal_July2022/en/ESA_website_ENG_20220727_final.csv', index=False)


# # ############################# Combine the merged index files #############################
# # Concatenate the index file of date update #1&2 and data update #3
# pd.concat([
#     pd.read_csv('data/download_internal_July2022/en/ESA_website_ENG_20220727_final.csv'),
#     pd.read_csv('data/download_internal_Aug2022/en/ESA_website_ENG.csv')]).sort_values('ID')\
#     .to_csv('data/download_internal_Aug2022_merged/en/ESA_website_ENG.csv', index=False)
