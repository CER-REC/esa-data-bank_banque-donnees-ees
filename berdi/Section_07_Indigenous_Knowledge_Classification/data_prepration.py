# Preprocess the data
import pandas as pd
import numpy as np
import pickle
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()


def get_page_text(path, document_id, page_number):
    """
    This method parses a Pickle file with xmlContent from a PDF document and
    extracts the text from the identified page of the document

    Parameters
    ----------
    path: path of the root folder in string format.
          This path will be used to find the folder location where the pickle
          files are stored
    document_id: PDF unique ID which is also the pickle file name
    page_number: Page number from which the text will be extracted

    Returns
    ----------
    page_str:
        Text content of one page of a PDF and length of the string
    """
    path_pkl = path + "Pickles\\" + str(document_id) + ".pkl"
    page_str = ""
    with open(path_pkl, 'rb') as f:
        data = pickle.load(f)
        soup = BeautifulSoup(data['content'], 'lxml')
        pages = soup.find_all('div', attrs={'class': 'page'})
        for b, p in enumerate(pages):
            if b != int(page_number) - 1:
                continue
            pages_text = [x.text for x in p.find_all('p')]                        
            
            for text in pages_text:
                text = text.replace("\n", " ")
                page_str = page_str + " " + text
                
            page_str = page_str.replace("   ", " ")
            page_str = page_str.replace("  ", " ")
            
    return(page_str, len(page_str))


def get_types(row):
    """
    This method translates letters to their corresponding words.
    
    Parameters
    ----------
   row: one entry of from the dataframe (index master file)

    Returns:
    'table' for t, 'figure' for f, and 'alignment_sheet' for a
    ----------:
    """
    int_id = row.Internal_ID
    if 't' in int_id:
        return "table"
    if 'f' in int_id:
        return "figure"
    if 'a' in int_id:
        return "alignment_sheet"



def check_ik_words_new(page_text, ik_keywords):
    """
    Counts number of distinct IK keywords in each page
    
    Parameters
    ----------
    page_text: Text content of a PDF page 
    
    ik_keywords: list of Indigenous Knowledge related keywords

    Returns:
    ik_count_per_1000: normalized number of IK keywords count 
    ik_count: number of distinct IK keywords in one page
    ik_present: 1 if one or more instance of IK keyword is detected in text
    ----------:
    """
    ik_count = 0
    ik_present = 0
    count_keys = np.zeros(len(ik_keywords), dtype = int)
    for sentence in page_text.split("."):
        sentence = sentence.lower()
        sentence = ''.join(e for e in sentence if e.isalnum() or e == ' ')
        sentence = sentence.replace("   ", " ").replace("  ", "")
        stemmed_sent = ""
        for word in sentence.split():
            if word in stopwords.words("english"):
                continue
            else:
                stemmed_token = stemmer.stem(word)
                stemmed_sent = stemmed_sent + " " + stemmed_token
        # Checking the presence of IK_keywords in the stemmed_text 
        for i in range(len(ik_keywords)):
            if ik_keywords[i] in stemmed_sent:
                count_keys[i] = count_keys[i] + 1
                ik_count = ik_count + 1
                ik_present = 1      
    ik_count_per_1000 = int((ik_count *1000)/ (len(page_text.split())+ 1)) 
    return(ik_count_per_1000, ik_count, ik_present)


def get_ik_label_num(label): 
    """
    Converts "Yes" to integer 1 and "No" to value 0
    """
    if label == "Yes":
        return 1
    elif label == "No":
        return 0
    else: 
        return label


