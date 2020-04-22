import pandas as pd
import pickle
from bs4 import BeautifulSoup
import re
import os
from multiprocessing import Pool
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import time

from Codes.external_functions import figure_checker
from Codes.external_functions import find_tag_title_table, find_toc_title_table, find_final_title_table
from Codes.external_functions import find_tag_title_fig, find_toc_title_fig, find_final_title_fig
import Codes.constants as constants

load_dotenv(override=True)
engine_string = f"mysql+mysqldb://esa_user_rw:{os.getenv('DB_PASS')}@os25.neb-one.gc.ca./esa?charset=utf8"
engine = create_engine(engine_string)

get_toc = 0  # need to go through all docs to create lists of tables and figures in csvs
get_figure_titles = 1  # find all figs page #
get_table_titles = 0
do_tag_title_table = 0  # assign table titles to each table using text search method
do_toc_title_table = 0  # assign table titles to each table using TOC method
do_final_title_table = 0  # replace continued tables and create final table title
do_tag_title_fig = 0  # assign table titles to each table using text search method
do_toc_title_fig = 0  # assign table titles to each table using TOC method
do_final_title_fig = 0  # replace continued tables and create final table title

if __name__ == "__main__":
    # get list of all documents
    with engine.connect() as conn:
        stmt = text("SELECT pdfId, hearingOrder, short_name FROM esa.pdfs;")
        all_projects = pd.read_sql_query(stmt, conn)
    projects = all_projects['short_name'].unique()
    list_ids = all_projects['pdfId'].tolist()
    # print(len(projects))
    # print(projects)

    # now get TOC from each document and create a list of all figs and tables (that were found in TOC's)
    if get_toc:
        print('Searching for TOC tables and figures')
        conn = engine.connect()
        for index, row in all_projects.iterrows():
            doc_id = row['pdfId']
            with open(constants.pickles_path + str(doc_id) + '.pkl', 'rb') as f:  # unrotated pickle
                data = pickle.load(f)
            # with open(constants.pickles_rotated_path + str(doc_id) + '.pkl', 'rb') as f:  # rotated pickle
            #     data_rotated = pickle.load(f)
            content = data['content']
            # content_rotated = data_rotated['content']  # save the rotated text

            # find tables of content and list of figures in the unrotated text
            soup = BeautifulSoup(content, 'lxml')
            pages = soup.find_all('div', attrs={'class': 'page'})
            for page_num, page in enumerate(pages):
                # delete any existing TOC from this page
                stmt = text("DELETE FROM esa.toc WHERE toc_pdfId = :pdfId and toc_page_num = :page_num;")
                params = {"pdfId": doc_id, "page_num": page_num+1}
                result = conn.execute(stmt, params)

                # extract TOC
                clean_text = re.sub(constants.empty_line, '', page.text)  # get rid of empty lines
                tocs = re.findall(constants.toc, clean_text)
                for i, toc in enumerate(tocs):
                    title = re.sub(constants.whitespace, ' ', toc[0]).strip()
                    page_name = toc[1].strip()
                    type = title.split(' ', 1)[0].capitalize()
                    if type in constants.accepted_toc: # if accepted type
                        stmt = text("INSERT INTO esa.toc (assigned_count, title_type, titleTOC, page_name, "
                                    "toc_page_num, toc_pdfId, toc_title_order) "
                                    "VALUE (null, :type, :title, :page_name, :page_num, :pdfId, :order);")
                        params = {"type": type, "title":title, "page_name":page_name,
                                  "page_num":page_num+1, "pdfId":doc_id, "order":i+1}
                        result = conn.execute(stmt, params)
                        if result.rowcount != 1:
                            print('Did not go to database:',doc_id, page_num+1, toc)
        conn.close()

    if get_table_titles:
        # put them all together
        for project in projects:
            # need to fix this
            # get_titles_tables(project)
            y = 0
        data = []
        projects = all_projects['Hearing order'].unique()
        for project in projects:
            df = pd.read_csv(constants.save_dir + project + '-final_tables.csv', encoding='utf-8-sig')
            data.append(df)
        df_all = pd.concat(data, axis=0, ignore_index=True)
        df_all.to_csv(constants.save_dir + 'final_tables.csv', index=False, encoding='utf-8-sig')

    # get page numbers for all the figures found in TOC
    if get_figure_titles:
        # get all fig titles from db
        # df_figs = pd.read_csv(constants.save_dir + 'all_figs.csv', encoding='utf-8-sig')
        with engine.connect() as conn:
            stmt = text("SELECT toc.titleTOC, toc.page_name, toc.toc_page_num, toc.toc_pdfId, toc.toc_title_order, pdfs.short_name "
                        "FROM esa.toc LEFT JOIN esa.pdfs ON toc.toc_pdfId = pdfs.pdfId WHERE title_type='Figure' "
                        "ORDER BY pdfs.short_name, toc.toc_pdfId, toc.toc_page_num, toc.toc_title_order;")
            df_figs = pd.read_sql_query(stmt, conn)

        # prev_id = 0
        prev_pr = ''
        for index, row in df_figs.iterrows():
            # for i in range(1600, df_figs.shape[0]):
            t1 = time.time()
            # index = i
            # row = df_figs.iloc[index, :]
            project = row['short_name']
            if prev_pr != project:
                project_ids = all_projects[all_projects['short_name'] == project]['pdfId'].tolist()
                prev_id = 0
                prev_pr = project
            title = row['titleTOC']
            c = title.count(' ')
            if c >= 2:
                word1, word2, s2 = title.split(' ', 2)
            else:
                word1, word2 = title.split(' ', 1)
                s2 = ''
            word2 = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
            word1_rex = re.compile(r'(?i)\b' + word1 + r'\s')
            word2_rex = re.compile(r'(?i)\b' + word2)
            s2 = re.sub(constants.whitespace, ' ', s2)  # remove whitespace
            s2_a = re.sub(constants.punctuation, '.*', s2) # allow anything in place of punctuation
            s2_rex = r'(?i)\b'

            for s in s2_a.split(' '):
                s2_rex = s2_rex + r'[^\w]*' + s
                s2_len = len(s2_rex)
                if s2_len > 200:
                    break
            s2_rex = s2_rex + r'\b'
            s2_rex = re.compile(s2_rex)
            toc_id = row['toc_pdfId']
            toc_page = row['toc_page_num']
            page_str = row['page_name']
            title_order = row['toc_title_order']
            page_rex = re.sub('[^a-zA-Z0-9]', '[^a-zA-Z0-9]', word2)
            page_rex = re.compile(r'(?i)\b' + page_rex + '\b')

            id_list = []
            page_list = []
            count = 0

            # if toc_id != 2967773:
            # do this for the list of docs to check, list of all docs in this project
            # first check previous and toc id's

            docs_check = [prev_id, toc_id]
            docs_check.extend(project_ids)
            count = 0
            for doc_id in docs_check:
                if (doc_id > 0):
                    arg = (doc_id, toc_id, toc_page, word1_rex, word2_rex, s2, s2_rex, page_rex, title)
                    count = figure_checker(arg)
                    # update db with count
                if count > 0:
                    prev_id = doc_id
                    break
            with engine.connect() as conn:
                stmt = text("UPDATE esa.toc SET assigned_count = :count "
                            "WHERE (toc_pdfId = :pdf_id) and (toc_page_num = :page_num) and (toc_title_order = :title_order);")
                params = {"count": count, "pdf_id": toc_id, "page_num": toc_page, "title_order": title_order}
                result = conn.execute(stmt, params)
                if result.rowcount != 1:
                    print('could not assign TOC count to: ', toc_id, toc_page, title_order)
            print(index, time.time() - t1)

    # update tag method titles
    if do_tag_title_table:
        # print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_tag_title_table, list_ids)
        with open('tag_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open('tag_errors.txt', 'a', encoding='utf-8') as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))

    # update TOC method titles
    if do_toc_title_table:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_toc_title_table, list_ids)
        with open('toc_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open("toc_errors.txt", "a", encoding='utf-8') as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    # update final titles
    if do_final_title_table:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_final_title_table, list_ids)
        with open('final_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open("final_errors.txt", "a", encoding='utf-8') as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    with engine.connect() as conn:
        stmt = text("SELECT csvFullPath, pdfId, page, tableNumber, topRowJson, titleTag, titleTOC, titleFinal FROM esa.csvs "
                    "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78);")
        df = pd.read_sql_query(stmt, conn)
    df.to_csv(constants.save_dir + 'all_tables-final.csv', index=False, encoding='utf-8-sig')

    # do similar process for figures

    # update tag method titles

    if do_tag_title_fig:
        # print(len(list_ids))

        # sequential
        # for doc_id in list_ids:
        #     print(doc_id)
        #     find_tag_title_fig(doc_id)

        # milti process
        with Pool() as pool:
            results = pool.map(find_tag_title_fig, list_ids)
        with open('tag_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open('tag_errors.txt', 'a', encoding='utf-8') as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))


    # update final titles
    if do_final_title_fig:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_final_title_fig, list_ids)
        with open('final_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open("final_errors.txt", "a", encoding='utf-8') as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    with engine.connect() as conn:
        stmt = text("SELECT pdfs.hearingOrder, pdfs.short_name, blocks.pdfId, blocks.page_num, blocks.block_order, "
                    "blocks.titleTag, blocks.titleTOC, blocks.titleFinal "
                    "FROM esa.blocks LEFT JOIN esa.pdfs ON pdfs.pdfId = blocks.pdfId "
                    "WHERE titleTOC is not null;")
        df = pd.read_sql_query(stmt, conn)
        df.to_csv(constants.save_dir + 'final_figs_pivoted.csv', index=False, encoding='utf-8-sig')

        stmt = text("SELECT pdfs.hearingOrder, pdfs.short_name, T.* FROM  "
                    "(SELECT min(pdfId) as pdfId, concat(page_num + ',') as page_list, titleTOC "
                    "FROM esa.blocks WHERE titleTOC is not null "
                    "GROUP BY titleTOC) T LEFT JOIN esa.pdfs ON pdfs.pdfId = T.pdfId;")
        df = pd.read_sql_query(stmt, conn)
        df.to_csv(constants.save_dir + 'final_figs.csv', index=False, encoding='utf-8-sig')

