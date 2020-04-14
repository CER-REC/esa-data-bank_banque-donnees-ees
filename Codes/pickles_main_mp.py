# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 08:59:30 2020

@author: T1Sousan
"""

# Libraies
import time
import glob
import multiprocessing
import pickles_functions_mp as pf
# import sys
# sys.path.insert(0, 'H:/GitHub/Extract-Tables-With-Titles')


if __name__ == '__main__':
    # list of full paths to pdfs
    subset_list_pdf_full = ['F:/Environmental Baseline Data/Version 4 - Final/PDF/'
                            + x.split('\\')[-1] for x in glob.glob
                            ('F:/Environmental Baseline Data/Version 4 - Final/PDF/*.pdf')]

    # Directory where the output pickle files are saved
    path = 'H:/GitHub/tmp/'
    # prepare arguments for multiprocessing
    args = pf.get_argument(subset_list_pdf_full, path)

    # timing the process-start
    starttime = time.time()
    
    # sequential
#    for arg in args:
#        try:
#            pf.pickle_pdf_xml(arg)
#        except Exception:
#            pass

    # multiprocessing
    pool = multiprocessing.Pool()
    pool.map(pf.pickle_pdf_xml, args)
    pool.close()
    # time ends and dellta displayed
    print('That took {} seconds'.format(time.time() - starttime))
