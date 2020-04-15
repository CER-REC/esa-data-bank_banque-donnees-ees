from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import re
from bs4 import BeautifulSoup
import traceback
import pickle

import constants

def table_checker(args):
    doc_text, doc_text_rotated, doc_id, toc_id, toc_page, s1_rex, s2_rex = args
    buf = StringIO()
    p_list = []
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            print("Start.")
            # check unrotated
            if '<body>' in doc_text:
                soup = BeautifulSoup(doc_text, 'lxml')
                pages = soup.find_all('div', attrs={'class': 'page'})
                soup_r = BeautifulSoup(doc_text_rotated, 'lxml')
                pages_r = soup_r.find_all('div', attrs={'class': 'page'})

                for page_num in range(len(pages)):
                    text_clean = re.sub(constants.whitespace, ' ', pages[page_num].text)
                    text_clean_r = re.sub(constants.whitespace, ' ', pages_r[page_num].text)
                    # text_clean = re.sub(punctuation, ' ', text_clean)
                    if (doc_id != toc_id) or (page_num != toc_page):
                        if (re.search(s1_rex, text_clean) and re.search(s2_rex, text_clean)) \
                                or (re.search(s1_rex, text_clean_r) and re.search(s2_rex, text_clean_r)):
                            p_list.append(page_num)

                # check rotated
                soup = BeautifulSoup(doc_text_rotated, 'lxml')
                pages = soup.find_all('div', attrs={'class': 'page'})
                for page_num, page in enumerate(pages):
                    text_clean = re.sub(constants.whitespace, ' ', page.text)
                    # text_clean = re.sub(punctuation, ' ', text_clean)
                    if re.search(s1_rex, text_clean) and re.search(s2_rex, text_clean):
                        if (page_num not in p_list) and ((doc_id != toc_id) or (page_num != toc_page)):
                            p_list.append(page_num)
            print(f"Success. Found data on {len(p_list)} pages.")
            return True, buf.getvalue(), p_list, doc_id
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            return False, buf.getvalue(), p_list, doc_id

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