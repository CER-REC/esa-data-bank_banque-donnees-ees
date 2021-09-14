from tika import parser
import multiprocessing as mp
import os
from pathlib import Path

pdfs_path = Path('.') / "Data_Files/esa-project-pdfs-subsample"
output_path = pdfs_path / "extracted_texts"


def process_file(filename):
    in_filename = Path('.') / filename
    out_filename = str(Path('.') / 'extracted_texts' / filename) + '.txt'

    text = parser.from_file(in_filename)
    with open(out_filename, 'w+') as outfile:
        outfile.write(text["content"])

if __name__ == '__main__':
    pool = mp.Pool()
    pool.map(process_file, listdir(str(pdfs_path)))