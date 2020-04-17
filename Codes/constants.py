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
empty_line = re.compile(r'<\/p>\s*<p ?\/?>')
whitespace = re.compile(r'\s+') # all white space
punctuation = re.compile(r'[^\w\s]') # punctuation (not letter or number)
figure = re.compile(r'(?im)(^Figure .*?\n?.*?)\.{2,}(.*)')
table = re.compile(r'(?im)(^Table (?!of contents?).*?\n?.*?)\.{2,}(.*)')
# tables_rex = re.compile(r'^(F[iI][gG][uU][rR][eE]|I[mM][aA][gG][eE]|P[hH][oO][tT][oO]|T[aA][bB][lL][eE])[sS]? ')
figures_rex = re.compile(r'.*\bF[iI][gG][uU][rR][eE][sS]?\b')
tables_rex = re.compile(r'[^|\n]T[aA][bB][lL][eE][sS]?\b')
small_word = re.compile(r'\b[a-zA-Z]{1,2}\b') # words that are 1 or 2 letters (no numbers or punctuation)
# cont_rex = re.compile(r'')
# extra_chars = re.compile(r'-|:|-|\(|\.') # extra characters we want to delete from string

exceptions_list = ['...', 'table of content', 'table des matières']




