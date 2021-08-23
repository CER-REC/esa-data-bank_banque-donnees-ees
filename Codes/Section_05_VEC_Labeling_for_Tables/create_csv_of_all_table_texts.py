import pandas as pd
import csv

index_df = pd.read_csv('G:/ESA_downloads/phase_2_download_files/final_csv_table_index_with_pdf_metadata.csv')

print(index_df['filename'])

csv_location = 'G:/ESA_downloads/phase_2_download_files/CSVs/'

for i in range(len(index_df)):
    if i == 0:
        csv_df = pd.read_csv(csv_location + index_df['filename'][i])
        print(csv_df)