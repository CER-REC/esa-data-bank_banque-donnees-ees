#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import glob
import shutil
from time import gmtime, strftime

# filepath to the English and French index files
ENG_index_filepath = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_ENG.csv'
FRA_index_filepath = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_website_FRA.csv'

# Loading index file of all tables
df = pd.read_csv(ENG_index_filepath)
df_FRA = pd.read_csv(FRA_index_filepath)

# Remove all rows for figures so that we are only moving tables
df = df[df['Content Type'] == 'Table']
df_FRA = df_FRA[df_FRA['Type de contenu'] == 'Tableau']

# Dropping old index column to create new one
df.drop(columns=['Unnamed: 0'], inplace=True)
df = df.reset_index()
df.rename(columns = {"index": "Index"}, inplace = True) 

df_FRA.drop(columns=['Unnamed: 0'], inplace=True)
df_FRA = df_FRA.reset_index()
df_FRA.rename(columns = {"Index": "Indice"}, inplace = True)

# Creating the names of each csv file
df['filename'] = df['Download folder name'] + '-' + df['Title'].str.lower().str.replace('(', '').str.replace(')', '').str.replace(' ', '-').str.replace('.', '-').str.replace('[^\w+-]', '').str.slice(0,80)

df_FRA['nom_du_fichier'] = df_FRA['Télécharger le nom du dossier'] + '-' + df_FRA['Titre'].str.lower().str.replace('(', '').str.replace(')', '').str.replace(' ', '-').str.replace('.', '-').str.replace('[^\w+-]', '').str.slice(0,80)

# Creating a column with the old filename so that we can rename the files
old_filename_df = df['CSV Download URL'].str.split('/').str[-1].str.split('_')
df['old_filename'] = old_filename_df.str[0] + '_' + old_filename_df.str[1] + '_lattice-v_' + old_filename_df.str[2]

vieux_nom_du_fichier_df = df_FRA['URL de téléchargement CSV'].str.split('/').str[-1].str.split('_')
df_FRA['vieux_nom_de_fichier'] = vieux_nom_du_fichier_df.str[0] + '_' + vieux_nom_du_fichier_df.str[1] + '_lattice-v_' + vieux_nom_du_fichier_df.str[2]

# We add a counter for all CSVs connected to the same table
# For the English index file
prev_title = ''
for index, row in df.iterrows():
    current_title = row['filename']
    if current_title == prev_title:
        current_title = current_title + '-' + 'pt' + str(i)
        i += 1
    else:
        i = 1
        current_title = current_title + '-' + 'pt' + str(i)
    
    df.loc[index, 'filename'] = current_title
    df.loc[index, 'CSV Download URL'] = os.path.join('http://www.cer-rec.gc.ca/esa-ees/', row['Download folder name'] + '/' + current_title + '.csv')
    prev_title = row['filename']

# Making sure there are no duplicates in English filenames
assert len(df) - len(df['filename'].unique()) == 0, "Should be 0."

# For French index file
prev_title = ''
for index, row in df_FRA.iterrows():
    current_title = row['nom_du_fichier']
    if current_title == prev_title:
        current_title = current_title + '-' + 'pt' + str(i)
        i += 1
    else:
        i = 1
        current_title = current_title + '-' + 'pt' + str(i)
    
    df_FRA.loc[index, 'nom_du_fichier'] = current_title
    df_FRA.loc[index, 'URL de téléchargement CSV'] = os.path.join('http://www.cer-rec.gc.ca/esa-ees/', row['Télécharger le nom du dossier'] + '/' + current_title + '.csv')
    prev_title = row['nom_du_fichier']

# Making sure there are no duplicates in French filenames
assert len(df_FRA) - len(df_FRA['nom_du_fichier'].unique()) == 0, "Should be 0."

# Adding an index ID to each file to avoid duplicates
df['filename'] = df['filename'] + '-' + 'no' + df['Index'].astype(str) + '.csv'
df_FRA['nom_du_fichier'] = df_FRA['nom_du_fichier'] + '-' + 'no' + df_FRA['Indice'].astype(str) + '.csv'

# Where the CSVs are located
csv_folder_path_ENG = 'F:/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_latest_ENG/'
csv_folder_path_FRA = 'F:/Environmental Baseline Data/Version 4 - Final/all_csvs_cleaned_latest_FRA/'

# Making the folder the base path
os.chdir(csv_folder_path)

# Here we are renaming the files to our new filename for better user experience
# If the final file has been renamed, it will skip the renaming loop
if os.path.isfile(df['old_filename'].iloc[-1]):
  #loop through the name and rename
    for index, row in df.iterrows():
        if os.path.isfile(row['old_filename']):
            shutil.move(row['old_filename'], row['filename'])  

# Updating base path to Indices folder to save index files
os.chdir('F:/Environmental Baseline Data/Version 4 - Final/Indices/')

# Saving index files
df.to_csv('ESA_website_ENG_' + strftime("%Y_%m_%d", gmtime()) + '.csv')
df_FRA.to_csv('ESA_website_FRA_' + strftime("%Y_%m_%d", gmtime()) + '.csv')