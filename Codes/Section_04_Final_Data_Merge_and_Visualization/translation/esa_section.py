import pandas as pd

file = 'F:/Environmental Baseline Data/Version 4 - Final/Indices/English file sent to Translation - for French index file ESA_website_FRA.csv'
df_translation_eng = pd.read_csv(file, encoding='latin-1')

# file_fra ='F:/Environmental Baseline Data/Version 4 - Final/Indices/Final ESA index file - translated - Jan 8 2021.xlsx'
# df_translation_fra = pd.read_excel(file_fra, sheet_name='200505-1-Data - Translated')

# We assume that section cells with comma in it are not translated correctly
# There are section items like below, but we will just separate them by ',':
# Section 9: Wildlife (Volume 6A, Pipeline and Tank Terminal)
# Section 8: Inspection, Monitoring, and Follow-Up
# Section 21: Accidents, Malfunctions and Unplanned Events
df_translation_eng['is_multi_section_item'] = df_translation_eng['ESA Section(s)']\
    .apply(lambda x: len(x.split(',')) > 1 if type(x) == str else False)

sections = df_translation_eng[df_translation_eng['is_multi_section_item']]['ESA Section(s)'].unique().tolist()


section_items = set()
for section in sections:
    for item in section.split(','):
        if item.strip():
            section_items.add(item.strip())

df_section = pd.DataFrame({'ESA Section': list(section_items)})
df_section.to_csv('ESA_Section_Jan272021.csv', index_label='ID', encoding='latin-1')
