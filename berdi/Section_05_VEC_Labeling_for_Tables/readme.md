## Description of the folder structure

1. `01_creating_index_file_with_vecs_vscs.ipynb:` In order to label VECs and VSCs with each of the table, first we need to extract the text from each of these tables. This jupyter notebook extracts the contents of the CSV file from the `csvs` table that we created in [Section_02_DB_setup_and_CSVs_extraction](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/berdi/Section_02_DB_setup_and_CSVs_extraction) and save it in a tab-separated file named `esa_csvs_raw.txt`. The length of the extracted text is then trimmed to only include 30,000 characters due to excel cell character limit of 32,767 characters

2. `keywords.py`: 

3. `02_keywords_to_labels.ipynb:` This jupyter notebook look for VECs and VSCs keywords, saved in the file 

4. `03_labeling_figs_align_sheets.ipynb:` 

## How to use the files in this repo?

- Clone or download github files into a local directory
- Install required python packages from [requirements.txt](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/blob/master/requirements.txt) file by creating virtual environment
- Activate the virtual environment
- Open Jupyter notebook and run the files in the following order and observe results:
    - `01_creating_index_file_with_vecs_vscs.ipynb`
    - `keywords.py`
    - `02_keywords_to_labels.ipynb`
    - `03_labeling_figs_align_sheets.ipynb`
