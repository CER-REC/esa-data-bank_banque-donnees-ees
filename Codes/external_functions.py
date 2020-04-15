import pandas as pd
import re
import time
from multiprocessing import Pool
import pickle
from bs4 import BeautifulSoup
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import traceback
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import os
from fuzzywuzzy import fuzz
import json
import numpy as np

import constants

load_dotenv(override=True)
engine_string = f"mysql+mysqldb://esa_user_rw:{os.getenv('DB_PASS')}@os25.neb-one.gc.ca./esa?charset=utf8"
engine = create_engine(engine_string)

def figure_checker(args):
    doc_id, toc_id, toc_page, word1_rex, word2_rex, s2_rex = args
    # get the text and rotated text
    with open(constants.pickles_path + str(doc_id) + '.pkl', 'rb') as f:  # unrotated pickle
        data = pickle.load(f)
    with open(constants.pickles_rotated_path + str(doc_id) + '.pkl', 'rb') as f:  # rotated pickle
        data_rotated = pickle.load(f)
    doc_text = data['content']
    doc_text_rotated = data_rotated['content']  # save the rotated text

    buf = StringIO()
    p_list = []
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            print("Start.")
            # check unrotated
            if '<body>' in doc_text:
                soup = BeautifulSoup(doc_text, 'lxml')
                pages = soup.find_all('div', attrs={'class': 'page'})
                for page_num, page in enumerate(pages):
                    text_clean = re.sub(constants.whitespace, ' ', page.text)
                    # text_clean = re.sub(punctuation, ' ', text_clean)
                    if re.search(word2_rex, text_clean) and re.search(s2_rex, text_clean):
                        if (page_num not in p_list) and ((doc_id != toc_id) or (page_num != toc_page)):
                            p_list.append(page_num)

                # check rotated
                soup = BeautifulSoup(doc_text_rotated, 'lxml')
                pages = soup.find_all('div', attrs={'class': 'page'})
                for page_num, page in enumerate(pages):
                    text_clean = re.sub(constants.whitespace, ' ', page.text)
                    # text_clean = re.sub(punctuation, ' ', text_clean)
                    if re.search(word2_rex, text_clean) and re.search(s2_rex, text_clean):
                        if (page_num not in p_list) and ((doc_id != toc_id) or (page_num != toc_page)):
                            p_list.append(page_num)
            print(f"Success. Found data on {len(p_list)} pages.")
            return True, buf.getvalue(), p_list, doc_id
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue(), p_list, doc_id

def get_category(title):
    category = False
    # title_clean = re.sub(extra_chars, '', title) # get rid of some extra characters
    title_clean = re.sub(constants.punctuation, '', title)  # remove punctuation
    title_clean = re.sub(constants.small_word, '', title_clean)  # delete any 1 or 2 letter words without digits
    title_clean = re.sub(constants.whitespace, ' ', title_clean).strip()  # replace whitespace with single space
    num_words = title_clean.count(' ') + 1
    _, _, third, _ = (title_clean + '   ').split(' ', 3)

    if num_words <= 3:
        if 'cont' in title_clean.lower():  # if any word starts with cont
            category = 1
        else:
            category = 2
    else:
        if third.lower().startswith('cont') or third[0].isdigit() or third[0].isupper():
            category = 1
        else:
            category = 0
    return category

def find_tag_title(data_id):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            conn = engine.connect()
            # get tables for this document
            stmt = text("SELECT page, tableNumber FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()

            # get text for this document
            path = constants.pickles_path + str(data_id) + '.pkl'
            with open(path, 'rb') as f:
                data = pickle.load(f)
            soup = BeautifulSoup(data['content'], 'lxml')
            pages = soup.find_all('div', attrs={'class': 'page'})
            tables_pages = df['page'].unique()

            for page_num in tables_pages:
                page_tables = df[df['page'] == page_num].set_index('Real Order')
                page_text = pages[page_num - 1]
                lines = [x.text for x in page_text.find_all('p')]  # list of lines
                num_lines = len(lines)
                final_table_titles = [] # holds all titles found on this page
                for i, line in enumerate(lines):
                    title = re.sub(constants.whitespace, ' ', line).strip()  # replace all whitespace with single space
                    # identify if this line is a table line (took out exceptions, should not need)
                    if re.match(constants.tables_rex, line):  # and not any(x in line.lower() for x in exceptions_list):
                        if i < num_lines - 1:
                            title_next = re.sub(constants.whitespace, ' ', lines[i + 1]).strip()
                        else:
                            title_next = ''
                        category = get_category(title)
                        if category > 0:
                            if category == 2:
                                final_table_title = title + ' ' + title_next
                            else:
                                final_table_title = title
                            final_table_titles.append(final_table_title)

                count_tables = page_tables.shape[0]
                for i, title in enumerate(final_table_titles):
                    if i < count_tables:
                        # update the db
                        table_num = page_tables.loc[i+1, 'tableNumber']
                        stmt = text("UPDATE esa.csvs SET titleTag = :title_tag WHERE (pdfId = :pdf_id) and "
                                    "(page = :page_num) and (tableNumber = :table_num);")
                        params = {"pdf_id": data_id, "page_num": page_num, "table_num": table_num, "title_tag": title}
                        result = conn.execute(stmt, params)
                        if result.rowcount != 1:
                            print('Did not go to database:', data_id, '_', page_num, '_', table_num, '_', i+1, ':', title,
                                  ': error:', result)
                    else:
                        print('No table for:', data_id, '_', page_num, '_', i + 1, ':', title)
            return True, buf.getvalue()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()
        finally:
            conn.close()

def find_toc_title(data_id):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            conn = engine.connect()
            # get tables for this document
            stmt = text("SELECT page, tableNumber FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()
            # print(data_id, df.shape)

            df_all_titles = pd.read_csv(constants.main_path + 'Saved/final_tables.csv', header=0)
            df_all_titles['location_DataID'] = df_all_titles['location_DataID'].fillna(0)
            df_all_titles['location_Page'] = df_all_titles['location_Page'].fillna('')
            df_all_titles['location_DataID'] = np.where(df_all_titles['location_DataID'].str.contains(','), 0,
                                                        df_all_titles['location_DataID'])
            df_all_titles['location_DataID'] = pd.to_numeric(df_all_titles['location_DataID'], errors='ignore',
                                                             downcast='integer')
            df_all_titles = df_all_titles[df_all_titles['location_DataID'] == data_id]
            df_temp = df_all_titles.copy()

            for index, row in df.iterrows():
                page_num = int(row['page'])
                table_num = int(row['tableNumber'])
                # find TOC title and assign
                page_rex = r'\b' + str(page_num - 1) + r'\b'
                order = int(row['Real Order'])
                df_titles = df_all_titles[df_all_titles['location_Page'].str.contains(page_rex, regex=True)].reset_index()
                if df_titles.shape[0] >= order:
                    title = df_titles.loc[order-1, 'Name']
                    # update the db
                    stmt = text("UPDATE esa.csvs SET titleTOC = :title_toc WHERE (pdfId = :pdf_id) and "
                                "(page = :page_num) and (tableNumber = :table_num);")
                    params = {"pdf_id": data_id, "page_num": page_num, "table_num": table_num, "title_toc": title}
                    result = conn.execute(stmt, params)
                    if result.rowcount != 1:
                        print('Did not go to database:', data_id, '_', page_num, '_', table_num, '_', order, ':', title,
                              ': error:', result)
                    df_temp = df_temp[df_temp['Name'] != title]

            for i, row in df_temp.iterrows():
                print('Could not find table for:', data_id, '_', row['location_Page'], ':', row['Name'])
            return True, buf.getvalue()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()
        finally:
            conn.close()

def find_final_title(data_id):
    # print(data_id)
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            conn = engine.connect()
            # get tables for this document
            stmt = text("SELECT page, tableNumber, titleTag, titleTOC, topRowJson FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()
            df['titleFinal'] = df['titleTag'].fillna(df['titleTOC']).fillna('')
            # sort df by page and then order
            df.sort_values(['page', 'Real Order'], ignore_index=True, inplace=True)

            prev_title = ''
            prev_cols_list = []
            # fill titles that are continuation of tables
            for index, row in df.iterrows():
                cols_list = json.loads(row['topRowJson'])
                title = row['titleFinal']
                page_num = row['page']
                table_num = row['tableNumber']
                # print('try title: ', title)
                if (title == '') or ('cont' in title.lower()):
                    # check against previous table's columns
                    cols = ', '.join(cols_list)
                    prev_cols = ', '.join(prev_cols_list)
                    ratio_similarity = fuzz.token_sort_ratio(cols, prev_cols)
                    if len(set(prev_cols_list).difference(set(cols_list))) == 0 \
                            or len(prev_cols_list) == len(cols_list) \
                            or ratio_similarity > 89:
                        title = prev_title
                # update database
                stmt = text("UPDATE esa.csvs SET titleFinal = :title WHERE (pdfId = :pdf_id) and "
                            "(page = :page_num) and (tableNumber = :table_num);")
                params = {"pdf_id": data_id, "page_num": page_num, "table_num": table_num, "title": title}
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    print('Could not find:', data_id, '_', page_num, '_', table_num, ':', title, ': error:', result)
                prev_title = title
                prev_cols_list = cols_list
            return True, buf.getvalue()
        except Exception as e:
            print('errors on title:', title)
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()
        finally:
            conn.close()
