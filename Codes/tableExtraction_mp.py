#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import multiprocessing
# import sys
# sys.path.insert(0, 'H:/GitHub/Extract-Tables-With-Titles')
import functions_mp as mf



if __name__ == '__main__':

    path1 = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/Support files/Table titles raw data/final_table_titles8.csv'
    path2 = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/Support files/Table titles raw data/mackenzie_table_title.csv'

    df1= pd.read_csv(path1, usecols= ['page_number', 'final_table_title', 'DataID', 'categories',  'Category'])
    df2 = pd.read_csv(path2, 'utf-8', engine = 'python',delimiter = ',')
    df2 = df2[['page_number','final_table_title', 'DataID','categories', 'Category']]
    frames = [df1,df2]
    df = pd.concat(frames)
    df['DataID'] = df['DataID'].astype(str)
    df = df[df['categories'] > 0] 
    df = df[df['Category'] == 'Table']
    df['final_table_title'] = df['final_table_title'].str.title()
    df.head()

    path = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/CSV_final_JSON/'
    path_ = '//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/PDF/'
    lst_json = [(fname.split('\\')[-1]).split('_')[0] for fname in glob.glob(path+'*.txt')]
    lst_pdf = [(fname.split('\\')[-1]).replace('.pdf','') for fname in glob.glob(path_+'*.pdf')]
    files = [item+'.pdf' for item in lst_pdf if item not in lst_json]        
        
    args = mf.create_arguments(files, df) 
    starttime = time.time()
    outputs = []

#    ******************************************************
#    for arg in args:
#        outputs.append(mf.extract_tables_noname(arg))

#    ******************************************************
    with multiprocessing.Pool() as pool:
        outputs = pool.map(mf.extract_tables_noname, args)
    
    print('That took {} seconds'.format(time.time() - starttime))      


