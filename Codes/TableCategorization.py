# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 09:51:46 2020

@author: singvibu
"""

import pickle
import os
from bs4 import BeautifulSoup
from tika import parser
import re
import pandas as pd


def table_categorization(path, Index2, max_files):
    """
    This method attempts to download all the PDF files from the list of PDF 
    URLs that are sent to the function.
    
    It is assumesed that the list of PDFs sent to the function are relevant to 
    Environmental and Social Assessment. The files in this list are then 
    downloaded and saved in the PDFs folder which will be read and processed 
    later.
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved
    Index2: Dataframe with the DataIDs of the PDF and their downloadable links    
        Data_ID: It is the unique ID of the PDF file which will be used as the 
        name of the PDF downloaded
        esa_download_link: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
    max_files: maximum number of URL files to be downloaded
        This parameter allows us to limit the number of files that would 
        downloaded. This parameter is handy while running the code in the test
        phase or when we want to limit the number of files.  
        
    Returns
    ----------
    PDF Files:
        The PDF files are scrapped from the URLs and then saved in the PDF 
        folder
    Error List:
        In case theer are PDF files which were not scraped from the given URLs
        due to any reason then we shoudl have a text file which contains the 
        list of these error files.
        
    
    References 
    ----------
    Ref ->
    Ref -> 
        
        
    """
    DataIDs = Index2['DataID']
    all_paths = [path + '\\Data Files\\Pickle Files\\' + 'tikaxml_' + str(x) +'.pkl' for x in DataIDs]
    
    searchlist = ['Image', 'Figure', 'Photo']
    searchfor = []
    for search in searchlist:
        searchfor.append(search)
        searchfor.append(search + 's')
        searchfor.append(search.upper())
        searchfor.append(search.upper() + 'S')
    
    file_name = []
    page_number = []
    table_title = []
    table_title_next = []

    exceptions_list = ['...', 'Table of Content', 'TABLE OF CONTENTS', 'Table des matières', 'TABLE DES MATIÈRES'] 
    last_ptag_starts_with_key = 0
    for x in all_paths:
        with open(x, 'rb') as f:
            data = pickle.load(f)
            soup = BeautifulSoup(data['content'], 'lxml')
            pages = soup.find_all('div', attrs={'class': 'page'})
            for b, p in enumerate(pages):
                pages_text = [x.text for x in p.find_all('p')]
                for y in pages_text:
                    if last_ptag_starts_with_key ==1:
                        table_title_next.append(y.replace('\n',' ').replace('\r',''))
                    last_ptag_starts_with_key = 0
                
                    ytest = y.replace('\n','').replace('\r','')
                    ytest = ytest.split(" ")
                    ytest_no_blanks = ""
                    for ytes in ytest:
                        if len(ytes) > 2:
                            ytest_no_blanks = ytest_no_blanks + ytes + " "
                        
                    if ytest_no_blanks.startswith(('Table', 'TABLE', 'FIGURE', 'FIGURES', 'Figure', 'Figures', 'IMAGE', 'IMAGES', 'Image', 'Images', 'PHOTO', 'PHOTOS', 'Photo', 'Photos')) and not any(substring in y for substring in exceptions_list):
                        file_name.append(x)
                        table_title.append(y.replace('\n','').replace('\r',''))
                        page_number.append(b + 1)
                        last_ptag_starts_with_key = 1
    
    def count_digits_in_string(word):
        digit_count = 0
        for a in word:
            if a.isdigit():
                digit_count = digit_count + 1
        return(digit_count)
    
    
    def categorize_tables(list_titles):
        categories = []
        for title in list_titles: 
            table_string = title.replace('\n','').replace('\r','').replace('–',"").replace(":","").replace("-","").replace("(","")
            table_string = table_string.replace('.','')
            category = 0
        
            title_words = re.split(" ", table_string)
        
            title_words_no_blanks = []
            for title_word in title_words:
                if len(title_word) > 2:
                    title_words_no_blanks.append(title_word)
                elif len(title_word) > 0 and count_digits_in_string(title_word) > 0:
                    title_words_no_blanks.append(title_word)
        
            category = 0
        
        
            if len(title_words_no_blanks) < 3: 
                category = 0.75
            
            if 'cont' in table_string.lower():
                category = 0.35
            
            if len(title_words_no_blanks) > 2:
                if(title_words_no_blanks[2][0].isupper() or title_words_no_blanks[2][0].isdigit()):
                    category = 1
                else:
                    category = 0
                if(title_words_no_blanks[1][-1]== ',') or (title_words_no_blanks[1][-1]== ']') or (title_words_no_blanks[1][-1]== ')'):
                    category = 0
                if(title_words_no_blanks[2][:4].lower() == 'cont'):
                    category = 0.35
            
            if len(title_words_no_blanks) == 3 :
                category = 0.5
                if(title_words_no_blanks[1][0].isdigit() and  title_words_no_blanks[1][0].isupper()):
                    category = 0.65
                if(title_words_no_blanks[2][0].lower() == 'c'):
                    category = 0.55
                if(title_words_no_blanks[2][:4].lower() == 'cont'):
                    category = 0.35
            
            categories.append(category)
            #print("{} is {}. {} ".format(title, category, title_words_no_blanks))
            
        return(categories)
    
    categorize_tablesgorize_tablesgorize_tablesgories = []
    categories = categorize_tables(table_title)
    
    
    final_table_title = []
    for i in range(len(categories)):
        if categories[i] > 0.49 and categories[i] < 1:
            final_table_title.append(table_title[i].strip() + " " + table_title_next[i].strip())
        else:
            final_table_title.append(table_title[i].strip())
    
    
    for i in range(len(categories)):
        if categories[i] == 0.35:
            if(file_name[i]== file_name[i-1]):
                final_table_title[i] = final_table_title[i-1]
    
    
    df_table_names = pd.DataFrame({'file_name' : file_name, 
                               'page_number' : page_number, 
                               'table_title' : table_title, 
                               'table_title_next' : table_title_next, 
                               'final_table_title' : final_table_title,
                                'categories' : categories})
    df_table_names.shape
    
    df_table_names['DataID'] = [int(a.split('_')[-1].split('.')[0]) for a in df_table_names['file_name']]
    
    df_table_names['table_title'] = df_table_names['table_title'].str.replace('\n', ' ')
                                
    df_table_names = df_table_names.drop('file_name', axis = 1)
    
    file = path + '\\Input Files\\Index 2 - PDFs for Major Projects with ESAs.xlsx'
    index2tab = pd.read_excel(file, sheet_name="Sheet1")

    df_table_names_project = df_table_names.merge(index2tab, on = 'DataID')
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('FIGURE'), 'Category'] = 'Figure'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('TABLE'), 'Category'] = 'Table'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('Figure'), 'Category'] = 'Figure'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('Table'), 'Category'] = 'Table'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('IMAGE'), 'Category'] = 'Figure'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('Image'), 'Category'] = 'Figure'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('PHOTO'), 'Category'] = 'Figure'
    df_table_names_project.loc[df_table_names_project['table_title'].str.contains('Photo'), 'Category'] = 'Figure'
    df_table_names_project.head()
    
    
    
    
    
    df_table_names_project['Application title short'].nunique()
    df_table_names_project.shape
    df_table_names_project['table_title'] = df_table_names_project['table_title'].str.strip()
    
    save_string = path + '\\Support Files\\table_titles_categorization.csv'
    df_table_names_project.to_csv(save_string, index = False, encoding='utf-8-sig')
    
    return(len(df_table_names_project))    
                
        
    
