import pandas as pd
import numpy as np
import pickle
from bs4 import BeautifulSoup
import re
import os
from multiprocessing import Pool
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import time

from external_functions import get_titles_figures, get_titles_tables, find_tag_title, find_toc_title, find_final_title
from external_external_functions import figure_checker
import constants

load_dotenv(override=True)
engine_string = f"mysql+mysqldb://esa_user_rw:{os.getenv('DB_PASS')}@os25.neb-one.gc.ca./esa?charset=utf8"
engine = create_engine(engine_string)

load_pickles = 0  # need to load text from pickles and save to each project's csv
get_toc = 0  # need to go through all docs to create lists of tables and figures in csvs
get_figure_titles = 1  # find all figs page #
get_table_titles = 0  # find all table page #
do_tag_title = 0  # assign table titles to each table using text search method
do_toc_title = 0  # assign table titles to each table using TOC method
do_final_title = 0  # replace continued tables and create final table title

if __name__ == "__main__":
    # get list of all documents and projects (Index2)
    if True:
        # put it all together
        with engine.connect() as conn:
            stmt = text("SELECT pdfId, hearingOrder, short_name FROM esa.pdfs;")
            all_projects = pd.read_sql_query(stmt, conn)
            projects = all_projects['short_name'].unique()
    else:
        all_projects = pd.read_excel(constants.projects_path)
        projects = all_projects['Hearing order'].unique()
    # print(len(projects))
    # print(projects)

    # get text for each document in all projects
    if load_pickles:
        print('Creating project csvs with text')
        for project in projects:
            print(project)
            df_project = all_projects[all_projects['Hearing order'] == project].copy()
            df_project.set_index('DataID', inplace=True)
            df_project['Text'] = None
            df_project['Text_rotated'] = None

            for index, row in df_project.iterrows():
                with open(constants.pickles_path + str(index) + '.pkl', 'rb') as f:  # unrotated pickle
                    data = pickle.load(f)
                with open(constants.pickles_rotated_path + str(index) + '.pkl', 'rb') as f:  # rotated pickle
                    data_rotated = pickle.load(f)
                df_project.loc[index, 'Text'] = data['content']  # save the unrotated text
                df_project.loc[index, 'Text_rotated'] = data_rotated['content']  # save the rotated text
            df_project.to_csv(constants.save_dir + 'project_' + project + '.csv', index=True, encoding='utf-8-sig')

    # now get TOC from each document and create a list of all figs and tables (that were found in TOC's)
    if get_toc:
        print('Searching for TOC tables and figures')
        list_figs = []
        list_tables = []
        for index, row in all_projects.iterrows():
            project = row['short_name']
            hearing = row['hearingOrder']
            doc_id = row['pdfId']
            # print(doc_id)
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
                text = re.sub(constants.empty_line, '', page.text)  # get rid of empty lines

                # extrat TOC for figures
                figures = re.findall(constants.figure, text)
                if len(figures) > 0:
                    df_figs = pd.DataFrame(figures, columns=['Name', 'Page'])
                    df_figs['Name'] = df_figs['Name'].str.replace(constants.whitespace, ' ', regex=True).str.strip()
                    df_figs['Page'] = df_figs['Page'].str.strip()
                    df_figs['TOC_Page'] = page_num
                    df_figs['DataID'] = doc_id
                    df_figs['Project'] = project
                    df_figs['Hearing_Order'] = hearing
                    list_figs.append(df_figs)

                # extract TOC for Tables
                tables = re.findall(constants.table, text)
                if len(tables) > 0:
                    df_tables = pd.DataFrame(tables, columns=['Name', 'Page'])
                    df_tables['Name'] = df_tables['Name'].str.replace(constants.whitespace, ' ', regex=True).str.strip()
                    df_tables['Page'] = df_tables['Page'].str.strip()
                    df_tables['TOC_Page'] = page_num
                    df_tables['DataID'] = doc_id
                    df_tables['Project'] = project
                    df_tables['Hearing_Order'] = hearing
                    list_tables.append(df_tables)

        if len(list_figs) > 0:
            df_figs = pd.concat(list_figs, axis=0, ignore_index=True)
            df_figs.to_csv(constants.save_dir + 'all_figs.csv', index=False, encoding='utf-8-sig')
        else:
            print('No figures found!')
        if len(list_tables) > 0:
            df_tables = pd.concat(list_tables, axis=0, ignore_index=True)
            df_tables.to_csv(constants.save_dir + 'all_tables.csv', index=False, encoding='utf-8-sig')
        else:
            print('No tables found!')

    # get page numbers for all the figures found in TOC
    if get_figure_titles:
        # get all fig titles
        df_figs = pd.read_csv(constants.save_dir + 'all_figs.csv', encoding='utf-8-sig')
        df_figs['location_DataID'] = None
        df_figs['location_Page'] = None
        df_figs['count'] = 0

        prev_id = 0
        for index, row in df_figs.iterrows():
            # for i in range(1665, 1700):
            t1 = time.time()
            # index = i
            # row = df_figs.iloc[index, :]
            project = row['Project']
            project_ids = all_projects[all_projects['short_name'] == project]['pdfId'].tolist()
            title = row['Name']
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
            s2 = re.sub(constants.punctuation, '.*', s2) # allow anything in place of punctuation
            s2_rex = r'(?i)\b'
            for s in s2.split(' '):
                s2_rex = s2_rex + r'[^\w]*' + s
            s2_rex = s2_rex + r'\b'
            s2_rex = re.compile(s2_rex)
            toc_id = row['DataID']
            toc_page = row['TOC_Page']

            #print(toc_id, ':', title)
            #print(word1_rex, word2_rex)
            #print(s2_rex)
            id_list = []
            page_list = []
            count = 0


            if toc_id != 2967773:
                # do this for the list of docs to check, list of all docs in this project
                # first check previous and toc id's
                docs_check = [prev_id, toc_id]
                docs_check.extend(project_ids)
                for doc_id in docs_check:
                    if (doc_id > 0) and (doc_id != 2967773):
                        # print(doc_id)
                        arg = (doc_id, toc_id, toc_page, word1_rex, word2_rex, s2_rex)
                        success, output, p_list, doc_id = figure_checker(arg)
                        if not success:
                            print(output)
                        if len(p_list) > 0:
                            id_list.append(doc_id)
                            page_list.extend(p_list)
                            count += len(p_list)
                            break

                # if not found check all docs
                # if len(id_list) == 0:
                #     docs_check = project_ids
                #     args = []
                #     for doc_id in docs_check:
                #         if (doc_id != toc_id) and (doc_id != prev_id):
                #             args.append((doc_id, toc_id, toc_page, word1_rex, word2_rex, s2_rex))
                #     with Pool() as pool:
                #         results = pool.map(figure_checker, args)
                #
                #     # Phase 3. Processing of results
                #     for result in results:
                #         success, output, p_list, doc_id = result
                #         if not success:
                #             print(output)
                #         if len(p_list) > 0:
                #             id_list.append(doc_id)
                #             page_list.extend(p_list)
                #             count += len(p_list)

            if len(id_list) == 1:
                prev_id = id_list[0]

            df_figs.loc[index, 'location_DataID'] = str(id_list).replace('[', '').replace(']', '').strip()
            df_figs.loc[index, 'location_Page'] = str(page_list).replace('[', '').replace(']', '').strip()
            df_figs.loc[index, 'count'] = count
            print(index, time.time() - t1)
        df_figs.to_csv(constants.save_dir + 'final_figs.csv', index=False, encoding='utf-8-sig')

        # unpivot the page numbers
        data = []
        for index, row in df_figs.iterrows():
            if row['count'] <= 1:
                data.append(row)
            else:
                for page in row['location_Page'].split(', '):
                    new_row = row.copy()
                    new_row['location_Page'] = page
                    data.append(new_row)
        df_pivoted = pd.DataFrame(data)
        df_pivoted.to_csv(constants.save_dir + 'final_figs_pivoted.csv', index=False, encoding='utf-8-sig')


    # get page numbers for all the figures found in TOC
    if False:
        # reset projects to what we need
        projects = ['OH-002-2016']

        for project in projects:
            get_titles_figures(project)

        # put everything together
        data = []
        projects = all_projects['hearingOrder'].unique()
        for project in projects:
            df = pd.read_csv(constants.save_dir + project + '-final_figs.csv', encoding='utf-8-sig')
            data.append(df)
        df_all = pd.concat(data, axis=0, ignore_index=True)
        df_all.to_csv(constants.save_dir + 'final_figs.csv', index=False, encoding='utf-8-sig')

        # unpivot the page numbers
        data = []
        for index, row in df_all.iterrows():
            if row['count'] <= 1:
                data.append(row)
            else:
                for page in row['location_Page'].split(', '):
                    new_row = row.copy()
                    new_row['location_Page'] = page
                    data.append(new_row)

        df_pivoted = pd.DataFrame(data)
        df_pivoted.to_csv(constants.save_dir + 'final_figs_pivoted.csv', index=False, encoding='utf-8-sig')

    # get page numbers for all the figures found in TOC
    if get_table_titles:
        # reset projects to what we need
        projects = ['OH-002-2016']

        # put them all together
        for project in projects:
            get_titles_tables(project)
        data = []
        projects = all_projects['Hearing order'].unique()
        for project in projects:
            df = pd.read_csv(constants.save_dir + project + '-final_tables.csv', encoding='utf-8-sig')
            data.append(df)
        df_all = pd.concat(data, axis=0, ignore_index=True)
        df_all.to_csv(constants.save_dir + 'final_tables.csv', index=False, encoding='utf-8-sig')

    # put it all together
    with engine.connect() as conn:
        stmt = text("SELECT csvFullPath, pdfId, page, tableNumber FROM esa.csvs "
                    "WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78);")
        df = pd.read_sql_query(stmt, conn)
    list_ids = df['pdfId'].unique()
    df.to_csv(constants.save_dir + 'all_tables_list.csv', index=False, encoding='utf-8-sig')

    # update tag method titles
    if do_tag_title:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_tag_title, list_ids)
        with open('tag_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open('tag_errors.txt', 'a', encoding='utf-8') as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))

    # update TOC method titles
    if do_toc_title:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_toc_title, list_ids)
        with open('toc_errors.txt', 'w', encoding='utf-8') as f:
            f.write('Errors found:\n')
        with open("toc_errors.txt", "a", encoding='utf-8') as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    # update final titles
    if do_final_title:
        #print(len(list_ids))
        with Pool() as pool:
            results = pool.map(find_final_title, list_ids)
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
