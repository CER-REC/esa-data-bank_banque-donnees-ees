# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:47:06 2020

@author: singvibu
"""
import pandas as pd
import nltk

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# Importing libraries 
import nltk 
import re 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import pandas as pd 

from pathlib import Path


import PyPDF2
from pathlib import Path


        
def check_topic_present(topic, text):
    """
    This basic function attempts to check if any of the keywords of a 
    particular topic are present in the the description line of the PDF File. 
    
    Parameters
    ----------
    topic: contains a list of keywords present in a topic
    text: contains the textual description line for the PDF
    
    Returns
    ----------
    Binary_Value:
        It returs binary value 1 or 0, depecding on if there is a keyword that 
        is present in the textual description line for the PDF. 
        
    """
    
    for key in topic:
        if key in text:
            return 1
    return 0
          
def remove_string_special_characters(s): 
    """
    This basic function attempts to replace special characters, and multiple 
    white spaces with a single pscae. It also removes all leading and trailing 
    characters from the string. Furthermore, it converts the string into lower 
    case characters. thus making the input string into easy to process string.
    
    Parameters
    ----------
    s: the input string 
    
    Returns
    ----------
    Easy to process string:
        It reurns easy to process string, which means the string does not have 
        unnecessary white spaces and all characters are in lower case.
        
    """
      
    # removes special characters with ' ' 
    stripped = re.sub('[^a-zA-z\s]', '', s) 
    stripped = re.sub('_', '', stripped) 
      
    # Change any white space to one space 
    stripped = re.sub('\s+', ' ', stripped) 
      
    # Remove start and end white spaces 
    stripped = stripped.strip() 
    return stripped.lower() 
        
def pdf_categorize(path, Index0):
    """
    This method attempts to categorize all the PDF files from the list of PDFs 
    into one more ESA categories. 
    
    Based on the contents of a ESA files, we were able to identify the top 10 
    ESA categories. We performed frequency analysis of the keywords from the 
    PDF contents, thereafter we came up with top 10 ESA categories. 
    
    As there might be a single PDF File covering more than one ESA category, 
    hence, we get an arror of categories for each PDF File. PDF files which do 
    not match to any of these 10 categories are classifies as 'other'.
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved
    Index0: Dataframe with the DataIDs of the PDF and their downloadable links    
        Data_ID: It is the unique ID of the PDF file which will be used as the 
        name of the PDF downloaded
        esa_download_link: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
        
    Returns
    ----------
    Index1:
        This returns a dataframe similar to Index0 with an additional coloumn
        'Topics', indicating the ESA categories which the code has identified 
        for the PDF file.
        
    """
    
    #Defining 10 categories based on the keywords chosen 
    land1 = ['soil', 'land', 'ground', 'terrain', 'topography', 'ecozones', 'terrain']
    air2 = ['air', 'emission', 'ghg', 'gas', 'greenhouse', 'weather' , 'climate', 'meteorological', 'atmospher']
    water3 = ['water', 'fish', 'wetlands', 'navigation', 'marine', 'aqua', 'drain', 'river']
    wildlife4 = ['wild', 'fish', 'poisson', 'species', 'habitat', 'acoustic', 'life', 'biophysical']
    vegetation5 = ['vegetation', 'wetlands', 'plant', 'soil']
    human6 = ['human', 'socio', 'social', 'economic', 'economy' 'occupancy', 'heritage', 'health', 'aesthetics', 
              'employment', 'acoustic', 'traditional', 'navigation', 'resource', 'infrastructure', 'noise', 'rapport']
    alignment_sheet7 = ['alignment', 'sheet']
    tech8 = ['technical', 'tech']
    traditional_knowledge9 = ['first', 'nation', 'traditional', 'engage']
    epp10 = ['environment protection', 'environmental protection' , 'epp']
        
    topics = []
    for index, row in Index0.iterrows():
        line = str(row['ESA Section(s)']) + str(row['File Name'])
        line = remove_string_special_characters(line).lower()
        line_topics = []
        topic_found = 0
    
        if check_topic_present(land1, line) == 1:
            line_topics.append('Land')
            topic_found = 1
        
        if check_topic_present(air2, line) == 1:
            line_topics.append('Air')
            topic_found = 1
    
        if check_topic_present(water3, line) == 1:
            line_topics.append('Water')
            topic_found = 1
        
        if check_topic_present(wildlife4, line) == 1:
            line_topics.append('Wildlife')
            topic_found = 1
            
        if check_topic_present(vegetation5, line) == 1:
            line_topics.append('Vegetation')
            topic_found = 1
        
        if check_topic_present(human6, line) == 1:
            line_topics.append('Human')
            topic_found = 1
            
        if check_topic_present(alignment_sheet7, line) == 1:
            line_topics.append('Alignment Sheet')
            topic_found = 1
        
        if check_topic_present(tech8, line) == 1:
            line_topics.append('Technology')
            topic_found = 1

        if check_topic_present(traditional_knowledge9, line) == 1:
            line_topics.append('Traditional Knowledge')
            topic_found = 1
    
        if check_topic_present(epp10, line) == 1:
            line_topics.append('Environment Protection Plan')
            topic_found = 1
        
        if topic_found == 0:
            line_topics.append('Other')
        
        topics.append(line_topics)
        
    Index1 = Index0
    Index1['Topics'] = topics
    return(Index1)


def pdf_size(path, Index0):
    """
    This method attempts to identify the size of each of the PDF files (in 
    bytes) from the list of files present in the Index0. The files which might 
    have an error in opening or any other dependent step will show a file size 
    of 0 bytes. 
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved
    Index0: Dataframe with the DataIDs of the PDF and their downloadable links    
        Data_ID: It is the unique ID of the PDF file which will be used as the 
        name of the PDF downloaded
        esa_download_link: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
        
    Returns
    ----------
    Index1:
        This returns a dataframe similar to Index0 with an additional coloumn
        'PDF Size (bytes)', indicating the size of the PDF file in bytes. 
        
    """
    sizes = []
    for index, row in Index0.iterrows():
        try:
            pdf_path = path + "\\Data_Files\\PDFs\\" + str(row['Data ID']) + '.pdf'
            file = Path(pdf_path)
            size = file.stat().st_size
            sizes.append(size)
        except:
            sizes.append(0)
    Index1 = Index0
    Index1['PDF Size (bytes)'] = sizes
    return(Index1)
            

def pdf_pagenumbers(path, Index0):
    """
    This method attempts to identify the number of pages in each of the PDF 
    files from the list of files present in the Index0. The files which might 
    have an error in opening due to any other dependent step will have 0 number 
    of pages in the pdf. 
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved
    Index0: Dataframe with the DataIDs of the PDF and their downloadable links    
        Data_ID: It is the unique ID of the PDF file which will be used as the 
        name of the PDF downloaded
        esa_download_link: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
        
    Returns
    ----------
    Index1:
        This returns a dataframe similar to Index0 with an additional coloumn
        'Number of Pages', indicating the number of pages in the PDF file. 
        
    """
    page_numbers = []
    for index, row in Index0.iterrows():
        try:
            pdf_path = Path(path + "\\Data_Files\\PDFs\\" + str(row['Data ID']) + '.pdf')
            with pdf_path.open("rb") as pdf:
                reader = PyPDF2.PdfFileReader(pdf)
                if reader.isEncrypted:
                    reader.decrypt("")
                total_pages = reader.getNumPages()
                page_numbers.append(total_pages)
        except:
            page_numbers.append(0)
    Index1 = Index0
    Index1['Number of Pages'] = page_numbers
    return(Index1)
    