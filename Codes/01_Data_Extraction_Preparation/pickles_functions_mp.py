# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:44:41 2020

@author: T1Sousan
"""
from tika import parser
import pickle


##create the argument
def get_argument(list_of_files, path):
    """
    This basic function attempts to create the an arrar or array of file 
    name and path for all the PDFs. Thus allowing the xml extraction of for
    the PDF files. 
    
    Parameters
    ----------
    list of files: contains a list of the PDF file names
    path: contains the path of the root directory
    
    Returns
    ----------
    args:
        It returs an array of array with the PDF file name and its complete 
        path. 
        
    """
    args = []
    for pdf_file in list_of_files:
        args.append([pdf_file, path])
    return args


def pickle_pdf_xml(arguments):
    """
    This method attempts to pickle a particular file with xmlContent = True and 
    then it saves the pickled file in the appropritae folder.
    
    The pickle data format uses a relatively compact binary representation, 
    allowing faster processing of the files with a reduced failure rate. 
    
    Parameters
    ----------
    arguments:  this is array of PDF file names and their paths for a particular
                PDF file. 
     argument[0]: contains the name of the PDF file.
     argument[1]: contains the path of the PDF file.
        
    Returns
    ----------
    file:
        This function returns the name of the PDF file in case there is a error
        in pickling process.
        
    """
    file = arguments[0]
    path = arguments[1]
    try:
        xml = parser.from_file(file, xmlContent = True)
        replace_string = file.split('\\')[-1].replace('.pdf', '')
        save_string = path + replace_string + '.pkl'
        print(save_string)
        pickle.dump(xml, open(save_string, "wb"))
    except: 
        return file


