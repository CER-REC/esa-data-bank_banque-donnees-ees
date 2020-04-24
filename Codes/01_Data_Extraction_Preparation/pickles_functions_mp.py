# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:44:41 2020

@author: T1Sousan
"""
from tika import parser
import pickle


##create the argument
def get_argument(list_of_files, path):
    args = []
    for pdf_file in list_of_files:
        args.append([pdf_file, path])
    return args


def pickle_pdf_xml(arguments):
    file = arguments[0]
    path = arguments[1]
    xml = parser.from_file(file, xmlContent = True)
    replace_string = file.split('\\')[-1].replace('.pdf', '')
    save_string = path + replace_string + '.pkl'
    print(save_string)
    pickle.dump(xml, open(save_string, "wb"))
    return True


