## Description of the folder structure

1. `01_creating_index_file_with_vecs_vscs.ipynb:` This file contains the funtions to download the PDF documents and to extract the features from each page of a PDF file. The ouput from this jupyter notebook file is a CSV containing all the extracted features

2. `02_keywords_to_labels.ipynb:` This file takes feature CSV as input and classify whether a PDF page is an alignment sheet or not by using the best performing classifier that we saved in repo [models](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/models). The later section of this jupyter notebook file contains the functions to extract and assign the titles for alignment sheets

3. `03_labeling_figs_align_sheets.ipynb:` 

## How to use the files in this repo?

- Clone or download github files into a local directory
- Install required python packages from [requirements.txt](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/blob/master/requirements.txt) file by creating virtual environment
- Activate the virtual environment
- Open Jupyter notebook and run the files in the following order and observe results:
    - `0. Download PDFs and extract features of Alignment Sheets.ipynb`
    - `1. Save Alignment Sheets.ipynb`
