import pandas as pd
import re
from multiprocessing import Pool
from sqlalchemy import text
import json
from dotenv import load_dotenv

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))

from berdi.Database_Connection_Files.connect_to_sqlserver_database import connect_to_db
from berdi.Section_03_Table_and_Figure_Title_Extraction.external_functions import (
    project_figure_titles,
    find_toc_title_table,
)
from berdi.Section_03_Table_and_Figure_Title_Extraction.external_functions import (
    find_tag_title_table,
    project_table_titles,
    find_final_title_table,
)
from berdi.Section_03_Table_and_Figure_Title_Extraction.external_functions import (
    find_tag_title_fig,
    find_final_title_fig,
)
import berdi.Section_03_Table_and_Figure_Title_Extraction.constants as constants


# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=constants.ROOT_PATH / "berdi/Database_Connection_Files" / ".env",
    override=True,
)
conn = connect_to_db()

get_toc = 1  # need to go through all docs to create lists of tables and figures in csvs
toc_figure_titles = 1  # assign page number to TOC figure titles
toc_table_titles = 1 # assign page number to TOC table titles

do_tag_title_table = 1  # assign table titles to each table using text search method
do_toc_title_table = 1  # assign table titles to each table using TOC method
do_final_title_table = 1  # replace continued tables and create final table title

do_tag_title_fig = 1  # assign figure titles to each figure using text search method
do_toc_title_fig = 1  # assign figure titles to each figure using TOC method
do_final_title_fig = 1  # replace continued figures and create final figure title

create_tables_csv = 0
create_figs_csv = 0

if __name__ == "__main__":
    # get list of all documents, read from pdfs
    with conn:
        stmt = '''SELECT pdfId, hearingOrder, short_name FROM [DS_TEST].[BERDI].pdfs;'''
        all_projects = pd.read_sql_query(stmt, conn)
    projects = all_projects["short_name"].unique()
    list_ids = all_projects["pdfId"].tolist()
    print(all_projects)

    # now get TOC from each document and create a list of all figs and tables (that were found in TOC's)
    if get_toc:
        print("Searching for TOC tables and figures")
        cursor = conn.cursor()
        for index, row in all_projects.iterrows():
            doc_id = row["pdfId"]

            # delete any existing TOC from this document
            stmt = '''DELETE FROM [DS_TEST].[BERDI].toc WHERE toc_pdfId = ?;'''
            params = [doc_id]
            result = cursor.execute(stmt, params)
            cursor.commit()

            # get text of this document
            params = [doc_id]
            stmt = '''SELECT page_num, content FROM [DS_TEST].[BERDI].pages_normal_txt
                WHERE (pdfId = ?);'''
            text_df = pd.read_sql_query(stmt, conn, params=params, index_col="page_num")

            # stmt_rotated = text("SELECT page_num, content FROM pages_rotated90_txt "
            #                     "WHERE (pdfId = :pdf_id);")
            # text_rotated_df = pd.read_sql_query(stmt_rotated, conn, params=params, index_col='page_num')

            for page_num, row in text_df.iterrows():
                # extract TOC
                clean_text = re.sub(
                    constants.empty_line, "", row["content"]
                )  # get rid of empty lines
                tocs = re.findall(constants.toc, clean_text)

                for i, toc in enumerate(tocs):
                    title = re.sub(constants.whitespace, " ", toc[0]).strip()
                    page_name = toc[1].strip()
                    type = title.split(" ", 1)[0].capitalize()
                    if type in constants.accepted_toc:  # if accepted type
                        stmt = '''INSERT INTO [DS_TEST].[BERDI].toc (assigned_count, title_type, titleTOC, page_name,
                            toc_page_num, toc_pdfId, toc_title_order)
                            VALUES (null, ?,?,?,?,?,?);'''
                        params = [type, title, page_name, page_num, doc_id, i+1]
                        result = cursor.execute(stmt, params)
                        if result.rowcount != 1:
                            print("Did not go to database:", doc_id, page_num, toc)
                        cursor.commit()
        conn.close()

    # get page numbers for all the figures found in TOC
    if toc_figure_titles:
        for project in projects:
            project_figure_titles(project)
        with Pool() as pool:
            results = pool.map(project_figure_titles, projects, chunksize=1)
        with open("fig_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("fig_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))

    # update tag method titles
    if do_tag_title_table:
        # for list_id in list_ids:
        #     find_tag_title_table(list_id)
        with Pool() as pool:
            results = pool.map(find_tag_title_table, list_ids, chunksize=1)
        with open("tag_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("tag_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))

    # update TOC method titles
    if toc_table_titles:
        print("Start assigning pages to TOC entries")
        # for project in projects:
        #     project_table_titles(project)
        with Pool() as pool:
            results = pool.map(project_table_titles, projects, chunksize=1)
        with open("toc_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("toc_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1]:
                    f.write(result[1])
        print("Finish")

    if do_toc_title_table:
        print("Start assigning toc titles to csvs")
        # for list_id in list_ids:
        #     find_toc_title_table(list_id)
        with Pool() as pool:
            results = pool.map(find_toc_title_table, list_ids, chunksize=1)
        with open("toc2_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("toc2_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1]:
                    f.write(result[1])
        print("Finish")

    # update final titles
    if do_final_title_table:
        # for list_id in list_ids:
        #     find_final_title_table(list_id)
        with Pool() as pool:
            results = pool.map(find_final_title_table, list_ids, chunksize=1)
        with open("final_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("final_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    if do_tag_title_fig:
        # for list_id in list_ids:
        #     find_tag_title_fig(list_id)
        with Pool() as pool:
            results = pool.map(find_tag_title_fig, list_ids, chunksize=1)
        with open("../tag_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("../tag_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1] != "":
                    f.write(str(result[1]))

    if do_final_title_fig:
        # for list_id in list_ids:
        #     find_final_title_fig(list_id)
        with Pool() as pool:
            results = pool.map(find_final_title_fig, list_ids, chunksize=1)
        with open("final_errors.txt", "w", encoding="utf-8") as f:
            f.write("Errors found:\n")
        with open("final_errors.txt", "a", encoding="utf-8") as f:
            for result in results:
                if result[1]:
                    f.write(result[1])

    if create_tables_csv:
        # write to all_tables-final.csv from csvs
        with conn:
            stmt = '''SELECT csvFullPath, pdfId, page, tableNumber, topRowJson, titleTag, titleTOC, titleFinal FROM [DS_TEST].[BERDI].csvs 
                WHERE (hasContent = 1) and (csvColumns > 1) and (whitespace < 78);'''
            df = pd.read_sql_query(stmt, conn)
        df.to_csv(
            constants.save_dir + "all_tables-final.csv",
            index=False,
            encoding="utf-8-sig",
        )
        # df.to_csv('Data_Files/all_tables-final.csv', index=False, encoding='utf-8-sig')

    if create_figs_csv:
        # get final figs csv files
        with conn:
            stmt = '''SELECT toc.titleTOC, toc.page_name, toc.toc_page_num, toc.toc_pdfId, toc.toc_title_order, toc.loc_pdfId, toc.loc_page_list, pdfs.short_name
                FROM [DS_TEST].[BERDI].toc LEFT JOIN [DS_TEST].[BERDI].pdfs ON toc.toc_pdfId = pdfs.pdfId WHERE title_type='Figure'
                ORDER BY pdfs.short_name, toc.toc_pdfId, toc.toc_page_num, toc.toc_title_order;'''
            df = pd.read_sql_query(stmt, conn)

        new_list = []

        df["loc_page"] = None
        df["sim"] = None
        df["ratio"] = None
        for index, row in df.iterrows():
            p = row["loc_page_list"]
            if p:
                pages = json.loads(p)
                df.loc[index, "loc_page"] = pages[0]["page_num"]
                df.loc[index, "sim"] = pages[0]["sim"]
                df.loc[index, "ratio"] = pages[0]["ratio"]

                for page in pages:
                    new_row = {
                        "Name": row["titleTOC"],  # 'Name_French': row['Name_French'],
                        "page_name": row["page_name"],
                        "toc_page_num": row["toc_page_num"],
                        "toc_pdfId": row["toc_pdfId"],
                        "toc_title_order": row["toc_title_order"],
                        "short_name": row["short_name"],
                        "loc_pdfId": row["loc_pdfId"],
                        # 'assigned_count': row['assigned_count'],
                        # 'loc_page_list': row['loc_page_list'],
                        "sim": page["sim"],
                        "ratio": page["ratio"],
                        "page_num": page["page_num"],
                    }
                    new_list.append(new_row)
            else:
                new_list.append(row)
        df_pivoted = pd.DataFrame(new_list)

        # df.to_csv('Data_Files/final_figs_new.csv', index=False, encoding='utf-8-sig')
        # df_pivoted.to_csv('Data_Files/final_figs_pivoted_new.csv', index=False, encoding='utf-8-sig')

        # df.to_csv(constants.save_dir + 'final_figs_new.csv', index=False, encoding='utf-8-sig')
        df_pivoted.to_csv(
            constants.save_dir + "final_figs_pivoted_new.csv",
            index=False,
            encoding="utf-8-sig",
        )
