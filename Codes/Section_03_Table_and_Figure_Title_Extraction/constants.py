import re
from pathlib import Path

# paths to data
main_path = r'//luxor/data/branch/Environmental Baseline Data/Version 4 - Final/'
projects_path = Path(main_path + r'Indices/Index 2 - PDFs for Major Projects with ESAs.xlsx')
pickles_path = main_path + 'Pickles/'
pickles_rotated_path = main_path + 'Pickles_rotated/'
csv_path = main_path + 'CSV_final/'
save_dir = main_path + 'Saved2/'

# regexes
empty_line_xml = re.compile(r'<\/p>\s*<p ?\/?>')
empty_line = re.compile(r'^\s*$')
whitespace = re.compile(r'\s+') # all white space
punctuation = re.compile(r'[^\w\s]') # punctuation (not letter or number)
# figure = re.compile(r'(?im)(^Figure .*?\n?.*?)\.{2,}(.*)')
# table = re.compile(r'(?im)(^Table (?!of contents?).*?\n?.*?)\.{2,}(.*)')
toc_old = re.compile(r'(?im)^(?! *LIST OF\b)(?! *Table of contents\b)(.+?\n?.*?)\.{2,}(.*)$')
toc = re.compile(r'(?im)^(?! *LIST OF\b)(?! *Table of contents\b)(.+?\n?.*?\n?.*?)\.{2,}(.*)$')
accepted_toc = ['Figure', 'Table', 'Plate', 'Attachment', 'Detail', 'Drawing', 'Photograph', 'Photo',
                'Sheet', 'Tableau', 'Index', 'Overview']

figures_rex = re.compile(r'.*\bF[iI][gG][uU][rR][eE][sS]?\b')
tables_rex = re.compile(r'^T[aA][bB][lL][eE][sS]?\b')
small_word = re.compile(r'\b[a-zA-Z]{1,2}\b') # words that are 1 or 2 letters (no numbers or punctuation)
# cont_rex = re.compile(r'')
# extra_chars = re.compile(r'-|:|-|\(|\.') # extra characters we want to delete from string

exceptions_list = ['...', 'table of content', 'table des matières']




