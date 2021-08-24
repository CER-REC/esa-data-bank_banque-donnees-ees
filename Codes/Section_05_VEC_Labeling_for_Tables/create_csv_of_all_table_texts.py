from numpy import NaN
import pandas as pd
import csv
from pathlib import Path
import os

index_df = pd.read_csv('G:/ESA_downloads/phase_2_download_files/final_csv_table_index_with_pdf_metadata.csv')
index_df['text'] = NaN

csv_location = str(Path(__file__).parents[2]) + '\\Data_Files\\CSVs\\new_projects\\'
print(csv_location)

def remove_s_tags(text):
    return text.replace('<s>', '').replace('</s>', '')

for i in range(len(index_df)):
    with open(csv_location + index_df['filename'][i], 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_string = ''
        for row in reader:
            csv_string += ' '.join(row)
        csv_string = remove_s_tags(csv_string)
        index_df['text'][i] = csv_string

print(index_df.head())

index_df.to_csv('./data/new_projects_index_file.csv', index=False)