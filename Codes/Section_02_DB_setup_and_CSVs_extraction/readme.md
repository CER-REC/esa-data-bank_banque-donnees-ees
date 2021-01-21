# Table Extraction and DB Population

## Rationale

The table extraction is a very CPU-intensive task and can take a long time to complete.
The initial approach regarding table extraction was to attempt table extraction only for those pages where the tables are suspected to be present.


However, since the tables detection methodology was constantly changed, the expensive table extraction code was ran over and over again. Therefore, the decision was made to extract tables from every page of every PDF while preserving the extraction metadata of every extraction yielded by the Camelot (amount of whitespace, accuracy, etc.).

Then, based on the information from the previous steps about the title and location of every table, the extracted CSVs are assigned titles in the DB.

## Overview

The table extraction process utilizes a MySQL Database to store the results of the extraction process. The steps of the process:
1. Create the DB to store data in.
2. Create two tables in it:

    * `pdfs` for storing information about the CSVs
    * `csvs` for storing information about extracted csvs

3. Populate the `pdfs` table with the following data from the Index file:
    * `pdfId` is the ID of the PDF file in REGDOCS (the last portion of the downloading link of a PDF in REGDOCS, for example for this file https://apps.cer-rec.gc.ca/REGDOCS/File/Download/3914250 pdfId is 3914250)
    * `totalPages` is the number of pages in the PDF
    * `csvsExtracted` is the indication whether all pages of the PDF were processed and all the tables were extracted from it (NULL - not processed, "true" - processed)
    * `hearingOrder`, `application_name`, `application_title_short`, `title_short`, and `commodity` are metadata taken from the input Index file regarding the hearing order number, application name, etc.

4. Run t ~TO DO: Fix sentence~

## Setting up the DB

0. If you feel comfortable installing and configuring the DB, you can skip this section.

1. Download and install the free and open source MySQL Community Edition for your platform from the official website: https://dev.mysql.com/downloads/. This is the DB engine that will run on your machine and hold the actual data.
* Write down the password for root user that you created

2. Download and install the Python MySQL connector - https://dev.mysql.com/downloads/connector/python/. This is used by the Python code to connect to the DB.


3. Download and install MySQL Workbench https://dev.mysql.com/downloads/connector/python/ that will be used to create the DB structure. If MySQL Workbench does not start, please see this discussion on how to make it work https://stackoverflow.com/a/18676633/9805867

### Recreating the DB structure

1. Open the MySQL Workbench and connect to the local MySQL DB
2. In the Navigator window, select 'Schemas' tab on the bottom
3. Right click in the free space in the list of ~TO DO: Fix sentence~
