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
    
        if check_topic_present(land1, line) == 1:
            line_topics.append('Land')
        
        if check_topic_present(air2, line) == 1:
            line_topics.append('Air')
    
        if check_topic_present(water3, line) == 1:
            line_topics.append('Water')
        
        if check_topic_present(wildlife4, line) == 1:
            line_topics.append('Wildlife')
            
        if check_topic_present(vegetation5, line) == 1:
            line_topics.append('Vegetation')
        
        if check_topic_present(human6, line) == 1:
            line_topics.append('Human')
            
        if check_topic_present(alignment_sheet7, line) == 1:
            line_topics.append('Alignment Sheet')
        
        if check_topic_present(tech8, line) == 1:
            line_topics.append('Technology')

        if check_topic_present(traditional_knowledge9, line) == 1:
            line_topics.append('Traditional Knowledge')
    
        if check_topic_present(epp10, line) == 1:
            line_topics.append('Environment Protection Plan')
        
        
        topics.append(line_topics)
        
    Index1 = Index0
    Index1['Topics'] = topics
    
    return(Index1)

