import pandas as pd
from csv_diff import load_csv, compare

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

df_index_dup = df_index.merge(df_merge[df_merge['count'] > 1], how='left', on=['Title', 'Data ID', 'PDF Page Number'])
df_index_dup['duplicate'] = df_index_dup['count'].notna()
# df_index_dup['duplicate'].value_counts()
# False     27558
# True      1333

df_project_dup = df_index_dup.groupby('Download folder name')['duplicate'].sum().reset_index()
df_project_count = df_index_dup.groupby('Download folder name')['duplicate'].count().reset_index().rename(columns={'duplicate': 'count'})
df_project_count = df_project_count.merge(df_project_dup, how='left')

df_project_count['percent'] = df_project_count.apply(lambda x: round(x['duplicate']/x['count']*100, 2), axis=1)
df_project_count.sort_values('percent', ascending=False)
#    Download folder name  count  duplicate  percent
# 3               brnswck    379        275    72.56
# 35      wlvrnrvrltrlllp    427        240    56.21
# 20    lsmrkttlrvrcrssvr    415        203    48.92
# 31             strnmnln    694        329    47.41
# 33              twrbrch    565        112    19.82
# 34                 vntg    531         20     3.77
# 1              2021ngtl    768         24     3.12
# 4                 cshng     73          2     2.74
# 12                  kwn     96          2     2.08
# 11               kmnrth    305          6     1.97
# 23            nrthcrrdr    636         12     1.89
# 14              kystnxl    829         10     1.21
# 2                  bkkn    337          4     1.19
# 37           wstpthdlvr    351          4     1.14
# 7               dsnmnln    397          4     1.01
# 24             nrthmntn    610          6     0.98
# 32                  tmx   3874         36     0.93
# 30           sthrnlghts    270          2     0.74
# 13                kystn    624          4     0.64
# 28              sprcrdg    647          4     0.62
# 22                nrgst   5763         26     0.45
# 16            lbrtclppr    524          2     0.38
# 0              2017ngtl   1869          4     0.21
# 25           nrthrngtwy   1152          2     0.17

df_pdf_dup = df_index_dup.groupby('Data ID')['duplicate'].sum().reset_index()
df_pdf_count = df_index_dup.groupby('Data ID')['duplicate'].count().reset_index().rename(columns={'duplicate': 'count'})
df_pdf_count = df_pdf_count.merge(df_pdf_dup, how='left')

df_pdf_count['percent'] = df_pdf_count.apply(lambda x: round(x['duplicate']/x['count']*100, 2), axis=1)
# df_pdf_count.shape (860, 4)
df_pdf = df_index[['Data ID', 'PDF Download URL', 'Download folder name']].drop_duplicates()
df_pdf_count = df_pdf_count.merge(df_pdf, on='Data ID')

df_pdf_count = df_pdf_count.sort_values('percent', ascending=False)
# df_pdf_count[df_pdf_count['percent'] > 50].shape  (9, 6)
# df_pdf_count[df_pdf_count['percent'] > 10].shape  (32, 6)

# Data ID  count  duplicate  percent
# 11    408937    379        275    72.56
# 412  2445655    276        198    71.74
# 264   702747    187        114    60.96
# 205   667050      7          4    57.14
# 260   702730     16          9    56.25
# ..       ...    ...        ...      ...
# 301   895339      5          0     0.00
# 302  1059614     29          0     0.00
# 303  1059803     24          0     0.00
# 304  1059806     41          0     0.00
# 859  3892459    161          0     0.00

# ======================================== Compare csv files ========================================
for index, item in df_merge_dup.iterrows():
    csv_files = item['CSV Download URL'].split('; ')
    csv_files = [file.replace('http://www.cer-rec.gc.ca/esa-ees', 'G:/ESA_downloads/copy_Bingjie') for file in
                 csv_files]
    count_error = 0
    for i in range(len(csv_files)):
        for j in range(i):
            try:
                diff = compare(load_csv(open(csv_files[i])), load_csv(open(csv_files[j])))
                if not (diff['added'] or diff['removed'] or diff['changed'] or diff['columns_added'] or diff['columns_removed']):
                    print('*** Same CSV files: {}, {}'.format(csv_files[i], csv_files[j]))
                    print('PDF Download URL: {}, PDF Page Number: {}'.format(item['PDF Download URL'], item['PDF Page Number']))
                    # print(item['Title'])
            except:
                # print('Error comparing files: {}, {}'.format(csv_files[i], csv_files[j]))
                count_error += 1


# Same CSV files: G:/ESA_downloads/copy_Bingjie/vntg/667050_14_2.csv, G:/ESA_downloads/copy_Bingjie/vntg/667050_14_1.csv
# PDF Download URL: https://apps.cer-rec.gc.ca/REGDOCS/File/Download/667050, PDF Page Number: 14

# Same CSV files: G:/ESA_downloads/copy_Bingjie/vntg/667248_13_2.csv, G:/ESA_downloads/copy_Bingjie/vntg/667248_13_1.csv
# PDF Download URL: https://apps.cer-rec.gc.ca/REGDOCS/File/Download/667248, PDF Page Number: 13

# Same CSV files: G:/ESA_downloads/copy_Bingjie/strnmnln/2541470_609_3.csv, G:/ESA_downloads/copy_Bingjie/strnmnln/2541470_609_2.csv
# PDF Download URL: https://apps.cer-rec.gc.ca/REGDOCS/File/Download/2541470, PDF Page Number: 609

# Same CSV files: G:/ESA_downloads/copy_Bingjie/strnmnln/2541470_469_5.csv, G:/ESA_downloads/copy_Bingjie/strnmnln/2541470_469_3.csv
# PDF Download URL: https://apps.cer-rec.gc.ca/REGDOCS/File/Download/2541470, PDF Page Number: 469
