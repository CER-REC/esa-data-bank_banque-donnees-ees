# Table Extraction and DB Population

## Rationale

The table extraction is a very CPU-intensive task and can take a long time to complete.
The initial approach regarding table extraction (with the python package Camelot) was to attempt table extraction only for those pages where the tables are suspected to be present.

However, since the tables detection methodology was constantly changed, the expensive table extraction code was ran over and over again. Therefore, the decision was made to extract tables from every page of every PDF while preserving the extraction metadata of every extraction yielded by the Camelot (amount of whitespace, accuracy, etc.).

Then, based on the information from the previous steps about the title and location of every table, the extracted CSVs are assigned titles in the DB. The extraction metadata from Camelot allowed us to to see which tables were poorly extracted (lots of whitespace or low accuracy score) and remove what was extracted by Camelot which wasn't actually a table (e.g. GIS figures will sometimes be mistaken for a table).

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

0. If you feel comfortable installing and configuring the DB, you can skip this section.

1. Download and install the free and open source MySQL Community Edition for your platform from the official website: https://dev.mysql.com/downloads/. This is the DB engine that will run on your machine and hold the actual data.
Write down the password for root user that you created.

2. Download and install the Python MySQL connector - https://dev.mysql.com/downloads/connector/python/. This is used by the Python code to connect to the DB.

3. Download and install MySQL Workbench https://dev.mysql.com/downloads/connector/python/ that will be used to create the DB structure. If MySQL Workbench does not start, please see this discussion on how to make it work https://stackoverflow.com/a/18676633/9805867
