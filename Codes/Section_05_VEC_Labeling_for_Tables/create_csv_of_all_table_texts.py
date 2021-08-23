import pandas as pd
import csv
from pathlib import Path

index_df = pd.read_csv('G:/ESA_downloads/phase_2_download_files/final_csv_table_index_with_pdf_metadata.csv')

# print(index_df['filename'])

csv_location = str(Path(__file__).parents[2]) + '\\Data_Files\\CSVs\\new_projects\\'
print(csv_location)

# csv_location = '/Data_Files/CSVs/new_projects/'

def remove_s_tags(text):
    return text.replace('<s>', '').replace('</s>', '')

for i in range(len(index_df)):
    if i == 0:
        with open(csv_location + index_df['filename'][i], 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            csv_string = ''
            for row in reader:
                csv_string += ''.join(row)
            csv_string = remove_s_tags(csv_string)
            print(csv_string)
        # csv_df = pd.read_csv(csv_location + index_df['filename'][i])
        # print(csv_df)
