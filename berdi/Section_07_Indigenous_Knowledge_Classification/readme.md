## Overview
This section is focused on classifying texts with sensitive Indigenous Knowledge. 
Run main.py in this section.
** CSV files in "data" folder contain sample/mock data

Below are the steps taken to identify IK sensitive data.

1.  Extract text from PDF File <br>
Refer to master index file with metadata on tables, figures, and alignment-sheet. Use document id and page number to parse the PDF's pickle file and extract the text from the corresponding page number. 

2.  Merge labelled data <br>
A subset of 349 tables, figures and alignment sheets data were labelled by subject matter experts. Labels were merged with the full dataset.

3.  Prepare features <br>
- Use the manually curated IK keywords to get the number of distinct keywords and their normalized values from each page  
- Use Topic Modeling methods to generate 20 topic weights pertained to each data point

4.  Balance labelled data <br>
Split the labelled data to training and test datasets and Use SMOTE to balance the labelled data. There are significantly larger number of non-IK labels compared to IK labels.

5.  Tune parameters <br>
Use GridSearchCV from scikit-learn library to tune the model parameters and find a good set of parameter combination.

6.  Train the model <br>
Perform the model training using ensemble learning approach and comparing the performance of multiple models, with the given X_train and y_train data. We show the model with the best performance in this code, Random Forest.

7.  Measure model performance <br>
Use False Omission rate, False Discovery rate, and accuracy as main bases of model validation and comparison.

8. Get prediction <br>
Run the selected model on unlabeled data and get the classifications.
