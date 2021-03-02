import pandas as pd

file = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/English file sent to Translation - for French index file ESA_website_FRA.csv'
df_translation_eng = pd.read_csv(file, encoding='latin-1')

# We found that section cells with commas in it are not translated correctly
# i.e. Section 13.1: Introduction, Section 13.1: Project Description, Section 13.3: Assessment Methods
# However, there are section items like below, but we will just separate them by ',':
# Section 9: Wildlife (Volume 6A, Pipeline and Tank Terminal)
# Section 8: Inspection, Monitoring, and Follow-Up
# Section 21: Accidents, Malfunctions and Unplanned Events
df_translation_eng['is_multi_item_section'] = df_translation_eng['ESA Section(s)']\
    .apply(lambda x: len(x.split(',')) > 1 if type(x) == str else False)

multi_item_sections = df_translation_eng[df_translation_eng['is_multi_item_section']]['ESA Section(s)'].unique().tolist()

section_items = set()
for section in multi_item_sections:
    for item in section.split(','):
        if item.strip():
            section_items.add(item.strip())

df_section = pd.DataFrame({'ESA Section': list(section_items)})
df_section.to_csv('ESA_Section_Jan272021.csv', index_label='ID', encoding='latin-1')


# ------ Add a new column to corrected French translation file ------
file_french_titles = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/corrected_French_titles.csv'
file_translated_esa = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/ESA_Section_Jan272021_FR.xlsx'

df_corrected_titles = pd.read_csv(file_french_titles)
# 'In_En_Title', 'In_En_Section', 'Tr_Fr_Title', 'Tr_Fr_Section'
df_translated_esa = pd.read_excel(file_translated_esa)
# 'ID', 'ESA Section', 'Section EES'
section_translation_dict = dict(zip(df_translated_esa['ESA Section'], df_translated_esa['Section EES']))


def translate(en_section, fr_section):
    # en_section = df_corrected_titles.iloc[0]['In_En_Section']
    # fr_section = df_corrected_titles.iloc[0]['Tr_Fr_Section']
    if type(en_section) is str:
        esa_items = [item.strip() for item in en_section.split(',')]

        translated_esa_items = []
        for item in esa_items[1:]:
            if item in section_translation_dict:
                translated_esa_items.append(section_translation_dict[item])
            else:
                print('Missing: {}'.format(item))

        translated_esa_items.insert(0, fr_section)
        fr_section_complete = ', '.join(translated_esa_items)
        return fr_section_complete
    return


df_section_unique = df_corrected_titles[['In_En_Section', 'Tr_Fr_Section']].drop_duplicates()
df_section_unique['Tr_Fr_Section_New'] = df_section_unique\
    .apply(lambda x: translate(x['In_En_Section'], x['Tr_Fr_Section']), axis=1)

df_corrected_titles = df_corrected_titles.merge(df_section_unique)

# Below is for exporting files in 'latin-1' encoding
df_corrected_titles = df_corrected_titles\
    .applymap(lambda x: x.replace('\u2019', '\'').replace('\u2013', '-').replace('\u2010', '-').replace('\u2212', '-')
                        if type(x) is str else x)

df_corrected_titles.to_csv(
    'F:/Environmental Baseline Data/Version 4 - Final/Indices/corrected_French_titles_sections_16.csv',
    index=False,
    encoding='utf-16',
    sep='\t')

df_x = pd.read_csv(
    'F:/Environmental Baseline Data/Version 4 - Final/Indices/corrected_French_titles_sections_16.csv',
    encoding='utf-16',
    sep='\t')

new_df = df_x.applymap(lambda x: str(x).encode("utf-16", errors="ignore").decode("latin-1", errors="ignore"))
new_df = new_df.applymap(lambda x: x.replace('ÿþ', ''))
new_df.to_csv(
    'F:/Environmental Baseline Data/Version 4 - Final/Indices/corrected_French_titles_sections_latin.csv',
    index=False,
    encoding='latin-1')
