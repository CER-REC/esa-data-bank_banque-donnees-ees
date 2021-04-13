# Table Extraction

## Overview

The table extraction process utilizes a MySQL Database to store the results of the extraction process. The steps of the process:
1. Create the DB (e.g. with MySQL Workbench) to store data in.
2. Create two tables in it:
    * `pdfs` for storing information about the CSVs
    * `csvs` for storing information about extracted csvs

3. Populate the `pdfs` table with the following data from the Index file that was created at the end of Data_Extraction_Preparation.ipynb (5. Extracting PDF Metadata) in Section_01_Data_Extraction_Preparation:
    * `pdfId` is the ID of the PDF file in REGDOCS (the last portion of the downloading link of a PDF in REGDOCS, for example for this file https://apps.cer-rec.gc.ca/REGDOCS/File/Download/3914250 pdfId is 3914250)
    * `totalPages` is the number of pages in the PDF
    * `csvsExtracted` is the indication whether all pages of the PDF were processed and all the tables were extracted from it (NULL - not processed, "true" - processed)
    * `hearingOrder`, `application_name`, `application_title_short`, `title_short`, and `commodity` are metadata taken from the input Index file regarding the hearing order number, application name, etc.

4. Run the scripts in this order:
    * `DB.sql` creates some of the tables in the database
    * `pdfs_db_seeding.py` populates `pdfs` table
    * `pages_and_blocks_db_seeding.py` populates `pages` and `blocks` tables
    * `extracting_pages_content.py` populates a series of pages tables with pdf content
    * `extracting_tables.py` populates `csvs` table

## Setting up the DB

1. Download and install the open source MySQL Community Edition for your platform from the official website: https://dev.mysql.com/downloads/.

2. Download and install the Python MySQL connector - https://dev.mysql.com/downloads/connector/python/. This is used by the Python code to connect to the DB.

3. Download and install MySQL Workbench https://dev.mysql.com/downloads/connector/python/ that will be used to create the DB structure. If MySQL Workbench does not start, please see this discussion on how to make it work https://stackoverflow.com/a/18676633/9805867
