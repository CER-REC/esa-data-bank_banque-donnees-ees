import re
from enum import Enum

from src.util.process_text import clean_text_content
from src.util.process_text import remove_short_words, remove_extra_whitespaces
from src.util.exception_and_logging.handle_exception import ExceptionHandler


class TitleType(Enum):
    """ Enum for title type """
    TABLE = "Table"
    FIGURE = "Figure"
    ALIGNMENT_SHEET = "AlignmentSheet"


class TitleTextCategory(Enum):
    """ Enum for title text category """
    NON_TITLE_TEXT = 0
    TITLE_CONTENT = 1
    TITLE_PREFIX = 2


class RegexConstant(Enum):
    """ Enum for regex constant """
    TABLES = re.compile(r"^T[aA][bB][lL][eE][sS]?\b")
    FIGURES = re.compile(r".*\bF[iI][gG][uU][rR][eE][sS]?\b")
    PHOTOS = re.compile(r".*\bP[hH][oO][tT][oO][sS]?\b")


def _get_title_category(line_text):
    """
        determine category of TableElement TitleText
    """
    # remove punctuations and extra whitespaces
    text_clean = clean_text_content(line_text, remove_punctuation=True, extra_whitespace=True).strip()

    long_words = remove_short_words(text_clean).split(" ")  # delete any 1 or 2-letter words without digits
    if len(long_words) <= 3:
        # title contains less than or equal to 3 long words
        if "cont" in text_clean.lower():
            # if any word starts with 'cont'
            return TitleTextCategory.TITLE_CONTENT
        return TitleTextCategory.TITLE_PREFIX

    third_title_word = text_clean.split(" ")[2]

    # if the third word in the title
    # (starts with / contains) the word 'cont'
    # or first letter of the third word is a digit
    # or first letter of the third word is an upper case letter
    if third_title_word.lower().startswith("cont") or \
            third_title_word[0].isdigit() or \
            third_title_word[0].isupper():
        return TitleTextCategory.TITLE_CONTENT
    return TitleTextCategory.NON_TITLE_TEXT


def _get_full_title(line_text, next_line_text):
    category = _get_title_category(line_text)
    if category == TitleTextCategory.TITLE_PREFIX:
        return line_text + " " + next_line_text
    if category == TitleTextCategory.TITLE_CONTENT:
        return line_text
    return ""


def _append_title_candidates(titles, text):
    if text and len(text) < 1000:
        # if the text is less than 1000 characters, append to the candidate title list
        titles.append(text)


def extract_titles_from_text(text, title_type):
    """
        This function creates a list containing the candidates
        for the title of the 'TableElement'

        Params:
        ------------------------------
        text (string): raw text content of a page
        title_type (TitleType): the type of title to be extracted

        Returns:
        ------------------------------
        title candidates
    """
    with ExceptionHandler("Unrecognized title_type for function extract_titles_from_text"):
        if title_type not in (type.value for type in TitleType):
            raise ValueError(f"Unrecognized title_type for function extract_titles_from_text: {title_type}")

    lines = text.split("\n\n")
    titles = []
    for index, line in enumerate(lines):
        # replace all whitespace with single space
        line_text = remove_extra_whitespaces(line).strip()

        if title_type == TitleType.TABLE.value and re.match(RegexConstant.TABLES.value, line_text):
            # verify whether this line is a table line
            title_text = _get_full_title(line_text, lines[index + 1].strip() if index < len(lines) - 1 else "")
            _append_title_candidates(titles, title_text)
        elif title_type == TitleType.FIGURE.value and re.match(RegexConstant.FIGURES.value, line_text):
            # verify whether this line is a figure line
            # get the line text starting from "Figure"; for example, extract "Figure 7.1) and this UWR" from
            # "Moberly Rivers (Figure 7.1) and this UWR"
            figure_text = re.search(r"\bF[iI][gG][uU][rR][eE][sS]?.*", line_text).group()
            title_text = _get_full_title(figure_text, lines[index + 1].strip() if index < len(lines) - 1 else "")
            _append_title_candidates(titles, title_text)
        elif title_type == TitleType.ALIGNMENT_SHEET.value \
                and (re.match(RegexConstant.FIGURES.value, line_text)
                     or re.match(RegexConstant.PHOTOS.value, line_text)):
            # verify whether this line is an alignment sheet line
            _append_title_candidates(titles, line_text)

    return titles
