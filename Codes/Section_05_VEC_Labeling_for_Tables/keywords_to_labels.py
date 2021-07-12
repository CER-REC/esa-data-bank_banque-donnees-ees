import pickle
import re

with open("keywords.pkl", "rb") as f:
    keywords = pickle.load(f)

def regex_to_labels(keywords_for_label):