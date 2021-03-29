import pandas as pd
import re
import regex
import pickle
from bs4 import BeautifulSoup
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import traceback
from sqlalchemy import text
from fuzzywuzzy import fuzz
import json
import numpy as np

from Codes.Database_Connection_Files.connect_to_database import connect_to_db
import Codes.Section_03_Table_and_Figure_Title_Extraction.constants as constants


engine = connect_to_db()


# take a project and assign all Figure titles from toc to a pdf id and page
def project_figure_titles(project):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            # get all fig titles for this project from db
            with engine.connect() as conn:
                params = {"project": project}
                stmt = text("SELECT toc.titleTOC, toc.page_name, toc.toc_page_num, toc.toc_pdfId, toc.toc_title_order "
                            "FROM esa.toc LEFT JOIN esa.pdfs ON toc.toc_pdfId = pdfs.pdfId "
                            "WHERE title_type='Figure' and short_name = :project "
                            "ORDER BY pdfs.short_name, toc.toc_pdfId, toc.toc_page_num, toc.toc_title_order;")
                df_figs = pd.read_sql_query(stmt, conn, params=params)

                stmt = text("SELECT pdfId FROM esa.pdfs WHERE short_name = :project;")
                project_df = pd.read_sql_query(stmt, conn, params=params)

            prev_id = 0
            project_ids = project_df['pdfId'].tolist()
            for index, row in df_figs.iterrows():
                title = row['titleTOC']
                c = title.count(' ')
                if c >= 2:
                    word1, word2, s2 = title.split(' ', 2)
                else:
                    word1, word2 = title.split(' ', 1)
                    s2 = ''
                word2 = re.sub('[^a-zA-Z0-9]$', '', word2)
                word2 = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
                word1_rex = re.compile(r'(?i)\b' + word1 + r'\s')
                word2_rex = re.compile(r'(?i)\b' + word2)
                s2 = re.sub(constants.punctuation, ' ', s2)  # remove punctuation
                s2 = re.sub(constants.whitespace, ' ', s2)  # remove whitespace
                toc_id = row['toc_pdfId']
                toc_page = row['toc_page_num']
                page_str = row['page_name']
                title_order = row['toc_title_order']
                page_rex = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
                page_rex = re.compile(r'(?i)\b' + page_rex + '\b')

                docs_check = [prev_id, toc_id]
                after = [i for i in project_ids if i > toc_id]
                after.sort()
                before = [i for i in project_ids if i < toc_id]
                before.sort(reverse=True)
                docs_check.extend(after)
                docs_check.extend(before)
                count = 0
                for doc_id in docs_check:
                    if doc_id > 0:
                        arg = (doc_id, toc_id, toc_page, title_order, word1_rex, word2_rex, s2.lower(), page_rex, title)
                        count = figure_checker(arg)
                    if count > 0:
                        prev_id = doc_id
                        break
                if count == 0:
                    # write 0 count to db
                    with engine.connect() as conn:
                        stmt = text(
                            "UPDATE esa.toc SET assigned_count = 0, loc_pdfId = null, loc_page_list = null  "
                            "WHERE (toc_pdfId = :pdf_id) and (toc_page_num = :page_num) and (toc_title_order = :title_order);")
                        params = {"pdf_id": toc_id, "page_num": toc_page, "title_order": title_order}
                        result = conn.execute(stmt, params)
                    if result.rowcount != 1:
                        print('could not assign 0 count to: ', toc_id, toc_page, title_order)
            return True, buf.getvalue()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


# For a Figure TOC title, find a pdf id and page where that figure lives
def figure_checker(args):
    conn = engine.connect()
    try:
        doc_id, toc_id, toc_page, toc_order, word1_rex, word2_rex, s2, page_rex, title = args

        # get pages where we have images for this document (from db)
        stmt = text("SELECT page_num, block_order, type as 'images', bbox_area_image, bbox_area FROM esa.blocks "
                    "WHERE (pdfId = :pdf_id) and (bbox_x0 >= 0) and (bbox_y0 >= 0) and (bbox_x1 >= 0) and (bbox_y1 >= 0);")
        params = {"pdf_id": doc_id}
        df = pd.read_sql_query(stmt, conn, params=params)
        df_pages = df[['page_num', 'bbox_area_image', 'bbox_area', 'images']].groupby('page_num', as_index=False).sum()
        df_pages['imageProportion'] = df_pages['bbox_area_image'] / df_pages['bbox_area']
        min_proportion = df_pages['imageProportion'].mean() if df_pages['imageProportion'].mean() < 0.1 else 0.1
        min_images = df_pages['images'].mean()
        df_pages = df_pages[(df_pages['imageProportion'] > min_proportion) | (df_pages['images'] > min_images)]
        image_pages = df_pages['page_num'].unique().tolist()
        # df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()

        stmt = text("SELECT page FROM esa.csvs WHERE (pdfId = :pdf_id) "
                    "and (titleFinal = '' or titleFinal is null) GROUP BY page;")
        params = {"pdf_id": doc_id}
        extra_pages_df = pd.read_sql_query(stmt, conn, params=params)
        extra_pages = [p for p in extra_pages_df['page'].tolist() if p not in image_pages] # list of extra pages to check

        # get text
        if len(extra_pages) > 0 and len(image_pages) > 0:
            params = {"pdf_id": doc_id, "image_list": image_pages, "extra_list": extra_pages}
            stmt = text("SELECT page_num, clean_content FROM esa.pages_normal_txt "
                        "WHERE (pdfId = :pdf_id) and (page_num in :image_list or page_num in :extra_list);")
            stmt_rotated = text("SELECT page_num, clean_content FROM esa.pages_rotated90_txt "
                                "WHERE (pdfId = :pdf_id) and (page_num in :image_list or page_num in :extra_list);")
            text_df = pd.read_sql_query(stmt, conn, params=params, index_col='page_num')
            text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

        elif len(image_pages) > 0:
            params = {"pdf_id": doc_id, "image_list": image_pages}
            stmt = text("SELECT page_num, clean_content FROM esa.pages_normal_txt "
                        "WHERE (pdfId = :pdf_id) and (page_num in :image_list);")
            stmt_rotated = text("SELECT page_num, clean_content FROM esa.pages_rotated90_txt "
                                "WHERE (pdfId = :pdf_id) and (page_num in :image_list);")
            text_df = pd.read_sql_query(stmt, conn, params=params, index_col='page_num')
            text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

        elif len(extra_pages) > 0:
            params = {"pdf_id": doc_id, "extra_list": extra_pages}
            stmt = text("SELECT page_num, clean_content FROM esa.pages_normal_txt "
                        "WHERE (pdfId = :pdf_id) and (page_num in :extra_list);")
            stmt_rotated = text("SELECT page_num, clean_content FROM esa.pages_rotated90_txt "
                                "WHERE (pdfId = :pdf_id) and (page_num in :extra_list);")
            text_df = pd.read_sql_query(stmt, conn, params=params, index_col='page_num')
            text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

        else:
            text_df = None
            text_rotated_df = None

        p_list = []
        sim_list = []
        ratio_list = []
        word2_list = []
        for check_list in [image_pages, extra_pages]:
            for page_num in check_list:
                if (doc_id != toc_id) or (page_num != toc_page):  # if not toc page
                    text_ws = text_df.loc[page_num, 'clean_content']
                    text_clean = re.sub(constants.punctuation, ' ', text_ws)
                    text_clean = re.sub(constants.whitespace, ' ', text_clean)
                    text_clean = text_clean.lower()

                    text_rotated_ws = text_rotated_df.loc[page_num, 'clean_content']
                    text_rotated_clean = re.sub(constants.punctuation, ' ', text_rotated_ws)
                    text_rotated_clean = re.sub(constants.whitespace, ' ', text_rotated_clean)
                    text_rotated_clean = text_rotated_clean.lower()

                    if re.search(word2_rex, text_ws) or re.search(word2_rex, text_rotated_ws): # check fig number
                        words = [word for word in s2.split() if (len(word) > 3) and (word != 'project')]
                        match = [word for word in words if (regex.search(r'(?i)\b' + word + r'{e<=1}\b', text_clean))
                                 or (regex.search(r'(?i)\b' + word + r'{e<=1}\b', text_rotated_clean))]
                        if len(words) > 0:
                            sim = len(match) / len(words)
                        else:
                            sim = 0

                        if sim >= 0.7: # check that enough words exists
                            l = len(s2)
                            ratio = 0
                            for i in range(len(text_clean) - l + 1):
                                r = fuzz.ratio(s2, text_clean[i:i + l])
                                if r > ratio:
                                    ratio = r
                                if ratio == 1:
                                    break
                            for i in range(len(text_rotated_clean) - l + 1):
                                if ratio == 1:
                                    break
                                r = fuzz.ratio(s2, text_rotated_clean[i:i + l])
                                if r > ratio:
                                    ratio = r
                            # ratio = max(fuzz.partial_ratio(s2, text_clean),
                            #             fuzz.partial_ratio(s2, text_rotated_clean))

                            if ratio >= 60:  # check that the fuzzy match is close enough
                                p_list.append(page_num)
                                sim_list.append(sim)
                                ratio_list.append(ratio)

            if len(sim_list) > 0:  # if found in image pages don't check extra pages
                break

        # only keep those with largest sim
        if len(sim_list) > 0:
            max_sim = max(sim_list)
            p_list2 = []
            ratio_list2 = []
            for i, sim in enumerate(sim_list):
                if sim >= max_sim:
                    p_list2.append(p_list[i])
                    ratio_list2.append(ratio_list[i])
            max_ratio = max(ratio_list2)
            # now only keep those with largest ratio
            final_list = [{'page_num':int(p_list2[i]), 'sim':max_sim, 'ratio':ratio} for i, ratio in enumerate(ratio_list2) if ratio >= max_ratio]
        else:
            final_list = []
        count = len(final_list)

        if count > 0:
            stmt = text("UPDATE esa.toc SET assigned_count = :count, loc_pdfId = :loc_id, loc_page_list = :loc_pages "
                        "WHERE (toc_pdfId = :pdf_id) and (toc_page_num = :page_num) and (toc_title_order = :title_order);")
            params = {"count": count, "loc_id": doc_id, "loc_pages": json.dumps(final_list), "pdf_id": toc_id, "page_num": toc_page, "title_order": toc_order}
            result = conn.execute(stmt, params)
            if result.rowcount != 1:
                print('could not assign TOC count to: ', toc_id, toc_page, toc_order)

        conn.close()
        return count
    except Exception as e:
        conn.close()
        print('Error in', doc_id)
        print(traceback.print_tb(e.__traceback__))
        return 0


# determine category of table tag title (if continued title --> 1, if regular title --> 2, if just text --> 0)
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


def find_tag_title_table(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            # get tables for this document
            stmt = text("SELECT page, tableNumber FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            if df.empty:
                df['Real Order'] = None
            else:
                df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()
            table_pages = df['page'].unique().tolist()

            if len(table_pages) > 0:
                params = {"pdf_id": data_id, "table_list": table_pages}
                stmt = text("SELECT page_num, content FROM esa.pages_normal_txt "
                            "WHERE (pdfId = :pdf_id) and (page_num in :table_list);")
                stmt_rotated = text("SELECT page_num, content FROM esa.pages_rotated90_txt "
                                    "WHERE (pdfId = :pdf_id) and (page_num in :table_list);")
                text_df = pd.read_sql_query(stmt, conn, params=params, index_col='page_num')
                text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

                for page_num in table_pages:
                    page_tables = df[df['page'] == page_num].set_index('Real Order')
                    page_text = text_df.loc[page_num, 'content']
                    page_text_rotated = text_rotated_df.loc[page_num, 'content']
                    lines = page_text.split('\n\n')
                    lines_rotated = page_text_rotated.split('\n\n')

                    final_table_titles = []  # holds all titles found on this page

                    # unrotated
                    num_lines = len(lines)
                    for i, line in enumerate(lines):
                        title = re.sub(constants.whitespace, ' ', line).strip()  # replace all whitespace with single space
                        # identify if this line is a table line (took out exceptions, should not need)
                        if re.match(constants.tables_rex, title):  # and not any(x in line.lower() for x in exceptions_list):
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

                    # rotated
                    if len(final_table_titles) == 0:
                        num_lines = len(lines_rotated)
                        for i, line in enumerate(lines_rotated):
                            title = re.sub(constants.whitespace, ' ', line).strip()  # replace all whitespace with single space
                            # identify if this line is a table line (took out exceptions, should not need)
                            if re.match(constants.tables_rex, title):  # and not any(x in line.lower() for x in exceptions_list):
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
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            conn.close()
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def find_tag_title_fig(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            # get tables for this document
            stmt = text("SELECT page_num, block_order, type, bbox_area_image, bbox_area FROM esa.blocks "
                        "WHERE (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            df_pages = df[['page_num', 'bbox_area_image', 'bbox_area']].groupby('page_num', as_index=False).sum()
            df_pages['imageProportion'] = df_pages['bbox_area_image'] / df_pages['bbox_area']
            df_pages = df_pages[df_pages['imageProportion'] > 0.1]
            # df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()

            # get text for this document
            path = constants.pickles_path + str(data_id) + '.pkl'
            path_rotated = constants.pickles_rotated_path + str(data_id) + '.pkl'
            with open(path, 'rb') as f:
                data = pickle.load(f)
            soup = BeautifulSoup(data['content'], 'lxml')
            pages = soup.find_all('div', attrs={'class': 'page'})
            figs_pages = df_pages['page_num'].tolist()

            for page_num in figs_pages:
                page_figs = df[df['page_num'] == page_num].reset_index() #.set_index('Real Order')
                page_text = pages[page_num - 1]
                lines = [x.text for x in page_text.find_all('p')]  # list of lines
                final_table_titles = []  # holds all titles found on this page
                for i, line in enumerate(lines):
                    title = re.sub(constants.whitespace, ' ', line).strip()  # replace all whitespace with single space
                    # identify if this line is a figure line (took out exceptions, should not need)
                    if re.match(constants.figures_rex, title):  # and not any(x in line.lower() for x in exceptions_list):
                        # if i < num_lines - 1:
                        #     title_next = re.sub(constants.whitespace, ' ', lines[i + 1]).strip()
                        # else:
                        #     title_next = ''
                        # category = get_category(title)
                        # if category > 0:
                        #     if category == 2:
                        #         final_table_title = title + ' ' + title_next
                        #     else:
                        #         final_table_title = title
                        final_table_titles.append(title)

                count_figs = page_figs.shape[0]
                for i, title in enumerate(final_table_titles):
                    if i < count_figs:
                        # update the db
                        block_num = page_figs.loc[i, 'block_order']
                        stmt = text("UPDATE esa.blocks SET titleTag = :title_tag WHERE (pdfId = :pdf_id) and "
                                    "(page_num = :page_num) and (block_order = :block_num);")
                        params = {"pdf_id": data_id, "page_num": page_num, "block_num": block_num, "title_tag": title}
                        result = conn.execute(stmt, params)
                        if result.rowcount != 1:
                            print('Did not go to database:', data_id, '_', page_num, '_', block_num, '_', i+1, ':', title,
                                  ': error:', result)
                    else:
                        print('No table for:', data_id, '_', page_num, '_', i + 1, ':', title)
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            conn.close()
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def table_checker(args):
    conn = engine.connect()
    try:
        doc_id, toc_id, toc_page, toc_order, word1_rex, word2_rex, s2_rex, page_rex, title = args
        # get tables for this document
        stmt = text("SELECT page, tableNumber FROM esa.csvs "
                    "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                    "and (pdfId = :pdf_id);")
        params = {"pdf_id": doc_id}
        df = pd.read_sql_query(stmt, conn, params=params)
        if df.empty:
            df['Real Order'] = None
        else:
            df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()
        table_pages = df['page'].unique().tolist()

        count = 0
        if len(table_pages) > 0:
            params = {"pdf_id": doc_id, "table_list": table_pages}
            stmt = text("SELECT page_num, content FROM esa.pages_normal_txt "
                        "WHERE (pdfId = :pdf_id) and (page_num in :table_list);")
            stmt_rotated = text("SELECT page_num, content FROM esa.pages_rotated90_txt "
                                "WHERE (pdfId = :pdf_id) and (page_num in :table_list);")
            text_df = pd.read_sql_query(stmt, conn, params=params, index_col='page_num')
            text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

            p_list = []
            for page_num in table_pages:
                if (doc_id != toc_id) or (page_num != toc_page):  # if not toc page
                    text_ws = text_df.loc[page_num, 'content']
                    text_clean = re.sub(constants.punctuation, ' ', text_ws)
                    text_clean = re.sub(constants.whitespace, ' ', text_clean)
                    text_clean = text_clean.lower()

                    text_rotated_ws = text_rotated_df.loc[page_num, 'content']
                    text_rotated_clean = re.sub(constants.punctuation, ' ', text_rotated_ws)
                    text_rotated_clean = re.sub(constants.whitespace, ' ', text_rotated_clean)
                    text_rotated_clean = text_rotated_clean.lower()

                    if re.search(word1_rex, text_ws) or re.search(word1_rex, text_rotated_ws):
                        if re.search(word2_rex, text_ws) or re.search(word2_rex, text_rotated_ws) :
                            if re.search(s2_rex, text_clean) or re.search(s2_rex, text_rotated_clean):
                                p_list.append(page_num)

            count = len(p_list)
            # assign pages to the title in toc table
            if (count > 0):
                stmt = text("UPDATE esa.toc SET assigned_count = :count, loc_pdfId = :loc_id, loc_page_list = :loc_pages "
                            "WHERE (toc_pdfId = :pdf_id) and (toc_page_num = :page_num) and (toc_title_order = :title_order);")
                params = {"count": count, "loc_id": doc_id, "loc_pages": json.dumps(p_list), "pdf_id": toc_id, "page_num": toc_page, "title_order": toc_order}
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    print('could not assign TOC count to: ', toc_id, toc_page, toc_order)
        conn.close()
        return count
    except Exception as e:
        conn.close()
        print('Error in', doc_id)
        print(traceback.print_tb(e.__traceback__))
        return 0


def project_table_titles(project):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            with engine.connect() as conn:
                params = {"project": project}
                stmt = text("SELECT toc.titleTOC, toc.page_name, toc.toc_page_num, toc.toc_pdfId, toc.toc_title_order "
                            "FROM esa.toc LEFT JOIN esa.pdfs ON toc.toc_pdfId = pdfs.pdfId "
                            "WHERE title_type='Table' and short_name = :project "
                            "ORDER BY pdfs.short_name, toc.toc_pdfId, toc.toc_page_num, toc.toc_title_order;")
                df_tables = pd.read_sql_query(stmt, conn, params=params)

                stmt = text("SELECT pdfId FROM esa.pdfs WHERE short_name = :project;")
                project_df = pd.read_sql_query(stmt, conn, params=params)

            prev_id = 0
            project_ids = project_df['pdfId'].tolist()
            for index, row in df_tables.iterrows():
                title = row['titleTOC']
                c = title.count(' ')
                if c >= 2:
                    word1, word2, s2 = title.split(' ', 2)
                else:
                    word1, word2 = title.split(' ', 1)
                    s2 = ''

                word2 = re.sub('[^a-zA-Z0-9]$', '', word2)
                word2 = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
                word1_rex = re.compile(r'(?i)\b' + word1 + r'\s')
                word2_rex = re.compile(r'(?i)\b' + word2 + r'\b')
                s2 = re.sub(constants.punctuation, ' ', s2)  # remove punctuation
                s2 = re.sub(constants.whitespace, ' ', s2)  # remove whitespace
                s2_rex = r'(?i)\b'
                for s in s2.split(' '):
                    s2_rex = s2_rex + r'[^\w]*' + s
                s2_rex = s2_rex + r'\b'

                toc_id = row['toc_pdfId']
                toc_page = row['toc_page_num']
                page_str = row['page_name']
                title_order = row['toc_title_order']
                page_rex = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
                page_rex = re.compile(r'(?i)\b' + page_rex + '\b')

                docs_check = [prev_id, toc_id]
                after = [i for i in project_ids if i > toc_id]
                after.sort()
                before = [i for i in project_ids if i < toc_id]
                before.sort(reverse=True)
                docs_check.extend(after)
                docs_check.extend(before)
                count = 0

                for doc_id in docs_check:
                    if doc_id > 0:
                        arg = (doc_id, toc_id, toc_page, title_order, word1_rex, word2_rex, s2_rex, page_rex, title)
                        count = table_checker(arg)
                    if count > 0:
                        prev_id = doc_id
                        break
                if count == 0:
                    # write 0 count to db
                    with engine.connect() as conn:
                        stmt = text(
                            "UPDATE esa.toc SET assigned_count = 0, loc_pdfId = null, loc_page_list = null  "
                            "WHERE (toc_pdfId = :pdf_id) and (toc_page_num = :page_num) and (toc_title_order = :title_order);")
                        params = {"pdf_id": toc_id, "page_num": toc_page, "title_order": title_order}
                        result = conn.execute(stmt, params)
                    if result.rowcount != 1:
                        print('could not assign 0 count to: ', toc_id, toc_page, title_order)
            return True, buf.getvalue()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def find_toc_title_table(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            stmt = text("SELECT page, tableNumber FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            if not df.empty:
                df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()
                # get all tocs titles for this doc
                stmt = text("SELECT titleTOC, loc_page_list FROM esa.toc "
                            "WHERE (loc_pdfId = :pdf_id) and (title_type='Table') and (assigned_count > 0) "
                            "ORDER BY toc_pdfId, toc_page_num, toc_title_order;")
                params = {"pdf_id": data_id}
                df_all_titles = pd.read_sql_query(stmt, conn, params=params)

                for index, row in df.iterrows():
                    page_num = int(row['page'])
                    table_num = int(row['tableNumber'])
                    order = int(row['Real Order'])
                    # get the title for that page and order
                    ts = [i for i, r in df_all_titles.iterrows() if page_num in json.loads(r['loc_page_list'])]

                    if len(ts) >= order:
                        title = df_all_titles.loc[ts[order-1], 'titleTOC']
                        # update the db
                        stmt = text("UPDATE esa.csvs SET titleTOC = :title_toc WHERE (pdfId = :pdf_id) and "
                                    "(page = :page_num) and (tableNumber = :table_num);")
                        params = {"pdf_id": data_id, "page_num": page_num, "table_num": table_num, "title_toc": title}
                        result = conn.execute(stmt, params)
                        if result.rowcount != 1:
                            print('Did not go to database:', data_id, '_', page_num, '_', table_num, '_', order, ':', title,
                                  ': error:', result)
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            conn.close()
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def find_toc_title_fig(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            # get tables for this document
            stmt = text("SELECT page_num, block_order, type, bbox_area_image, bbox_area FROM esa.blocks "
                        "WHERE (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            df_pages = df[['page_num', 'bbox_area_image', 'bbox_area']].groupby('page_num', as_index=False).sum()
            df_pages['imageProportion'] = df_pages['bbox_area_image'] / df_pages['bbox_area']
            df_pages = df_pages[df_pages['imageProportion'] > 0.1]
            # df['Real Order'] = df.groupby(['page'])['tableNumber'].rank()

            df_all_titles = pd.read_csv(constants.main_path + 'Saved/final_figs.csv', header=0)
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
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            conn.close()
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def find_final_title_table(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            # get tables for this document
            stmt = text("SELECT page, tableNumber, titleTag, titleTOC, topRowJson FROM esa.csvs "
                        "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78) "
                        "and (pdfId = :pdf_id);")
            params = {"pdf_id": data_id}
            df = pd.read_sql_query(stmt, conn, params=params)
            if not df.empty:
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
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            print('errors on title:', title)
            conn.close()
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()


def find_final_title_fig(data_id):
    buf = StringIO()
    conn = engine.connect()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
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
            conn.close()
            return True, buf.getvalue()
        except Exception as e:
            conn.close()
            print('errors on title:', title)
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue()
