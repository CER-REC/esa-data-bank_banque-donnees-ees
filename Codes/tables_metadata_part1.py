# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:09:11 2020

@author: yazdsous
"""
import json
import pandas as pd
import os
import numpy as np
import glob
from copy import deepcopy

def json_integrate(path: str, colname: list) -> pd.DataFrame:
    paths = os.listdir(path)
    all_paths = [path + '/' + str(x) for x in paths]
    df_concat = pd.DataFrame()
    for path in all_paths:
        # load json file; save dictionary in variable d
        with open(path) as f:
            d = json.load(f)
        # ignore dictionary of empty
        if not d:
            continue
        else:
            df_json = pd.concat({k: pd.Series(v) for k, v in d.items()})
            frames = [df_concat, df_json]
            df_concat = pd.concat(frames)
    df_concat.reset_index(level=0, inplace=True)
    csv_name = pd.DataFrame(df_concat.iloc[:,1].values.tolist(), columns=['1','2', '3'])
    meta = csv_name['2'].str.split('_', n = 2, expand = True)
    meta = meta.replace(to_replace=r'\.csv', value='', regex=True)
    titles = csv_name['3'].str.split('_', n = 2, expand = True).iloc[:,1]
    out_df = pd.concat([meta, titles], axis = 1)
    out_df.columns = colname
    return out_df


# function to retreiv csv names with separated element of the name
def csv_name_elements(path: str, colnames: list) -> pd.DataFrame:
    csv_names = [os.path.basename(ipath).replace('.csv', '')
                 for ipath in glob.glob(path + '/*.csv')]
    names_series = pd.Series(csv_names)
    md_df = names_series.str.split('_', expand = True)
    md_df.columns = colnames
    return md_df


# map data on CSV to dataframe from the JSON's
def assign_titles(df_json: pd.DataFrame, df_csv: pd.DataFrame) -> pd.DataFrame:
    #find unique fileid's in df_
    fileid_lst = list(df_json.file_id.unique())
    
    for fid in fileid_lst:
        # master dataframe filtered by fileid
        m_df = df_csv[df_csv.DataID == fid]
        # selected dataframe filtered by fileid
        c_df = new_df[df_json.file_id == fid]
        # find pages for this file in master df
        m_lst_pages = list(m_df.page_number.unique())
        m_lst_pages = [str(s) for s in m_lst_pages]
        # find pages for this file in selected df
        c_lst_pages = list(c_df.page_number.unique())

        for pg_c in c_lst_pages:
            if pg_c in m_lst_pages:
                print(fid)
                dis_m_df = df_csv[(df_csv.DataID == fid) &
                                  (df_csv.page_number == int(pg_c))]
                ind_list = list(new_df[(df_json.file_id == fid) &
                                       (df_json.page_number == pg_c)].index)
                # num_row_m = dis_m_df.shape[0]
                # num_row_c = dis_c_df.shape[0]
                for i, itm in enumerate(ind_list):
                    print(dis_m_df.final_table_title.iloc[0])
                    try:
                        df_json.table_title_fromCSV.iloc[itm] = dis_m_df.final_table_title.iloc[i]
                    except Exception:
                        pass
    return df_json


#********************************************************************************************************#
json_path = 'F:/Environmental Baseline Data/Version 4 - Final/CSV_final_JSON'
csv_path = 'F:/Environmental Baseline Data/Version 4 - Final/CSV_final'
clname = ['file_id', 'page_number', 'table_order', 'title_v_json']

# call the function and save a copy
df_tmp = json_integrate(json_path, clname)
new_df = deepcopy(df_tmp)

# arrange columns and indices
#new_df = pd.DataFrame([df_tmp.file_id, df_tmp.page_number,
#                       df_tmp.table_order, df_tmp.title]).transpose()

##########
path1 = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/Support files/Table titles raw data/table_titles_fixed.csv'
path2 = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/Support files/Table titles raw data/mackenzie_table_title.csv'
#df = pd.read_csv(path, usecols = ['page_number','final_table_title', 'Application title short', 'DataID_pdf','categories', 'Category'])
df1 = pd.read_csv(path1, 'utf-8', engine = 'python',delimiter = ',')
df2 = pd.read_csv(path2, 'utf-8', engine = 'python',delimiter = ',')
df2 = df2[['page_number', 'table_title', 'table_title_next', 'final_table_title','categories', 'DataID', 'Category']]
frames = [df1,df2]
df = pd.concat(frames)
df['DataID'] = df['DataID'].astype(str)
df = df[df['categories'] > 0] 
df = df[df['Category'] == 'Table']
df['final_table_title'] = df['final_table_title'].str.title()
df.head()
#############

new_df['table_title_fromCSV'] = np.nan
new_df['table_title_fromCSV'] =  new_df['table_title_fromCSV'].astype(str)

# Note: first goes the dataframe from the JSON's then the CSV
final_df = assign_titles(new_df, df)
#cname = ['file_id', 'page_number', 'table_order']
#tst_csv = csv_name_elements(csv_path, cname)

#remove rows where title and filename are the same
#for index, row in df_.iterrows():
#    lst = row['table_name']
#    lst_item2 = lst[1].replace('.csv','')
#    lst_item3 = lst[2]
#    if lst_item2 == lst_item3:
#        df_.drop(index , inplace=True)
        
#save dataframe to csv
new_df.to_csv("F:/Environmental Baseline Data/Version 4 - Final/Support files/output_sousan/title_assignment_comp_tst.csv", index = False, encoding = 'utf_8_sig')
    
    
    