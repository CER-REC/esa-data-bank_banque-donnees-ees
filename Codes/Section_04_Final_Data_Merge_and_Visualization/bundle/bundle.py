import pandas as pd
import os
import multiprocessing

from Codes.Section_04_Final_Data_Merge_and_Visualization.bundle.bundle_utilites \
    import bundle_for_project, bundle_for_table


index_filepath_eng = \
    '//luxor/data/Branch/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG_2021_01_28.csv'
csv_file_folder = '//luxor/data/Branch/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_latest_ENG'
readme_project_filepath = '//luxor/data/Board/ESA_downloads/README-ENG-projects.txt'
readme_table_filepath = '//luxor/data/Board/ESA_downloads/README-ENG-tables.txt'

# Create a new folder as the destination for downloading files
new_folder = os.path.join('//luxor/data/Board/ESA_downloads/', 'download_Bingjie_Mar262021')
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
df_index_raw = pd.read_csv(index_filepath_eng)

# Create a temporary column in the index dataframe as table identification
df_table_id = df_index_raw.groupby(['Title', 'Data ID']).size()\
    .reset_index().drop(columns=[0])\
    .reset_index().rename(columns={'index': 'ID'})
df_index_raw = df_index_raw.merge(df_table_id, left_on=['Title', 'Data ID'], right_on=['Title', 'Data ID'])

# Remove bad csvs
df_index = df_index_raw[~df_index_raw['bad_csv']]

# Add a new column - Project Download Path
df_index['Project Download Path'] = df_index['Download folder name']\
    .apply(lambda x: '/projects/{}.zip'.format(x))

# Add a new column - Table Download Path
df_table_filename = df_index.sort_values(['PDF Page Number'])\
    .groupby('ID')['filename'].first().reset_index().rename(columns={'filename': 'Table Name'})
df_table_filename['Table Name'] = df_table_filename['Table Name']\
    .apply(lambda x: x.replace('.csv', '').replace('--', '-'))
df_index = df_index.merge(df_table_filename, left_on='ID', right_on='ID')
df_index['Table Download Path'] = df_index['Table Name']\
    .apply(lambda x: '/tables/{}.zip'.format(x))

# Remove ',All' from Pipeline Location, ESA Section(s) Topics
df_index['Pipeline Location'] = df_index['Pipeline Location']\
    .apply(lambda x: ', '.join([location for location in x.split(', ') if location != 'All']))
df_index['ESA Section(s) Topics'] = df_index['ESA Section(s) Topics']\
    .apply(lambda x: ', '.join([section for section in x.split(', ') if section != 'All']) if type(x) is str else x)
# Update ESA Download URls
df_index['ESA Folder URL'] = df_index['ESA Folder URL'].apply(lambda x: x.replace('LoadResult', 'View'))

# Prepare a list of column names for the final index files
columns_index = [col for col in df_index.columns.to_list() if col not in (
    'Table Name', 'CSV Download URL', 'Download folder name', 'Zipped Project Link', 'Unnamed: 0',
    'Unnamed: 0.1', 'Index', 'filename', 'old_filename', 'Data ID', 'bad_csv')]


# =============================== Create Project Download Files ==============================
args = [(df_index, project_folder_name, new_folder_projects, csv_file_folder, columns_index, readme_project_filepath)
        for project_folder_name in sorted(df_index['Download folder name'].unique().tolist())]
pool = multiprocessing.Pool()
pool.starmap(bundle_for_project, args)
pool.close()

# =============================== Create Table Download Files ===============================
args_table = [(df_index, table_id, new_folder_tables, csv_file_folder, columns_index, readme_table_filepath)
              for table_id in sorted(df_index['ID'].unique().tolist())]
pool = multiprocessing.Pool()
pool.starmap(bundle_for_table, args_table)
pool.close()

# =============================== Create Master Index File ===============================
# Added figures back to alpha index file
df_index_with_figure = pd.read_excel('//luxor/data/Branch/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.xlsx')
figure_columns = columns_index.copy()
figure_columns.remove('ID')
figure_columns.remove('Project Download Path')
figure_columns.remove('Table Download Path')
df_figure = df_index_with_figure[df_index_with_figure['Content Type'] == 'Figure'][figure_columns]
df_figure['ID'] = df_figure.index + df_index_raw['ID'].max() + 1
df_figure['Application Filing Date'] = df_figure['Application Filing Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

# Add bad tables
bad_table_columns = columns_index.copy()
bad_table_columns.remove('Project Download Path')
bad_table_columns.remove('Table Download Path')
df_table_bad = df_index_raw[df_index_raw['bad_csv']].sort_values(['ID', 'PDF Page Number']).groupby('ID').first()\
    .reset_index()[bad_table_columns]
df_table_bad['Good Quality'] = False

# Concatenate all tables
df_table = df_index.sort_values(['ID', 'PDF Page Number']).groupby('ID').first()\
    .reset_index()[columns_index]
df_table['Good Quality'] = True

df_index_new = pd.concat([df_figure, df_table, df_table_bad])

# Remove ',All' from Pipeline Location, ESA Section(s) Topics
df_index_new['Pipeline Location'] = df_index_new['Pipeline Location']\
    .apply(lambda x: ', '.join([location for location in x.split(', ') if location != 'All']))
df_index_new['ESA Section(s) Topics'] = df_index_new['ESA Section(s) Topics']\
    .apply(lambda x: ', '.join([section for section in x.split(', ') if section != 'All']) if type(x) is str else x)
# Update ESA Download URls
df_index_new['ESA Folder URL'] = df_index_new['ESA Folder URL'].apply(lambda x: x.replace('LoadResult', 'View'))

# Export alpha index
df_index_new.to_csv(os.path.join(new_folder, 'ESA_website_ENG.csv'), index=False)


# Quality check

df_index_new = pd.read_csv(os.path.join(new_folder, 'ESA_website_ENG.csv'))

for project_path in df_index_new['Project Download Path'].unique():
    if type(project_path) is str:
        project_folder = project_path.split('/')[-1]
        if project_folder not in os.listdir(new_folder_projects):
            print('Missing project folder: {}'.format(project_folder))

for table_path in df_index_new['Table Download Path']:
    if type(table_path) is str:
        table_folder = table_path.split('/')[-1]
        if table_folder not in os.listdir(new_folder_tables):
            print('Missing table folder: {}'.format(table_folder))

df_index_new['table missing'] = df_index_new['Table Download Path']\
    .apply(lambda x: x.split('/')[-1] not in os.listdir(new_folder_tables) if type(x) is str else x)

for table_id in df_index_new[df_index_new['table missing'] == True]['ID']:
    print(table_id)
    bundle_for_table(df_index, table_id, new_folder_tables, csv_file_folder, columns_index, readme_table_filepath)

for table_path in df_index_new[df_index_new['table missing'] == True]['Table Download Path']:
    if type(table_path) is str:
        table_folder = table_path.split('/')[-1]
        if table_folder not in os.listdir(new_folder_tables):
            print('Missing table folder: {}'.format(table_folder))

# Check if certain attributes stay the same for projects
df = pd.read_csv('G:/ESA_downloads/download_Bingjie_Mar262021/ESA_website_ENG.csv')
df_fra = pd.read_csv('G:/ESA_downloads/download_Bingjie_Mar262021_fra/ESA_website_FRA.csv', encoding='latin-1')

df_project = df.groupby(['Application Short Name'])[[
    'Application Name',
    'Application Filing Date',
    'Company Name',
    'Commodity',
    'Application Type (NEB Act)',
    'Pipeline Location',
    'Hearing order',
    'Consultant Name',
    'Pipeline Status',
    'Application URL',
    'Project Download Path'
    ]].nunique()

df_project_fra = df_fra.groupby(['Nom abrégé de la demande'])[[
    'Nom de la demande',
    'Dépôt de la demande',
    'Nom de la société',
    'Produit de base',
    'Type de demande (Loi sur l\'Office national de l\'énergie)',
    'Emplacement du pipeline',
    'Ordonnance d\'audience',
    'Nom du consultant',
    'État d\'avancement',
    'URL de la demande',
    "Chemin d'accès pour télécharger le projet"
]].nunique()
