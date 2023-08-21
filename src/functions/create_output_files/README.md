Output folder structure
-----------------------
- /internal
  - /en
    - /projects
    - /tables
    - ESA_website_ENG.csv
  - /fr
    - /projects
    - /tables
    - ESA_website_FRA.csv
  - thumbnails
- /external 
  - /en
    - /projects
    - /tables
    - ESA_website_ENG.csv
  - /fr
    - /projects
    - /tables
    - ESA_website_FRA.csv
  - thumbnails

** The external dataset is external facing so that we exclude IK content from the external dataset

In the /tables folder, we include all the table download zip folders. Each zip folder contains the data of one table
element group. Inside each zip folder, we include all the csv files of the table elements that belong to the table 
element group, as well as a readme file listing some standard information and the metadata of the table element group.

In the /projects folder, we include all the project zip folders. Each project zip folder contains the data of one 
application. Inside each zip folder, we include all the table zip folders (each table zip folder includes all the csv
files of the table elements, but no readme file), a standard readme file and a csv index file listing metadata of the 
tables. 

See [columns_and_translation.xlsx](columns_and_translation.xlsx) to find the required columns in master index files,
project index files, and readme files in the table download zip folders.

TODO: integrate creating thumbnails here

Steps to create the output files
--------------------------------
1. Create internal English dataset by running
   - `create_table_download_zip_folders(application_id)` in [external/create_table_download_zip_folders.py](external/create_table_download_zip_folders.py)
   - `create_project_download_zip_folder(application_id)` in [external/create_project_download_zip_folder.py](external/create_project_download_zip_folder.py)
   - `create_master_index_file(application_id)` in [external/create_master_index_file.py](external/create_master_index_file.py)

2. Create external English dataset (excluding IK) by running
   - `create_internal_en_folder()` in [internal/create_internal_dataset.py](internal/create_internal_dataset.py); this 
   function copies all the files in the internal English dataset and excludes all the IK content

3. Create the list of English text to be translated by the translation team by running
   - `create_translation_file()` in [translation/prepare_for_translation.py](translation/prepare_for_translation.py)

4. With the translation results returned from the translation team, load the translation results into the database by 
running the following function, input `filepath` is the absolute path to the translation file with French translation
   - `load_translation(filepath)` in [translation/load_translation.py](translation/load_translation.py)

5. Create internal French dataset by running
   - `create_table_download_zip_folders(application_id, "fr")` in [external/create_table_download_zip_folders.py](external/create_table_download_zip_folders.py)
   - `create_project_download_zip_folder(application_id, "fr")` in [external/create_project_download_zip_folder.py](external/create_project_download_zip_folder.py)
   - `create_master_index_file(application_id, "fr")` in [external/create_master_index_file.py](external/create_master_index_file.py)

Special instructions
----------------------
For csv files we are generating, we should be using "utf-8-sig" encoding, instead of "utf-8".
Assuming most users open csv file with Excel and Excel doesn't open files in utf-8 encoding by default, resulting some 
utf-8 characters not displayed correctly. However, by saving the csv file using "utf-8-sig" we can have Excel display
properly. See the following reference:
https://stackoverflow.com/questions/61314880/print-encoding-edcoding-french-characters-works-in-txt-file-but-incorrect-in-e
"'utf-8-sig' is a Windows-specific version of Excel which inserts a three character "byte order mark" (BOM)
and the beginning of the file. Windows applications trying to guess a file's encoding will read the BOM and
decode the file from UTF-8. The BOM may not be recognised on other platforms, resulting in three unusual
characters appearing at the beginning of the file."
