# Main function
# Libararies
import pandas as pd
import numpy as np
import os
from pathlib import Path
import data_prepration as dp
import topic_modeling_prepration as tm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import confusion_matrix


if __name__ == "__main__":
    # Update the path 
    ROOT_PATH = Path(__file__).resolve().parents[2]
    data_path = str(
        ROOT_PATH
        / "berdi"
        / "Section_07_Indeginious_Knowledge_Classification"
        / "data"
    )

    pickle_folder_path = str(
        ROOT_PATH
        / "berdi"
        / "data"
        / "processed"
        / "pickle_files"
    )

    # Load the list of projects
    Index0 = pd.read_csv(os.path.join(data_path, "ESA_website_ENG.csv"), encoding= 'unicode_escape', index_col=0)

    # Extract text from documents by page number
    internal_id = []
    id_csv = []
    page_text = []
    page_text_len = []
    error_ids = []
    types = []
    for index, row in Index0.iterrows():
        try:
            pdf = str(row["Data ID"])
            page = str(row["PDF Page Number"])
            text, len_text = dp.get_page_text(pdf, page, pickle_folder_path)

            types.append(dp.get_types(row))
            internal_id.append(row["Internal_ID"])
            id_csv.append(row["ID"])
            page_text.append(text)
            page_text_len.append(len_text)
        except Exception: 
            error_ids.append(index)

    esa_elements_text = pd.DataFrame({'Internal_ID': internal_id,
                                    'ID': id_csv,
                                    'Type':types,
                                    'page_text': page_text,
                                    'page_text_len': page_text_len})


    # Get IK word-counts per page and per 1000 words - new features
    ik_keywords = pd.read_csv(os.path.join(data_path, "ik_keywords.csv"))
    ik_count_per_1000 = []
    ik_count = []
    ik_present = []
    for index, row in esa_elements_text.iterrows():
        ik_count_per_1000_v, ik_count_v, ik_present_v = dp.check_ik_words_new(row['page_text'], ik_keywords)
        ik_count_per_1000.append(ik_count_per_1000_v)
        ik_count.append(ik_count_v)
        ik_present.append(ik_present_v)
        if index % 1000 == 0:
            print(index)
    esa_elements_text['ik_count_per_1000'] = ik_count_per_1000
    esa_elements_text['ik_count'] = ik_count
    esa_elements_text['ik_present'] = ik_present

    # Remove texts with no IK presence 
    esa_elements_text = esa_elements_text[esa_elements_text.ik_count>0]

    # Parse labelled data
    ik_labelled = pd.read_csv(os.path.join(data_path, "ik_labelled.csv"))

    # Merge 349 labelles with the master file
    df_join = pd.merge(esa_elements_text, ik_labelled, on = 'Internal_ID', how = 'outer')
    
    # Preprocess text data and have it ready to train a Topic Modeling model
    # Reference: https://yanlinc.medium.com/how-to-build-a-lda-topic-model-using-from-text-601cdcbfd3a6
    # Cleaning, tokenizing, stemming
    cleaned_text = tm.preprocess_text(df_join['page_text'])
    data_lemmatized_all = tm.lemmatize(cleaned_text) #select noun and verb
    df_join["data_lemmatized"] = data_lemmatized_all

    # Prepare LDA corpus with labelled data
    df_labelled = df_join[df_join.IK_label.notna()]
    labelled_data_lemmatized = df_labelled.data_lemmatized.values.tolist()

    # LDA Model
    vectorizer = CountVectorizer(analyzer = 'word', strip_accents = 'unicode', stop_words = 'english',\
         lowercase = True, max_features = 2000, token_pattern = r'\b[a-zA-Z]{3,}\b', max_df = 0.75,min_df = 4, ngram_range=(1, 3))
    data_vectorized = vectorizer.fit_transform(labelled_data_lemmatized)

    best_lda_model = LatentDirichletAllocation(n_components=20, max_iter=10, random_state=100, batch_size=128)
    lda_output = best_lda_model.fit_transform(data_vectorized)

    # For non-labelled data
    # data_vectorized_all = vectorizer.fit_transform(data_lemmatized_all)
    # Topic Matrix
    # lda_output = best_lda_model.transform(data_vectorized_all)

    # Add topics to the dataset as features for the model
    df_join[['topic_1','topic_2','topic_3','topic_4','topic_5','topic_6','topic_7','topic_8','topic_9','topic_10',\
    'topic_11','topic_12','topic_13','topic_14', 'topic_15','topic_16','topic_17','topic_18','topic_19','topic_20']]=\
    [tm.map_predict_topics(a, vectorizer, best_lda_model) for a in df_join['data_lemmatized']]

    #############################################
    # Indeginous Knowledge Classification Model #
    #############################################
    # Get the data ready for training the models
    # Convert Yes and No labels to 1 and 0
    df_join['IK_label_numeric'] = df_join.apply(lambda x: dp.get_ik_label_num(x["IK_label"]), axis = 1)   
    df_labelled = df_join[df_join.IK_label.notna()]

    # Prepare Training and Test data
    X_df_features = df_labelled.copy()
    X_df_features.drop(columns = ['Internal_ID', 'ID', 'page_text', 'Type','ik_present','page_text_len_cat', 'IK_label', 'data_lemmatized', 'IK_label_numeric'], inplace = True)
    Y_df = df_labelled['IK_label_numeric']

    X = X_df_features
    y = Y_df
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    # Synthetic Minority Oversampling Technique (SMOTE)
    smote = SMOTE(random_state = 11)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Best performing model
    pipeline = Pipeline(steps = [['scaler', MinMaxScaler()],
                             ['clf', RandomForestClassifier()]])

    stratified_kfold = StratifiedKFold(n_splits=3,
                                        shuffle=True,
                                        random_state=11)
        
    param_grid = {
        "clf__n_estimators": [100, 500, 1000],
        "clf__max_depth": [1, 5, 8, 10, 25],
        "clf__max_features": [*np.arange(0.1, 1.1, 0.1)],
    }
    randomforest_grid_search = GridSearchCV(estimator=pipeline,
                            param_grid=param_grid,
                            scoring='roc_auc',
                            cv=stratified_kfold,
                            n_jobs=-1)

    # Fit the model in our Train dataset 
    randomforest_grid_search.fit(X_train, y_train)

    # Model performance
    cv_score = randomforest_grid_search.best_score_
    test_score = randomforest_grid_search.score(X_test, y_test)
    print(f'Cross-validation score: {cv_score}\nTest score: {test_score}')

    y_pred= randomforest_grid_search.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'Accuracy of {randomforest_grid_search} is {acc}')
    cm = confusion_matrix(y_test, y_pred)
    fdr = cm[0,1]/(cm[1,1]+cm[0,1])
    for_ = cm[1,0]/(cm[1,0]+cm[0,0])
    print(f'False Omission Rate: {for_}\nFalse Discovery Rate: {fdr}')

    # Run the model on unlabelled data and get the predictions
    df_unlabelled = df_join[df_join.IK_label.isna()]
    X_df_new = df_unlabelled.copy()
    X_df_new.drop(columns = ['Internal_ID', 'ID', 'page_text', 'Type','ik_present','page_text_len_cat', 'IK_label', 'data_lemmatized', 'IK_label_numeric'], inplace = True)
    Y_df = df_unlabelled['IK_label_numeric'].copy()
    Y_df = pd.DataFrame(Y_df)
    Y_df['preds'] = y_pred
    df_unlabelled['predictions'] = y_pred

