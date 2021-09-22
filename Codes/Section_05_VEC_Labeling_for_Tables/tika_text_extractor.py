from tika import parser
import multiprocessing as mp
from os import listdir, path, makedirs
from pathlib import Path
import time
import pickle

import spacy
import re

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


nlp = spacy.load('en_core_web_sm')

# run script in root directory
pdfs_path = str(Path('.') / "Data_Files/esa-project-pdfs-subsample/")
output_path = pdfs_path + "/extracted_texts/"
pickled_sentences_path = pdfs_path + "/pickle_lists/"

def list_files(path):
    """This function creates a list of strings with the names of all the PDFs in the specified directory."""
    return [f for f in listdir(path) if f.endswith('.pdf')]

def remove_false_sentences(sents_list):
    """This function will remove all short strings from sents_list so that we are only left with proper sentences."""
    new_sents_list = []
    for sent in sents_list:
        if (' ' in sent) == False:
            sent = 'false' # removes all extracted sentences with no whitespace
        sent = sent.replace('\n', ' ')
        sent = re.sub(' +', ' ', sent)
        if len(sent) > 6:
            new_sents_list.append(sent) # only saves sentences with more than 20 characters
    # print(new_sents_list)
    return new_sents_list

def split_sents_with_bullet_points(sents_list):
    """This function splits a list of sentences into a list of lists of sentences, where each list contains sentences
    that are separated by a bullet point."""
    new_sents_list = []
    d = '•'
    for sent in sents_list:
        if (d in sent) == True:
            new_sents = [d+e for e in sent.split(d) if e]
            for sent in new_sents:
                if len(sent) > 6:
                    new_sents_list.append(sent)
        else:
            new_sents_list.append(sent)
    return new_sents_list

def regex_remove_items_with_page_number(sents_list):
    """This function removes all sentences that contain a page number."""
    new_sents_list = []
    for sent in sents_list:
        if re.search(r'\d+\s*[pP]\s*\d+', sent) == None:
            new_sents_list.append(sent)
    return new_sents_list

## TODO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def regex_remove_spaced_words(sents_list):
    """This function removes all sentences where there is a space between every single character.
    It checks if there are more then 4 spaces in the first 10 characters."""
    new_sents_list = []
    for sent in sents_list:
        if re.search(r'\s{4,}', sent[:10]) == None:
            new_sents_list.append(sent)
    return new_sents_list


if not path.exists(output_path):
    makedirs(output_path)

def process_file(filename):
    """This function takes a single PDF file and extracts the text from it."""
    in_filename = pdfs_path + '/' + filename
    out_filename = output_path + '/' + filename[:-4] + '.txt'
    pickle_filename = pickled_sentences_path + '/' + filename[:-4] + '.pkl'

    text = parser.from_file(in_filename)
    with open(out_filename, 'w+') as outfile:
        outfile.write(text["content"])
        # print(text['content'])
        doc = nlp(text['content'])
        sents_list = []
        for sent in doc.sents:
            sents_list.append(sent.text)
        sents_list = remove_false_sentences(sents_list)
        sents_list = split_sents_with_bullet_points(sents_list)
        print(sents_list)

        # pickle.dump(sents_list, open(pickle_filename, 'wb'))

if __name__ == '__main__':
    time_start = time.time()
    pool = mp.Pool()
    pool.map(process_file, list_files(pdfs_path)[0:4])
    time_end = time.time()
    print(f"Time elapsed: {time_end - time_start}")
