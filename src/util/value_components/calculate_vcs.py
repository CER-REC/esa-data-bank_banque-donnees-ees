import json
from pathlib import Path
from collections import defaultdict
import pandas as pd

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from src.util.database_connection import engine, schema
from src.util.exception_and_logging.handle_exception import ExceptionHandler
from src.util.process_text import clean_text_content

nltk.download('stopwords')
nltk.download('punkt')

# load_dotenv(".env", override=True)

# load the vc and keywords to a dict, key is the Value Component values and the value is the keywords list
vc_keywords_file_path = Path(__file__).parent.resolve().joinpath("keywords.json")

with open(vc_keywords_file_path, "r", encoding="utf-8") as file:
    vc_keywords_mapping = json.load(file)

# query the value components from the database
query = f'''
    SELECT ValueComponentId, ValueComponent 
    FROM {schema}.ValueComponent ORDER BY ValueComponentId;
'''
with ExceptionHandler("Error retrieving rows from table ValueComponent"), engine.begin() as conn:
    df_vcs = pd.read_sql(query, conn)

# add a keywords column to the df_vcs
with ExceptionHandler("Unable to match value component keywords to the value components retrieved from the database"):
    df_vcs["keywords"] = df_vcs["ValueComponent"].apply(lambda x: vc_keywords_mapping[x])


def string_sum_of_matches(list_one, list_two):
    """
    This function takes two lists of strings and counts the number of total matches between the two lists, including
    duplicates. The function returns the number of total matches.
    """
    # Initialize the count variable.
    count = 0
    # Iterate over the first list.
    for item in list_one:
        # If the item is in the second list, increment the count variable.
        if item in list_two:
            count += 1
    # Return the count variable.
    return count


def calculate_vcs_count(df_content, text_column):
    """
        This function takes dataframe column text_column, processes the text first 
        followed by looking up VCS words and then generating the count of their 
        occurence in text_column

        Args:
            df_content (pandas.DataFrame)
            text_column (str)

        Returns:
            dictionary containing ContentId, ValueComponentId, FrequencyCount
    """
    df_content[text_column] = df_content.apply(lambda x: clean_text_content(x[text_column],
                                                                            special_character=True,
                                                                            long_string=True,
                                                                            cid=True,
                                                                            extra_whitespace=True,
                                                                            trailing_whitespace=True), axis=1)

    stemmer = PorterStemmer()
    vcs_dict = defaultdict(list)
    for _, df_content_row in df_content.iterrows():
        # tokenized_table_texts = []
        processed_text = word_tokenize(df_content_row[text_column])
        processed_text = [stemmer.stem(w) for w in processed_text if w not in stopwords.words("english")]
        table_ngram_list = []
        # Sometimes, processed_text would have less than 7 tokens. Hence, used min function inside range below
        # pylint: disable=invalid-name
        for n in range(1, min(7, len(processed_text))):
            table_ngrams = list(ngrams(processed_text, n))
            table_ngram_list.extend([" ".join(table_gram) for table_gram in table_ngrams])
        # pylint: enable=invalid-name

        for _, df_vcs_row in df_vcs.iterrows():
            number_of_matches = string_sum_of_matches(table_ngram_list, df_vcs_row["keywords"])
            if number_of_matches:
                vcs_dict["ContentId"].append(df_content_row.ContentId)
                vcs_dict["ValueComponentId"].append(df_vcs_row["ValueComponentId"])
                vcs_dict["FrequencyCount"].append(number_of_matches)

    return vcs_dict
