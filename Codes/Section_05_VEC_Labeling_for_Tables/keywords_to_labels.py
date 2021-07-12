import pickle
import re
import pandas as pd

with open("keywords.pkl", "rb") as f:
    keywords = pickle.load(f)        

labels_list = ['Physical and meteorological environment',
                'Soil and soil productivity',
                'Vegetation',
                'Water quality and quantity',
                'Fish and fish habitat',
                'Wetlands',
                'Wildlife and wildlife habitat',
                'Species at Risk or Species of Special Status and related habitat',
                'Greenhouse gas (GHG) emissions and climate change',
                'GHG Emissions and Climate Change – Assessment of Upstream GHG Emissions',
                'Air emissions',
                'Acoustic environment',
                'Electromagnetism and Corona Discharge',
                'Human occupancy and resource use',
                'Heritage resources',
                'Navigation and navigation safety',
                'Traditional land and resource use',
                'Social and cultural well-being',
                'Human health and aesthetics',
                'Infrastructure and services',
                'Employment and economy',
                'Environmental Obligations',
                'Rights of Indigenous Peoples']


def keywords_to_label(i, table_text, keywords_for_label, label):
    if any(word in table_text for word in keywords_for_label):
        df[f'{label}'][i] = 1
    else:
        df[f'{label}'][i] = 0

# df = pd.read_csv('./data/ESA_website_ENG_with_VCs_onehot.csv')
df = pd.read_csv('./data/esa_index_with_table_text_no_labels.csv')

table_texts = df['text'].tolist()[:10]

i = 0

for table_text in table_texts:
    for keywords_for_label, label in zip(keywords, labels_list):
        keywords_to_label(i, table_text, keywords_for_label, label)
        i += 1

with open("esa_index_ENG_labeled.pkl", "wb") as f:
    pickle.dump(df, f)

print(df.head())