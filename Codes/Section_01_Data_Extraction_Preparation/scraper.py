# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:51:46 2020

@author: singvibu
"""

import requests
import os
import pandas as pd


def file_scraper(path, Index0):
    """
    This method attempts to download all the PDF files from the list of PDF 
    URLs that are sent to the function.
    
    It is assumed that the list of PDFs sent to the function are relevant to 
    Environmental and Social Assessment. The files in this list are then 
    downloaded and saved in the PDFs folder which will be read and processed 
    later.
    
    Parameters
    ----------
    path: path of the root folder in string format
        This path will be used to find the folder location where the scraped 
        pdf files are going to be saved
    Index0: Dataframe with the DataIDs of the PDF and their downloadable links    
        Data_ID: It is the unique ID of the PDF file which will be used as the 
        name of the PDF downloaded
        esa_download_link: URL addresses stored as a list of string
        a list of the pdf URLs so that the respepctive files could be 
        downloaded
        
    Returns
    ----------
    PDF Files:
        The PDF files are scrapped from the URLs and then saved in the PDF 
        folder
    ScrapingErrorLogs.csv:
        In case there are PDF files which were not scraped from the given URLs
        then we are saving the error logs for those files in this CSV file.
        
    
    References 
    ----------
    Ref -> https://requests.readthedocs.io/en/master/user/quickstart/
        
    """
    count = 0
    error_urls = []
    error_dataIDs = []
    dataID = ""
    
    # Iterating each row in the Index0 dataframe
    for index, row in Index0.iterrows():
        try:
            dataID = row['Data ID']
            download_url = 'http://docs2.cer-rec.gc.ca/ll-eng/llisapi.dll?func=ll&objId=' + str(dataID) + '&objaction=download&viewType=1'
            r = requests.get(download_url)  # scraping the PDF file from the URL
            full_name = os.path.join(path + '\\Data_Files\\PDFs\\', (str(dataID) + '.pdf'))
            with open(full_name, 'wb') as file:
                file.write(r.content) 
            count = count + 1
        except:
            # storing the error logs 
            error_urls.append(download_url)
            error_dataIDs.append(dataID)
            print("error with file {}".format(row['File Name']))

    # creating and and saving the error logs dataframe
    df_scraping_errorlog = pd.DataFrame({'error_dataIDs': error_dataIDs,
                                         'error_urls': error_urls
                                         })
    df_scraping_errorlog.to_csv(path + '\\Error_Logs\\ScrapingErrorLogs.csv', index=False, encoding='utf-8-sig')
    return count
