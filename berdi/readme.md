## Overview

You can run the code in the following order:
1. In Section_01_Data_Extraction_Preparation, run main.py
2. In Section_02_DB_setup_and_CSVs_extraction, run the following files:
    * `pdfs_db_seeding.py`
    * `pages_and_blocks_db_seeding.py`
    * `extracting_pages_content.py`    
    * `extracting_tables.py`
3. In Section_03_Table_and_Figure_Title_Extraction, run main.py

4. Section_04 is for internal postprocessing work

5. In Section_06_Alignment_Sheets_index_merge, run the files in the following order:
    * `0. Download PDFs and extract features of Alignment Sheets.ipynb`
    * `1. Save Alignment Sheets.ipynb`

6. In Section_05_VEC_Labeling_for_Tables, run the files in the following order:
    * `01_creating_index_file_with_vecs_vscs.ipynb`
    * `02_keywords_to_labels.ipynb`
    * `03_labeling_figs_align_sheets.ipynb`

In each sub-folder, there is a readme file providing more details.
