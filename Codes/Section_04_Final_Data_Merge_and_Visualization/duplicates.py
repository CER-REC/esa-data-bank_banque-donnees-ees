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
