# Classify Alignment Sheets  
At CER, we receive applications from companies containing thousands of pages of documents. We wanted to develop a Machine Learning Algorithm to differentiate the pages which are alignment sheets (or maps) from pages which are not maps.

##### Sample Maps:

<p float="left">
  <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/map_1.PNG" width="100" />
  <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/map_2.PNG" width="100" /> 
  <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/map_3.PNG" width="100" />
</p>


##### Sample Non-Maps:
<img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_1.PNG" alt="page_1.png" width="150" height = "200" />   <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_2.PNG" alt="page_2.png" width="150" height = "200" />   <img src="https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/imgs/page_3.PNG" alt="page_3.png" width="150" height = "200" />


## Approach 

For the problem stated above we will be using classification algorithms and we will be using features such as area of images in a page, number of images in a page, count of words, we will also be checking if the page has certain words such as the word "North" or "N", "Figure", "Map", "Alignment Sheet" or "Sheet", "Legend", "scale", and "kilometers" or "km".  

Once we have the features extracted we will be training Classification models such as, XG Boost Classifier, Support Vector Classifier, Decision Treen Classifier,  Random Forest Classifier, Random Forest Regressor and XG Boost Regressor. We will be comparing the accuracy and performance of the confusion matrix for these models on Test Set and Training Set. Then we will save the best performing model for future use.

Note: The results from the regressor models are converted into binary output, hence, we will be referring these regression models classification models. 


Description of the folder structure:
1. Training Set: This folder contains the files which are used to prepare the training set and the test set. 

2. Validation Set: This folder contains the files which are used to validate the trained models and then identify the best performing model. 

3. feature_extraction.py: This file contains the funtions which are used to extract the features in a PDF page. These features will be used to do classification.

4. Classify Maps.ipynb: In this file first we read the PDF files in the Training Set fonder. We treat each page as a unique entity and then we use functions from feature_extraction.py to extract feaures for all the pages. Then all these pages with their features are split in to Training set and Test Set. Then we train the classification models and evaluate the model performances. Further we exctract the features for the PDF in the Validation Set folder in the same way. Then we evaluate the models and pick the best model. 