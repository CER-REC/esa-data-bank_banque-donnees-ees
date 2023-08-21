import re
import nltk


def replace_emails(text):
    """ replace emails with whitespace """
    rgx = re.compile(r"\S*@\S*\s?")
    return re.sub(rgx, " ", text)


def replace_special_characters(text):
    """ replace non-alphabetic and numeric characters, and latin letters with whitespace """
    rgx = re.compile(r"[^A-Za-z0-9À-ÿ]+")
    return re.sub(rgx, " ", text)


def remove_short_words(text):
    """
        remove short words (length less than 3 characters)

        Params:
        ------------------------------
        text (string): pdf Id number

        Returns:
        ------------------------------
        transformed text
    """
    return " ".join([w for w in text.split() if len(w) > 2])


def remove_stop_words(text):
    """ remove stop words """
    nltk.download("stopwords")
    en_stop = set(nltk.corpus.stopwords.words("english"))
    return " ".join([w for w in text.split() if w not in en_stop])


def remove_empty_lines(text):
    """ remove empty lines"""
    rgx = re.compile(r"^\s*$")
    return re.sub(rgx, "", text)


def remove_extra_whitespaces(text):
    """ reduce multiple continuous whitespace to one whitespace """
    return re.sub(r"\s+", " ", text)


def remove_trailing_whitespaces(text):
    """ remove trailing whitespaces """
    return text.strip()


def replace_punctuation_with_whitespace(text):
    """ replace punctuation marks with whitespaces """
    return re.sub(re.compile(r"[^\w\s]"), " ", text)


def remove_non_word_or_non_whitespace(text):
    """ remove non-words or whitespaces"""
    return re.sub(re.compile(r"[^\w\s]"), "", text)


def replace_long_string(text):
    """ replace long string with whitespace"""
    # \w Matches any alphanumeric character, this is equivalent to the class [a-zA-Z0-9_].
    # {m, n} braces match any repetitions preceding  regex from m to n both inclusive.
    # Thus, \w{25,} will be matched for any string in the text input which has a length of greater than 24 characters
    rgx = re.compile(r"\w{25,}")
    return re.sub(rgx, " ", text)


def replace_cid(text):
    """ replace strings containing 'cid' followed by one or more numbers with whitespace """
    # \d match a digit between [0-9]. \d+ will match one or more digits.
    # For example: cid\d+ will match for strings cid1, cid12, cid123
    rgx = re.compile(r"cid\d+")
    return re.sub(rgx, " ", text)


def clean_text_content(text,
                       lower_case=False,
                       trailing_whitespace=False,
                       extra_whitespace=False,
                       email=False,
                       special_character=False,
                       short_word=False,
                       stop_word=False,
                       empty_line=False,
                       replace_punctuation=False,
                       remove_punctuation=False,
                       long_string=False,
                       cid=False):
    
    """
        This basic function cleans text based on input parameters
    """
    # change to lower cases 
    if lower_case:
        text = text.lower()

    # replace emails with whitespace
    if email:
        text = replace_emails(text)

    # replace special characters with whitespace
    if special_character:
        text = replace_special_characters(text)

    # remove short words
    if short_word:
        text = remove_short_words(text)

    # remove stop words
    if stop_word:
        text = remove_stop_words(text)
    
    # remove empty lines
    if empty_line:
        text = remove_empty_lines(text)

    # replace non-word or non-whitespace with whitespace
    if replace_punctuation:
        text = replace_punctuation_with_whitespace(text)

    # remove non-words or non-whitespaces
    if remove_punctuation:
        text = remove_non_word_or_non_whitespace(text)

    # replace string of more than 24 characters with whitespace
    if long_string:
        text = replace_long_string(text)

    # replace strings containing 'cid' followed by one or more numbers with whitespace
    if cid:
        text = replace_cid(text)

    # reduce any number of white spaces to a single space
    if extra_whitespace:
        text = remove_extra_whitespaces(text)

    # remove trailing whitespaces
    if trailing_whitespace:
        text = remove_trailing_whitespaces(text)
        
    return text
