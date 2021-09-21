from tika import parser
import multiprocessing as mp
from os import listdir, path, makedirs
from pathlib import Path
import time

import spacy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


nlp = spacy.load('en_core_web_sm')

def list_files(path):
    """This function creates a list of strings with the names of all the PDFs in the specified directory."""
    return [f for f in listdir(path) if f.endswith('.pdf')]

def remove_all_short_strings(sents_list):
    """This function will remove all short strings from sents_list so that we are only left with proper sentences."""
    new_sents_list = []
    for sent in sents_list:
        new_sent = sent.replace('\n', ' ')
        if len(sent) > 20:
            new_sents_list.append(new_sent)
    return new_sents_list


# def store_text_in_sql_database_with_sqlalchemy(text):
#     """This function takes the extracted text and stores it in our MSSQL database."""


# run script in root directory
pdfs_path = str(Path('.') / "Data_Files/esa-project-pdfs-subsample/")
output_path = pdfs_path + "/extracted_texts/"

if not path.exists(output_path):
    makedirs(output_path)

def process_file(filename):
    """This function takes a single PDF file and extracts the text from it."""
    in_filename = pdfs_path + '/' + filename
    out_filename = output_path + '/' + filename[:-4] + '.txt'

    text = parser.from_file(in_filename)
    with open(out_filename, 'w+') as outfile:
        outfile.write(text["content"])
        print(text['content'])
        doc = nlp(text['content'])
        sents_list = []
        for sent in doc.sents:
            sents_list.append(sent.text)
        print(sents_list)

if __name__ == '__main__':
    time_start = time.time()
    pool = mp.Pool()
    pool.map(process_file, list_files(pdfs_path)[0:4])
    time_end = time.time()
    print(f"Time elapsed: {time_end - time_start}")
