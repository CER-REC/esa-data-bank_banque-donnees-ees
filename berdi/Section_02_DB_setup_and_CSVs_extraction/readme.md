# Table Extraction

## Overview

The table extraction process utilizes a MSSQL Database to store the results of the extraction process. The setup instructions and SQL scripts for MySQL database has also been provided in case you choose to utilize an open source MySQL Community Edition. The steps of the process are as follows:
1. Create the DB (e.g. with either MSSQL or MySQL Workbench) to store data in
2. Create two tables in it (refer schema in `DB.sql` in case you are using MySQL else use `DB_MSSQL.sql` for MSSQL database):
    * `pdfs` for storing information about the CSVs
    * `csvs` for storing information about extracted csvs

3. Populate the `pdfs` table with the following data from the Index file that was created at the end of Data_Extraction_Preparation.ipynb (5. Extracting PDF Metadata) in Section_01_Data_Extraction_Preparation:
    * `pdfId` is the ID of the PDF file in REGDOCS (the last portion of the downloading link of a PDF in REGDOCS, for example for this file https://apps.cer-rec.gc.ca/REGDOCS/File/Download/3914250 pdfId is 3914250)
    * `totalPages` is the number of pages in the PDF
    * `csvsExtracted` is the indication whether all pages of the PDF were processed and all the tables were extracted from it (NULL - not processed, "true" - processed)
    * `hearingOrder`, `application_name`, `application_title_short`, `title_short`, and `commodity` are metadata taken from the input Index file regarding the hearing order number, application name, etc.

4. Tika configuration for extract text from large PDFs

IMPORTANT: Before running the code in this section, make sure you go through the following steps:

I. The following steps allow you to configure the Tika server to allow extraction of much bigger PDF files. Otherwise, the script will fail when you try to extract bigger files (especially when using multiprocessing).

II. Download: the java runtime (64-bit version) from https://www.java.com/en/download/manual.jsp

III. If you want to update tika version, go to: https://tika.apache.org/download.html

IV. Run: `java -d64 -jar -Xms40g -Xmx40g tika-server-standard-2.1.0.jar`. Adjust the memory (40g in this case) to 2/3rds of RAM you have available. Adjust the tika version to the one you downloaded.

(Optional): if you know how to use docker, spin one of the containers here instead of downloading tika: https://hub.docker.com/r/apache/tika.
Note: the code runs slower on Windows if you use Docker because Windows needs to create a linux virtual environment.

5. Run the scripts in this order:
    * `DB.sql` (for MySQL) or `DB_MSSQL.sql` (for MSSQL) creates some of the tables in the database
    * `pdfs_db_seeding.py` populates `pdfs` table
    * `pages_and_blocks_db_seeding.py` populates `pages` and `blocks` tables
    * `extracting_pages_content.py` populates a `pages_normal_txt` and `pages_rotated90_txt` tables with pdf content
    * `extracting_tables.py` populates `csvs` table

## Setting up the MySQL DB

1. Download and install the open source MySQL Community Edition for your platform from the official website: https://dev.mysql.com/downloads/.

2. Download and install the Python MySQL connector - https://dev.mysql.com/downloads/connector/python/. This is used by the Python code to connect to the DB.

3. Download and install MySQL Workbench https://dev.mysql.com/downloads/connector/python/ that will be used to create the DB structure. If MySQL Workbench does not start, please see this discussion on how to make it work https://stackoverflow.com/a/18676633/9805867
