import pandas as pd
import numpy as np

# This is the data prepartion for quality check
# Refer to the jupyter notebook (QA_metrics.ipynb) for the analytical part where at the end we select a list of PDFs
# that we will exclude csvs files from

# ===== Data preparation for quality check =====
file = 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv'
df_index = pd.read_csv(file)

# add columns
for col in ['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']:
    df_index[col] = np.nan

for index, (csv_url) in df_index[['CSV Download URL']].itertuples():
    path = 'G:/ESA_downloads/copy_Bingjie/{}'.format('/'.join(csv_url.split('/')[-2:]))
    try:
        df_csv_temp = pd.read_csv(path, header=None)

        df_index.loc[index, 'csv_row_count'] = df_csv_temp.shape[0]
        df_index.loc[index, 'csv_column_count'] = df_csv_temp.shape[1]
        df_index.loc[index, 'csv_null_cell_count'] = df_csv_temp.isnull().sum().sum()

        count_cid_cell = 0
        for col in df_csv_temp.columns:
            if str(df_csv_temp[col].dtype) == 'object':
                count_cid_cell += df_csv_temp[col].str.contains('cid:').sum()
        df_index.loc[index, 'csv_cid_cell_count'] = count_cid_cell
    except:
        print(path)
        continue
        # Empty files:
        # G:/ESA_downloads/copy_Bingjie/tmx/2392795_369_1.csv
        # G:/ESA_downloads/copy_Bingjie/tmx/2393470_72_1.csv
        # G:/ESA_downloads/copy_Bingjie/nrgst/2968028_16_1.csv

# Calculate qa metrics
df_index['qa_single_row_or_col'] = df_index[['csv_row_count', 'csv_column_count']].apply(
    lambda x: x['csv_row_count'] == 1 or x['csv_column_count'] == 1, axis=1
)
df_index['qa_blank_cell_percent'] = df_index[['csv_row_count', 'csv_column_count', 'csv_null_cell_count']].apply(
    lambda x: round(100 * x['csv_null_cell_count'] / (x['csv_row_count'] * x['csv_column_count']), 2), axis=1
)
df_index['qa_cid_cell_percent'] = df_index[['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']].apply(
    lambda x: round(100 * x['csv_cid_cell_count'] / (x['csv_row_count'] * x['csv_column_count'] - x['csv_null_cell_count']), 2), axis=1
)

# Calculate duplicates
df_table_count = df_index.groupby(['Title', 'Data ID', 'PDF Page Number'])['CSV Download URL'].count()\
    .reset_index().rename(columns={'CSV Download URL': 'count'})
df_duplicate = df_table_count[df_table_count['count'] > 1]

df_index = df_index.merge(df_duplicate, how='left', on=['Title', 'Data ID', 'PDF Page Number'])
df_index['qa_duplicate'] = df_index['count'].notna()

df_index.to_csv('G:/ESA_downloads/index_qa_temp.csv', index=False)


# ====== Calculate the numbers of projects and pdfs during the whole process ======
file_all = 'Input_Files/Index_of_PDFs_for_Major_Projects_with_ESAs.csv'
df_all = pd.read_csv(file_all)

# df_all.shape
# (1902, 21)

# df_all['Application Short Name'].nunique()
# 37

df_index[['Application Short Name', 'Data ID']].nunique()
# Application Short Name 38, Data ID 860
# The difference is the Keystone project

df_fig = pd.read_csv('F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv')
# (38025, 31)

df_project_all = df_all.groupby('Application Short Name')['Data ID'].nunique().reset_index().rename(columns={'Data ID': 'pdf_count_all'})
df_project_table_fig = df_fig.groupby('Application Short Name')['Data ID'].nunique().reset_index().rename(columns={'Data ID': 'pdf_count_table_fig'})
df_project_table = df_index.groupby('Application Short Name')['Data ID'].nunique().reset_index().rename(columns={'Data ID': 'pdf_count_table'})

df_project_all.merge(df_project_table_fig, how='outer').merge(df_project_table, how='outer')\
    .to_csv('project_pdf_count.csv', index=False)

