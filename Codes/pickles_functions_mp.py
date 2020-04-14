# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 09:44:41 2020

@author: T1Sousan
"""

from tika import parser
import pickle

def get_pickeles(argument_list):
# print(subset_list_pdf_full[0:5])
    subset_list_pdf_full = argument_list[0]
    for x in subset_list_pdf_full:
        xml = parser.from_file(x, xmlContent = True)
        replace_string = x.replace('F:/Environmental Baseline Data/Version 4 - Final/PDF/', '').replace('.pdf', '')
        path = 'F:/Environmental Baseline Data/Version 4 - Final/Pickles/'
        save_string = path + replace_string + '.pkl'
        print(save_string)
        pickle.dump(xml, open(save_string, "wb" ))
    return True


def get_pickles_(x):
# print(subset_list_pdf_full[0:5])
    xml = parser.from_file(x, xmlContent = True)
    replace_string = x.replace('F:/Environmental Baseline Data/Version 4 - Final/PDF/', '').replace('.pdf', '')
    path = 'F:/Environmental Baseline Data/Version 4 - Final/Pickles/'
    save_string = path + replace_string + '.pkl'
    print(save_string)
    pickle.dump(xml, open(save_string, "wb" ))
    return True


