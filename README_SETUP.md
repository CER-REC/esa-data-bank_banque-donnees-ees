# Introduction
----------------------------------------------------------------------------------------

# Getting Started
----------------------------------------------------------------------------------------

1. Login into the SQL server (SQL Server Management Studio 18).

2. Use the following the database script in sequence. Replace Database name and schema name 
accordingly.
   a. src\database\4_drop_tables.sql (to remove existing tables)
   b. src\database\0_create_initial_tables.sql (to create necessary tables for processing)
   c. src\database\1_PR_Load_TableElement.sql (to add stored procedure for loading tables)
   d. src\database\2_PR_Load_Figure.sql (to add stored procedure for loading table figures)
   e. src\database\3_PR_Load_AlignmentSheet.sql (to add stored procedure for loading alignment sheets)
   f. src\database\8_insert_value_component.sql (to add value component categories)
   g. src\database\9_insert_generic_translation.sql (to add english to french translations
      of generic terms)

3. To create a python virtual environment and install required packages, run the following commands:
   
   > python -m venv venv
   > venv\Scripts\activate
   > python -m pip install --upgrade pip
   > pip install -r requirements.txt
   
   Python Version: 3.11.2 
    
4. Create a .env file. Use .env.sampe as reference.
5. Run pytest and pylint:
   > pytest
   > pylint src

6. Create a new terminal with the existing virtual environment enabled and use the following command to 
   start the Prefect server:

   > prefect server start

   Visit the Prefect UI at http://127.0.0.1:4200/

7. Create another terminal and use the following command to setup the Prefect deployment backend process:
   
   > prefect agent start -p default-agent-pool

8. Create all the necessary prefect deployment flows at once using the following command:
   > python -m src.prefect.create_deployment_flows

9. Visit Prefect UI to ensure that the deployment steps are created properly. The steps are named according 
   to their execution sequence. Each deploment sequence / flow starts with "Step_{step_number}_{step_name}". 
   Execute (Prefect URL -> Deployments -> click on the deployment -> Run -> Quick Run -> enter the required 
   parameter(s)) steps 1 to 3. Sent the translation file to the translation team to translate terms from 
   english to french. Once the translation file is completed, execute steps 4 to 5 to generate the final 
   output files.

# Build and Test
----------------------------------------------------------------------------------------

Run pytest and pylint before merging to main branch


# Special Instructions:
----------------------------------------------------------------------------------------

1. Tika parser does not support page level text processing. Therefore, we read the Pdf content using  
   PyPDF2 and then store each page separately in a different directory. Finally, Tika parser is used to 
   extract the text content from the pdf. 

2. Install Ghostscript using the following link:
   https://ghostscript.com/releases/gsdnld.html

3. Install Java using the following link:
   https://www.java.com/download/ie_manual.jsp

   [Make sure to restart VSCode or Operating System after installing the above mentioned softwares]

4. Ensure that the following folder structure is present to store the intermidiary processing
   data, the input data, and the final output data. 
   a. data-----|
               |----- raw  |
                           | --- pdfs
                           | --- pdf_pages
                           | --- pdf_rotated90_pages
               |--- index  |
                           | --- index.csv (main input file)
   b. log
   c. output ---|
                |---- internal   |
                                 |---- en |
                                          |---- projects
                                          |---- tables
                                 |---- fr |
                                          |---- projects
                                          |---- tables
                |---- external   |
                                 |---- en |
                                          |---- projects
                                          |---- tables
                                 |---- fr |
                                          |---- projects
                                          |---- tables
                | --- thumbnails
                | --- README-ENG-tables.txt
                | --- README-ENG-projects.txt
                | --- README-FRA-tables.txt
                | --- README-FRA-projects.txt

   

# Libraries
----------------------------------------------------------------------------------------

Currently using SQLAlchemy==1.4.46 due to incompatibility with Pandas read_sql (https://github.com/pandas-dev/pandas/issues/51015)
Need to upgrade to the latest version of SQLAlchemy when issue resolved

