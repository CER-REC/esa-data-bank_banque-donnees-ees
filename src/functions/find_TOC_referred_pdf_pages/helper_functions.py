import re
import pandas as pd
from fuzzywuzzy import fuzz
import regex


from src.util.database_connection import schema, engine
from src.functions.extract_TOCs.main import TOCType
from src.util.process_text import clean_text_content
from src.functions.find_TOC_referred_pdf_pages.compose_regex_pattern import compose_word_regex
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def _get_pdf_page_text(pdf_id, toc_pdf_page_id, toc_type):
    """
    Given PdfId, TOCPdfPageId and TOC Type, return the page text and rotated page text on the pdf pages where TOC items
    of the input type are found, exclude the pdf page where the TOC item is found. The returned data type is Pandas
    dataframe
    """
    # Get the database table name based on TOC type
    with ExceptionHandler("Wrong TOC type input"):
        if toc_type not in (TOCType.TABLE.value, TOCType.FIGURE.value):
            raise ValueError("Wrong TOC type input")
    table_name = "TableElement" if toc_type == TOCType.TABLE.value else "Figure"
    with ExceptionHandler(f"Error querying RawText and RawTextRotated90 for pdf pages of {table_name}"), \
            engine.begin() as conn:
        return pd.read_sql(f'''
            SELECT DISTINCT p.PdfPageId, p.RawText, p.RawTextRotated90
            FROM {schema}.{table_name} t 
                INNER JOIN {schema}.PdfPage p ON t.PdfPageId = p.PdfPageId 
                    AND p.PdfId = {pdf_id}
                    AND p.PdfPageId != {toc_pdf_page_id}; 
        ''', con=conn)


def find_toc_referred_pdf_pages_table(pdf_id, toc_pdf_page_id, content_type_regex, content_num_regex,
                                      content_title_regex):
    """
    This function is to find a list of pages a Table TOC item might be referring to, given the PdfId of which the pages
    will be scanned, the PdfPageId of the Table TOC item, and regex patterns of TOC type, number and title.
    """
    df_pdf_page_text = _get_pdf_page_text(pdf_id, toc_pdf_page_id, TOCType.TABLE.value)
    pdf_page_id_list = []
    for _, row_page in df_pdf_page_text.iterrows():
        # iterate the pages (excluding the page of TOC)
        # if the page text or the rotated page text contains matching regex patterns, add the pdf page id to
        # the list
        clean_page_text = clean_text_content(row_page["RawText"], extra_whitespace=True, replace_punctuation=True)
        clean_page_rotated90_text = clean_text_content(row_page["RawTextRotated90"], extra_whitespace=True,
                                                       replace_punctuation=True)
        is_type_matched = re.search(content_type_regex, clean_page_text) \
                          or re.search(content_type_regex, clean_page_rotated90_text)
        is_num_matched = re.search(content_num_regex, clean_page_text)\
                         or re.search(content_num_regex, clean_page_rotated90_text)
        is_title_matched = re.search(content_title_regex, clean_page_text)\
                           or re.search(content_title_regex, clean_page_rotated90_text)
        if is_type_matched and is_num_matched and is_title_matched:
            pdf_page_id_list.append(row_page["PdfPageId"])
    return pdf_page_id_list


def _calculate_fuzzy_match_ratio(title, page_text):
    """ Given the TOC title and the page text, calculate a ratio based on fuzzy matching """
    n_title = len(title)
    max_ratio = 0
    for i in range(len(page_text) - n_title + 1):
        curr_ratio = fuzz.ratio(title, page_text[i: i + n_title])
        max_ratio = max(curr_ratio, max_ratio)
        if max_ratio == 100:
            return max_ratio
    return max_ratio


def _calculate_word_match_ratio(title, page_text, rotated_page_text):
    """ Given the TOC title and the page text, calculate a ratio based on word matching """
    title_words = [word for word in title.split() if len(word) > 3 and word.lower() != "project"]
    matched_words = [word for word in title_words if regex.search(compose_word_regex(word), page_text) or
                     regex.search(compose_word_regex(word), rotated_page_text)]
    return len(matched_words) / len(title_words) if title_words else 0


def find_toc_referred_pdf_pages_figure(pdf_id, toc_pdf_page_id, content_num_regex, title):
    """
    This function is to find a list of pages a Figure TOC item might be referring to, given the PdfId of which the pages
    will be scanned, the PdfPageId of the Figure TOC item, the regex patterns of TOC number, and the TOC title text
    """
    df_pdf_page_text = _get_pdf_page_text(pdf_id, toc_pdf_page_id, TOCType.FIGURE.value)
    pdf_page_ratios_list = []   # store a list of tuples - (PdfPageId, word match ratio, fuzzy match ratio)
    for _, row_page in df_pdf_page_text.iterrows():
        # iterate the pages (excluding the page of TOC)
        # calculate text matching ratios using word match and fuzzy match, and append the values to the list
        clean_page_text = clean_text_content(row_page["RawText"], extra_whitespace=True, replace_punctuation=True)
        clean_page_rotated90_text = clean_text_content(row_page["RawTextRotated90"], extra_whitespace=True,
                                                       replace_punctuation=True)

        if re.search(content_num_regex, clean_page_text) or re.search(content_num_regex, clean_page_rotated90_text):
            word_match_ratio = _calculate_word_match_ratio(title, clean_page_text, clean_page_rotated90_text)

            if word_match_ratio > 0.7:
                fuzzy_match_ratio = max(_calculate_fuzzy_match_ratio(title, clean_page_text),
                                        _calculate_fuzzy_match_ratio(title, clean_page_rotated90_text))
                if fuzzy_match_ratio >= 60:
                    pdf_page_ratios_list.append((row_page["PdfPageId"], word_match_ratio, fuzzy_match_ratio))

    if pdf_page_ratios_list:
        # if word_match_ratio has the max value and the fuzzy match ratio has the max value amongst, then include the
        # PdfPageId in the final list
        max_word_match_ratio = max(ratio for _, ratio, _ in pdf_page_ratios_list)
        max_fuzzy_match_ratio = max(ratio2 for _, ratio1, ratio2 in pdf_page_ratios_list
                                    if ratio1 == max_word_match_ratio)
        return [page_id for page_id, _, ratio in pdf_page_ratios_list if ratio == max_fuzzy_match_ratio]
    return []
