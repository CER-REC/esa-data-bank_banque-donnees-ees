This section contains code for the following steps of internal processing:
1. generate_index_file_from_db.py
- Generate an index file that include metadata of extracted csv tables, figures and alignment sheets
2. sinclair.py & sinclair_FR.py
- Rename the csv files to semantic file names
- Find the good quality csv tables and only include them in the bundling step later
- Create bundling files - project download zip folders and table download zip folders
- Generate thumbnails for the pdf pages that are identified to have any table, figure or alignment sheet
- Update the index file to include tables (each table consists of one or more than one csv tables that have the same title on the same pdf page), figures and alignment sheets
3. remove_IK/remove_IK.py & remove_IK_fra.py 
- Create the external version of the dataset by removing the content that has been identified to contain indigenous knowledge
   