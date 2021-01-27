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
