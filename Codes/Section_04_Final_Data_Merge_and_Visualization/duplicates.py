import pandas as pd

file = 'G:/ESA_downloads/copy_Bingjie/ESA_website_ENG.csv'

df_index = pd.read_csv(file)
# df_index.shape
# (28891, 32)

df_table_count = df_index.groupby(['Title', 'Data ID'])['CSV Download URL'].count()\
    .reset_index().rename(columns={'CSV Download URL': 'count'})
# df_table_count.shape
# (15151, 3)

df_table_count_2 = df_index.groupby(['Title', 'Data ID', 'PDF Page Number'])['CSV Download URL'].count()\
    .reset_index().rename(columns={'CSV Download URL': 'count'})

df_table_count_3 = df_index.groupby(['Title', 'Data ID', 'PDF Page Number'])['CSV Download URL'].apply(lambda x: '; '.join(x))\
    .reset_index()

df_merge = df_table_count_2.merge(df_table_count_3)
# df_merge.shape
# (28049, 5)

df_merge_dup = df_merge[df_merge['count'] > 1]
# df_merge_dup.shape
# (491, 4)
# # df_merge_dup['count'].value_counts()
# 2    296
# 3    123
# 4     30
# 5     21
# 6      9
# 8      5
# 7      5
# 9      2

df_merge_dup = df_merge_dup.join(df_index[['PDF Download URL', 'Application Name', 'Application Filing Date', 'Consultant Name', 'Download folder name']], how='left')

df_merge_dup.sort_values(['Application Filing Date', 'PDF Page Number'], ascending=[False, True])\
    .to_csv('index_duplicates.csv', index=False)
