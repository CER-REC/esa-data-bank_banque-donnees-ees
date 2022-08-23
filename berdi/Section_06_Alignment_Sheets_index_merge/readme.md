# Classify Alignment Sheets  
At CER, we receive applications from companies containing thousands of pages of documents. We wanted to develop a Machine Learning Algorithm to differentiate the pages which are alignment sheets (or maps) from pages which are not maps.

##### Sample Maps:

[<img src="/imgs/map_1.PNG" width="100" />](/imgs/map_1.PNG)
![map_2](/imgs/map_2.PNG)
![map_3](/imgs/map_3.PNG)


##### Sample Non-Maps:
<img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_1.PNG" alt="page_1.png" width="150" height = "200" />   <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_2.PNG" alt="page_2.png" width="150" height = "200" />   <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_3.PNG" alt="page_3.png" width="150" height = "200" />


## Approach 

The problem stated above was tackled by building and training a bunch of classification algorithms using the features that were extracted from each page of a PDF file using [Python PyMuPDF library](https://pymupdf.readthedocs.io/en/latest/). The names of some of the features that were extracted using PyMuPDF library are area of images in a page, number of images in a page, count of words in a page. In addition, few more features were generated by simply checking if the page has certain words such as "North" or "N", "Figure", "Map", "Alignment Sheet" or "Sheet", "Legend", "scale", and "kilometers" or "km".  

After feature extraction, different Classification models were compiled and trained such as, XG Boost Classifier, Support Vector Classifier, Decision Trees Classifier,  Random Forest Classifier, Random Forest Regressor and XG Boost Regressor. Post model training, the model accuracy and performance was evaluated on the validation dataset and the unseen data i.e. test dataset. After evaluation phase, the best performing model was saved in [models](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/models) repo for future use.

**Note:** The result from the regressor models was converted into binary output using `sigmoid function`, hence, we will be referring these regression models as classification models. 

The model training part has not been discussed in depth here. Rather, we present below the structure of this repo and how to run the jupyter notebook files

Description of the folder structure:
1. `0. Download PDFs and extract features of Alignment Sheets.ipynb:` This file contains the funtions to download the PDF documents and to extract the features from each of page of a PDF file. These features will be used for inference using the best classifier that we saved. 

2. `1. Save Alignment Sheets.ipynb:` Classify Maps.ipynb: In this file first we read the PDF files in the Training Set fonder. We treat each page as a unique entity and then we use functions from feature_extraction.py to extract feaures for all the pages. Then all these pages with their features are split in to Training set and Test Set. Then we train the classification models and evaluate the model performances. Further we exctract the features for the PDF in the Validation Set folder in the same way. Then we evaluate the models and pick the best model. 