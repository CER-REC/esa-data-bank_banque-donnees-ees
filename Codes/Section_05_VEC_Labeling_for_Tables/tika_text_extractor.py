from tika import parser
import multiprocessing as mp
from os import listdir
from pathlib import Path
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import time



def list_files(path):
    """This function creates a list of strings with the names of all the PDFs in the specified directory."""
    return [f for f in listdir(path) if f.endswith('.pdf')]


def store_text_in_sql_database_with_sqlalchemy(text):
    """This function takes the extracted text and stores it in our MSSQL database."""

# run script in root directory
pdfs_path = str(Path('.') / "Data_Files/esa-project-pdfs-subsample")
output_path = pdfs_path / "extracted_texts"

if not output_path.exists():
    output_path.mkdir()

def process_file(filename):
    in_filename = str(Path('.') / filename)
    out_filename = str(Path('.') / 'extracted_texts' / filename) + '.txt'

    text = parser.from_file(in_filename)
    with open(out_filename, 'w+') as outfile:
        # outfile.write(text["content"])
        print(text['content'])

if __name__ == '__main__':
    time_start = time.time()
    pool = mp.Pool()
    pool.map(process_file, list_files(pdfs_path))
    time_end = time.time()
    print(f"Time elapsed: {time_end - time_start}")
