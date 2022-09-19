# Functions related to Topic Modeling
import pandas as pd
import numpy as np
import nltk, spacy, gensim
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm') 


def lemmatize(texts, allowed_postags=['NOUN', 'VERB']): 
    """
    Reduce the words to their common base/root form
    """    
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
    return texts_out


def preprocess_text(df_col):
    """
    Clean the data in page_text column of the dataframe and prepare
    it for training the LDA model
    """
    nltk.download('stopwords')
    en_stop = set(nltk.corpus.stopwords.words('english'))
    clean_df = pd.DataFrame(df_col)
    # keeping alphabets
    clean_df['clean_dat'] = clean_df['page_text'].str.replace("[^a-zA-Z_0-9-#]", ' ', regex=True)
    # Remove Emails
    clean_df['clean_dat'] = clean_df['clean_dat'].str.replace(r'\S*@\S*\s?', '', regex=True)
    # removing short words
    clean_df['clean_dat'] = clean_df['clean_dat'].apply(lambda x: ' '.join([w for w in x.split() if len(w)> 2]))
    # make all text lowercase
    clean_df['clean_dat'] = clean_df['clean_dat'].apply(lambda x: x.lower())
    # removing stopwords
    clean_df['clean_dat'] = clean_df['clean_dat'].apply(lambda x: ' '.join([w for w in x.split() if w not in en_stop]))
    clean_df['clean_dat_tokenized'] = clean_df['clean_dat'].apply(lambda x: gensim.utils.simple_preprocess(str(x), deacc=True))
    return clean_df['clean_dat_tokenized']


def map_predict_topics(data, vectorizer, lda_model):
    """
    Get topic weights assigned to each text item using the lda model and 
    vectorized data
    """
    # Vectorize transform applied to preprocessd and lemmatized text
    vectorized_data = vectorizer.transform([data])
    # LDA Transform
    topic_probability_scores = lda_model.transform(vectorized_data)

    topic_1 = topic_probability_scores[0][0]
    topic_2 = topic_probability_scores[0][1]
    topic_3 = topic_probability_scores[0][2]
    topic_4 = topic_probability_scores[0][3]
    topic_5 = topic_probability_scores[0][4]
    topic_6 = topic_probability_scores[0][5]
    topic_7 = topic_probability_scores[0][6]
    topic_8 = topic_probability_scores[0][7]
    topic_9 = topic_probability_scores[0][8]
    topic_10 = topic_probability_scores[0][9]
    topic_11 = topic_probability_scores[0][10]
    topic_12 = topic_probability_scores[0][11]
    topic_13 = topic_probability_scores[0][12]
    topic_14 = topic_probability_scores[0][13]
    topic_15 = topic_probability_scores[0][14]
    topic_16 = topic_probability_scores[0][15]
    topic_17 = topic_probability_scores[0][16]
    topic_18 = topic_probability_scores[0][17]
    topic_19 = topic_probability_scores[0][18]
    topic_20 = topic_probability_scores[0][19]
    
    return topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7,\
           topic_8, topic_9, topic_10, topic_11, topic_12, topic_13, topic_14,\
           topic_15, topic_16, topic_17, topic_18, topic_19, topic_20


