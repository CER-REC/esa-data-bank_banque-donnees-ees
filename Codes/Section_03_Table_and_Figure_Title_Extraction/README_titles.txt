1) Get a list of unique project names and all pdf IDs . These lists are required in later analysis. This data is retrieved form 
the database, table esa.pdfs.

2) Get all Table of Contents: go through all the pdfs (list from #1), identify table of comtents entries using regex expressions, 
   and save these Table of Contents entries to a list of all extracted TOC titles.

3) Assign TOC table titles to tables (tables are represented by a csv and all are listed in csvs table in the database).
   For each table title found in TOC (in step #2), find that table (title) in the documents. Regex expressions and fuzzy match are used
   to find the titles. First we check the document where previous table title was found (as TOC was read and saved in order),
   then check the document the the TOC appears in (often TOC and tables are in same document, but sometimes a document may be split over
   several pdfs and thus have several IDs). If the table is still not found, check the rest of the pdfs that belong to this project 
   (same project as the document with TOC).

4) Assign TOC figure titles to figures (figures are represented by blocks in the "blocks" table in the database).
   For each figure title found in TOC (in step #2), find that figure (title) in the documents. Regex expressions and fuzzy match are used
   to find the titles. First we check the document where previous figure title was found (as TOC was read and saved in order),
   then check the document the the TOC appears in (often TOC and figures are in same document, but sometimes a document may be split over
   several pdfs and thus have several IDs). If the figure is still not found, check the rest of the pdfs that belong to this project 
   (same project as the document with TOC).

5) Get all tables (csvs) from the database that should have a title (are not empty and have more then 1 columns and whitespace is more than 78%)
   Assign Tag titles to these tables. Go for each table, get the text for the page where that table is located, and using regex try to find a table title
   on that page. This is the "Tag Title"

6) Get all images (blocks) from the database. Determine which are deemed to be a figure (the area of the image to page is higher than 10% or 
   average image proportion for the entire document, whichever is lower). Try to assign Tag titles to these images/figures by reading the text for 
   that page (where the image is located), and using regex try to find a figure title on that page. This is the "Tag Title".

7) Combine the TOC title and Tag title for tables in the following way: If Tag title exists, take the Tag title, otherwise take the TOC title as Fina Title.
   Now go through the Final titles, and if a title contains "continued" or "cont'd", or "cont", replace it with the titles from the table on previous page.

8)  Combine the TOC title and Tag title for figures in the following way: If TOC title exists, take that TOC title, otherwise take Tag title.

9) Now the database contains all the Final titles for figures and tables. The dashboard can read from the database, selecting only those 
   items that contain a none-NULL title.

