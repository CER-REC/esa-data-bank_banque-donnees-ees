import pandas as pd
import numpy as np

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

# df_index.to_csv('G:/ESA_downloads/index_qa_temp.csv', index=False)
