# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 08:58:13 2020

@author: singvibu
"""
import PyPDF2
import pandas as pd

def rotate_pdf(path, Index0):
    """
    This method attempts to rotate all the PDF files from the list of PDFs 
    which we have already downloaded.
    
    Some of the ESA pdf files that were submitted to CER were rotated and this 
    hinders the process of component extraction for the PDFs. Hence, we wanted 
    to rotate all the PDFs and save them to the PDFs_Rotated folder so that 
    none of these components are missed out.
    
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
    PDFs_Rotated Files:
        The PDF files are rotated page by page and then they are saved in the 
        PDFs_Rotated folder.
    RotatingErrorLogs.csv:
        In case there are PDF files which were not rotated successfully then we 
        are saving the error logs for those files in this CSV file. 
        
    
    References 
    ----------
    Ref -> https://pythonhosted.org/PyPDF2/PdfFileReader.html
    Ref -> https://stackoverflow.com/questions/42615771/how-can-i-rotate-a-page-in-pypdf2
        
    """
    count = 0
    error_urls = []
    error_dataIDs = []
    dataID = ""
    
    # Itterating each row in the Index0 dataframe  
    for index, row in Index0.iterrows():
        #print(index)
        #print(row)
        
        try:
            full_path = path + "\\Data_Files\\PDFs\\" + str(row['Data ID']) + ".pdf"
            pdf_in = open(full_path, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_in, strict=False)
            pdf_writer = PyPDF2.PdfFileWriter()
            for pagenum in range(pdf_reader.numPages):
                page = pdf_reader.getPage(pagenum)
                page.rotateClockwise(90)
                pdf_writer.addPage(page)
            pdf_out = open(path + "\\Data_Files\\PDFs_Rotated\\" + str(row['Data ID']) + "_Rotated.pdf", 'wb')
            pdf_writer.write(pdf_out)
            pdf_out.close()
            pdf_in.close()
            count = count + 1

        except:
            # storing the error logs 
            error_urls.append(download_url)
            error_dataIDs.append(dataID)
            print("error with file {}".format(row['File Name']))
            
            
    # creating and and saving the error logs dataframe
    df_rotating_errorlog = pd.DataFrame({'error_dataIDs' : error_dataIDs,
                                         'error_urls' : error_urls
                                      })
    df_rotating_errorlog.to_csv(path + '\\Error_Logs\\RotatingErrorLogs.csv', index = False, encoding='utf-8-sig')
    return(count)    