## Approach

1. `01_creating_index_file_with_vecs_vscs.ipynb:` In order to label VECs and VSCs with each of the table, first we need to extract the text from each of these tables. This jupyter notebook extracts the contents of the CSV file from the `csvs` table that we created in [Section_02_DB_setup_and_CSVs_extraction](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/berdi/Section_02_DB_setup_and_CSVs_extraction) and save it in a tab-separated file named `esa_csvs_raw.txt`. The length of the extracted text is then trimmed to only include 30,000 characters due to excel cell character limit of 32,767 characters

2. `keywords.py`: For each of the 22 VECs and VSCs, a list of keywords that represents these VECs and VSCs were prepared in collaboration with the subject matter experts. This jupyter notebook file performs text preprocessing on the list of these keywords and then dump this list into a pickle file `vc_keywords.pkl` 

3. `02_keywords_to_labels.ipynb:` This jupyter notebook file look for all the VECs and VSCs keywords (saved in the pickle file `vc_keywords.pkl` above) in the table text that we extracted and saved in the step 1 above. For every VEC and VSC keyword found in the table text, a count is then assigned and incremented with occurence of each of the VEC and VSC keyword. The array of these 22 VECs & VSCs and their counts is then included in the dataframe

4. `03_labeling_figs_align_sheets.ipynb:` This notebook file runs the process, similar to the one described in step 3 above, to find and assign each of the 22 VECs & VSCs and their keyword counts for figures as well as alignment sheets. **Note:** In case of figures and alignment sheets, the VEC and VSC keywords are searched in the respective figure and alignment sheet titles 

## How to use the files in this repo?

- Clone or download github files into a local directory
- Install required python packages from [requirements.txt](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/blob/master/requirements.txt) file by creating virtual environment
- Activate the virtual environment
- Open Jupyter notebook and run the files in the following order and observe results:

    - `01_creating_index_file_with_vecs_vscs.ipynb`
    - `keywords.py`
    - `02_keywords_to_labels.ipynb`
    - `03_labeling_figs_align_sheets.ipynb`
