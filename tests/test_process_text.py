# pylint: disable=missing-function-docstring
from src.util import process_text


def test_1():
    """
        a general test case to check whether the function is working
    """
    input_string = "  a decision from  the Federal     Govt.$  *(    "
    expected_string = "a decision from the federal govt"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           trailing_whitespace=True,
                                           extra_whitespace=True,
                                           special_character=True) == expected_string


def test_2():
    """
        a test case to check whether the function retains email addresses
    """
    input_string = " A CER email address would be surname.firstname@cer-rec.gc.ca "
    expected_string = "a cer email address would be surname.firstname@cer-rec.gc.ca"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           trailing_whitespace=True) == expected_string


def test_3():
    """
        a test case to check whether the function removes emails and special characters
    """
    input_string = " A CER email address would be surname.firstname@cer-rec.gc.ca "
    expected_string = "a cer email address would be"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           trailing_whitespace=True,
                                           email=True,
                                           special_character=True) == expected_string


def test_4():
    """
        a general test case to check whether the function is working
    """
    input_string = "Can you process random sentences?"
    expected_string = "can you process random sentences"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           special_character=True,
                                           trailing_whitespace=True) == expected_string


def test_5():
    """
        a test case to check whether the function retains trailing white spaces when specified
    """
    input_string = " A CER email address would be surname.firstname@cer-rec.gc.ca "
    expected_string = " a cer email address would be "
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           extra_whitespace=True,
                                           email=True) == expected_string


def test_6():
    """
        a test case to check whether the function removes short words
    """
    input_string = " A CER email address would be surname.firstname@cer-rec.gc.ca "
    expected_string = "cer email address would"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           trailing_whitespace=True,
                                           email=True,
                                           short_word=True) == expected_string


def test_7():
    """
        a test case to check whether the function removes english stop words
    """
    input_string = " A CER email address would be surname.firstname@cer-rec.gc.ca "
    expected_string = "cer email address would"
    assert process_text.clean_text_content(input_string,
                                           lower_case=True,
                                           trailing_whitespace=True,
                                           extra_whitespace=True,
                                           email=True,
                                           special_character=True,
                                           stop_word=True) == expected_string
