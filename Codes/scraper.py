# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:51:46 2020

@author: singvibu
"""

def beautiful_soup_scraper(path, download_links, files = 10):
    """
    This method attempts to download all the PDF files from the list of PDF 
    URLs that are sent to the function.
    
    It is assumesed that the list of PDFs sent to the function are relevant to 
    Environmental and Social Assessment. The files in this list are then 
    downloaded and saved in the PDFs folder which will be read and processed 
    later.
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved    
    download links: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
        
    Returns
    ----------
    PDF Files:
        The PDF files are scrapped from the URLs and then saved in the PDF 
        folder
    Error List:
        In case theer are PDF files which were not scraped from the given URLs
        due to any reason then we shoudl have a text file which contains the 
        list of these error files. 
        
    """
    print(path)
    count = 0
    for link in download_links:
        count = count + 1
    print(count)
    print(files)
    return(count)
        
        
    
