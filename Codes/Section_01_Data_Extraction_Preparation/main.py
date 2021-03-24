import pandas as pd
import time
import os
import multiprocessing
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from Codes.Section_01_Data_Extraction_Preparation.file_preparation import download_file, rotate_pdf, pickle_pdf_xml
from Codes.Section_01_Data_Extraction_Preparation.pdf_metadata import get_pdf_metadata


Index0_path = os.path.join(os.getcwd(), 'Input_Files/Index_of_PDFs_for_Major_Projects_with_ESAs.csv')

Index0 = pd.read_csv(Index0_path, index_col=0)
Index0 = Index0.head(3)

# Download files
count = download_file(os.getcwd(), Index0)
print("{} Files were downloaded from {} URL links".format(count, len(Index0)))

# Rotate files
count = rotate_pdf(os.getcwd(), Index0)
print("{} Files were successfully rotated".format(count))

# Convert to pickle files
for pdf_folder_name, pickle_file_folder_name in {('PDFs', 'Pickle_Files'), ('PDFs_Rotated', 'Pickle_Files_Rotated')}:
    pdf_folder_path = os.path.join(os.getcwd(), 'Data_Files', pdf_folder_name)
    pdf_file_paths = [os.path.join(pdf_folder_path, file)
                      for file in os.listdir(pdf_folder_path) if file.endswith('.pdf')]
    pickle_folder_path = os.path.join(os.getcwd(), 'Data_Files', pickle_file_folder_name)

    # multiprocessing
    args = [(file, pickle_folder_path) for file in pdf_file_paths]
    starttime = time.time()
    pool = multiprocessing.Pool()
    pool.starmap(pickle_pdf_xml, args)
    pool.close()
    # time ends and delta displayed
    print('That took {} seconds'.format(time.time() - starttime))

# Add metadata and export to csv
Index1 = get_pdf_metadata(os.getcwd(), Index0)
metadata_file_path = os.path.join(os.getcwd(), 'Output_Files/Index 1 - PDFs for Major Projects with ESAs.csv')
Index1.to_csv(metadata_file_path, index=False, encoding='utf-8-sig')
