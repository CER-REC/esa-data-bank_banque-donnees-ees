from tika import parser
import multiprocessing as mp
import os

folder_path = "./esa-project-pdfs-subsample"

def list_of_pdfs_filepaths_in_folder(folder_path):
    list_of_pdfs=[]
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            list_of_pdfs.append(folder_path+"/"+file)
    return list_of_pdfs

list_of_pdfs = list_of_pdfs_filepaths_in_folder(folder_path)
print(list_of_pdfs)

def tika_text_extractor(file_path):
    parsed_tika=parser.from_file(file_path)
    print(parsed_tika["content"])

for pdf in list_of_pdfs:
    tika_text_extractor(pdf)

# # Multiprocessing
# with mp.Pool() as pool:
#     results = pool.map(tika_text_extractor, list_of_pdfs, chunksize=1)
# for result in results:
#     print(result, end='', flush=True)