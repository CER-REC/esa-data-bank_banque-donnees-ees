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
df_meta = df_index.groupby(['Title', 'Data ID', 'PDF Page Number'])[['PDF Download URL', 'Download folder name']].first().reset_index()

df_merge_dup = df_merge_dup.merge(df_meta)
# df_merge_dup['Download folder name'].value_counts()
# brnswck              111
# strnmnln             104
# wlvrnrvrltrlllp       80
# lsmrkttlrvrcrssvr     70
# twrbrch               40
# tmx                   18
# nrgst                 13
# 2021ngtl              12
# vntg                  10
# kystnxl                5
# nrthcrrdr              5
# kmnrth                 3
# nrthmntn               3
# kystn                  2
# bkkn                   2
# dsnmnln                2
# 2017ngtl               2
# sprcrdg                2
# wstpthdlvr             2
# nrthrngtwy             1
# lbrtclppr              1
# kwn                    1
# sthrnlghts             1
# cshng                  1

df_merge_dup.to_csv('index_duplicates.csv', index=False)
