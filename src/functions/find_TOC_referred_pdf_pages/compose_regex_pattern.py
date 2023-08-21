import re
import regex

from src.util.process_text import clean_text_content


def compose_content_type_regex(text):
    """  compose regex pattern for TOC type """
    # (?i): case-insensitive, \b empty string at the beginning, \s unicode whitespace characters.
    return re.compile(r"(?i)\b" + text + r"\s")


def compose_content_num_regex(text):
    """ compose regex pattern for TOC number """
    # remove non-alphanumeric characters at the end of string
    text = re.sub("[^a-zA-Z0-9]$", '', text)
    # replace non-alphanumeric characters with regex pattern string "[^a-zA-Z0-9]"
    text = re.sub("[^a-zA-Z0-9]", "[^a-zA-Z0-9]", text)
    # (?i): case-insensitive, \b empty string at the beginning or the end
    return re.compile(r"(?i)\b" + text + r"\b")


def compose_content_title_regex(text):
    """ compose regex pattern for TOC title """
    text = clean_text_content(text, extra_whitespace=True, replace_punctuation=True)
    # (?i): case-insensitive, \b empty string at the beginning or the end
    # \w: unicode word characters, [^\w]* non-word characters
    return re.compile(r"(?i)\b" + r"[^\w]*".join(text.split(" ")) + r"\b")


def compose_word_regex(text):
    """ compose regex pattern for a word in TOC """
    # (?i): case-insensitive, \b empty string at the beginning or the end
    # {e <= 1}: allow up to one error
    text = regex.sub(r"[\([{})\]]", ".", text)
    return regex.compile(r"(?i)\b" + text + r"{e<=1}\b")
