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


        
def check_topic_present(topic, text):
    for key in topic:
        if key in text:
            return 1
    return 0
          
def remove_string_special_characters(s): 
      
    # removes special characters with ' ' 
    stripped = re.sub('[^a-zA-z\s]', '', s) 
    stripped = re.sub('_', '', stripped) 
      
    # Change any white space to one space 
    stripped = re.sub('\s+', ' ', stripped) 
      
    # Remove start and end white spaces 
    stripped = stripped.strip() 
    if stripped != '': 
            return stripped.lower() 
        
def pdf_categorize(path, Index0):
    
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
    sizes = []
    for index, row in Index0.iterrows():
        pdf_path = path + "\\Data Files\\PDFs\\" + str(row['Data ID']) + '.pdf'
        file = Path(pdf_path)
        size = file.stat().st_size
        sizes.append(size)
    Index1 = Index0
    Index1['PDF Size (bytes)'] = sizes
    return(Index1)
            

#def pdf_pagenumbers(path, Index0):
    