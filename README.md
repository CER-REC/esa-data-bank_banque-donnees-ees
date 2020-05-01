# The ESA Data Bank
### From the Canada Energy Regulator (CER)

**** _**La version française suit**_ **** 

Environmental and Socio-Economic Assessments (ESAs) can be several hundred pages long and are submitted to the CER as a series of PDF documents. These PDFs contain qualitative and quantitative data, including text, tables, figures, maps and satellite images. 

While the information contained in each ESA is comprehensive, it is not easily searchable or accessible due to the limitations of the PDF format. No raw data files, such as tables in CSV format, are filed with the CER -- all relevant information is contained within the PDF file. Those interested in analysing, comparing, or processing the data must extract it manually, by copying and pasting information from the PDF into other software programs, such as spreadsheet software. This is time-intensive and tedious.

A team of data scientists at the CER created the process for automatically identifying ESA table and figure titles and extracting table data as a CSV. This process uses several open-source libraries in the Python programming language. All code is open source and available on the CER's GitHub repository.

### Step 1: Collect the relevant PDF documents
CER staff manually identified 1,902 ESA PDF documents in [REGDOCS](https://apps.cer-rec.gc.ca/REGDOCS/Home/Index). REGDOCS is the CER's on-line repository of public documents related to the design, construction, operation, and abandonment of federally regulated pipelines. A file that indexes all of these documents is available in our GitHub repository.

### Step 2: Convert PDF documents to text files
Each PDF was converted into a more computer-friendly text format using the [Python Tika library](https://github.com/chrismattmann/tika-python). 

### Step 3: Extract tables and figures
The next step was to identify unique features of each PDF page and their location coordinates. This information allows users to identify pages that have image features (ex. size of blocks, presence of text, etc.) and is used in modeling to identify ESA Figures. The [Python PyMuPDF library](https://pymupdf.readthedocs.io/en/latest/intro/) was used to extract these page-level PDF details. 

The extraction of tables from each PDF relied on a separate process. The [Python Camelot library](https://camelot-py.readthedocs.io/en/master/) was used to convert all tables from the PDFs into CSV (comma-separated value) files. Camelot relies on the presence of unique table features, (e.g. demarcated lines or presence of white space between cells) to identify tables in a PDF document.

Once tables and figures were identified, the next task was to label them with their respective title. 

### Step 4: Identify table and figure titles
The team used the ESA tables of contents from the PDF files (when available) together with a set of regular expressions to identify table and figure titles. Titles were then matched with their respective table or figure using regular expressions. In some instances, titles as they appear in the table of contents differed from the title spelling in the actual table or figure. Some calibration on matching was employed to match titles with figures or tables in such instances. 

### Step 5: Validate and verify
In general, programming the extraction of data out of PDFs is an imperfect process because each PDF can contain different table formats and be prepared and saved using different techniques. For example, tables with clear, black borders are easier to extract accurately compared to tables that have unclear or no borders. Our team employed a manual validation process for a sample of the tables, figures, and PDFs. We estimate that 94% - 98% of all tables in PDFs have been extracted, and that 88% - 94% of all tables have complete data. 

While it is not a perfect process due to inconsistency in formatting, tables and figures can now be searched quickly, and tables can be downloaded in a machine-readable format - both possibilities that did not exist previously.

### Acknowledgments
The data science team at the University of British Columbia was instrumental in guiding this project in its early days. The Canada Energy Regulator acknowledges the work of Nipun Goyal, Louis (Xiang) Luo, and Prakhar Sinha (with support from Martha Essak, Erin Martin-Serrano, Stuart Donald, and Gene Moo Lee) at the [Centre for Operations Excellence](https://www.sauder.ubc.ca/thought-leadership/research-outreach-centres/centre-operations-excellence), UBC Sauder School of Business.

