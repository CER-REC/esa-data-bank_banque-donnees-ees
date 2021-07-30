import pandas as pd
import numpy as np
from Codes.Database_Connection_Files.connect_to_database import connect_to_db


table_info_csv_path = 'Data_Files/all_tables-final.csv'
df_table_info = pd.read_csv(table_info_csv_path)

# df_table_info.shape  # (1348, 8)
df_table_info = df_table_info[df_table_info['titleFinal'].notna()][['csvFullPath', 'pdfId', 'page', 'tableNumber', 'titleFinal']]

# Get the application index file
df_app = pd.read_csv('Input_Files/Phase2_Index_of_PDFs_for_Major_Projects_with_ESAs.csv')
# Get PDF total number of page
engine = connect_to_db()
conn = engine.connect()
df_pdf_page = pd.read_sql('select pdfId, totalPages from pdfs;', con=conn)

# Organize pdf attributes
['Application Name', 'Application Short Name', 'Application Filing Date',
 'Company Name', 'Commodity',
 'File Name', 'ESA Folder URL', 'Document Number', 'PDF Download URL',
 'Application Type (NEB Act)', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
 'ESA Section(s)', 'ESA Section(s) Index', 'ESA Section(s) Topics',
 'PDF Page Count', 'PDF Size', 'PDF Outline']

df_example = pd.read_csv('G:/ESA_downloads/download_Bingjie_Mar262021/ESA_website_ENG.csv', nrows=20)

df_app.columns
df_app = df_app[['Application Name', 'Application Short Name', 'Application Filing Date',
                 'Company Name', 'Commodity',
                 'File Name', 'ESA Folder URL', 'Document Number', 'Data ID', 'PDF Download URL',
                 'Application Type (NEB Act)', 'Pipeline Location', 'Hearing Order', 'Consultant Name',
                 'Pipeline Status', 'Regulatory Instrument(s)', 'Application URL', 'Decision URL',
                 'ESA Section(s)', 'ESA Section(s) Index']].merge(df_pdf_page, left_on='Data ID', right_on='pdfId')
df_app = df_app.rename(columns={'totalPages': 'PDF Page Count'})
df_app = df_app.drop(labels=['pdfId'], axis=1)

# Compose pdf and csv table attributes
df_table_app = df_table_info.merge(df_app, left_on='pdfId', right_on='Data ID')
df_table_app = df_table_app.rename(columns={'page': 'PDF Page Number', 'titleFinal': 'Title'})
df_table_app = df_table_app.drop(labels=['pdfId'], axis=1)


df_table_app.groupby('Data ID')[['csvFullPath']].count().reset_index()\
    .rename(columns={'csvFullPath': 'csv_count'}).merge(df_pdf_page, left_on='Data ID', right_on='pdfId')\
    .drop(labels=['pdfId'], axis=1)

##### ====== QA on cav tables ======
# see Codes/Section_04_Final_Data_Merge_and_Visualization/quality_check/qa_metrics.py
df_index = df_table_app.copy()

for col in ['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']:
    df_index[col] = np.nan

for index, (path) in df_index[['csvFullPath']].itertuples():
    # path = 'G:/ESA_downloads/copy_Bingjie/{}'.format('/'.join(csv_url.split('/')[-2:]))
    try:
        df_csv_temp = pd.read_csv(path, header=None)

        df_index.loc[index, 'csv_row_count'] = df_csv_temp.shape[0]
        df_index.loc[index, 'csv_column_count'] = df_csv_temp.shape[1]
        df_index.loc[index, 'csv_null_cell_count'] = df_csv_temp.isnull().sum().sum()

        count_cid_cell = 0
        for col in df_csv_temp.columns:
            if str(df_csv_temp[col].dtype) == 'object':
                count_cid_cell += df_csv_temp[col].str.contains('cid:').sum()
        df_index.loc[index, 'csv_cid_cell_count'] = count_cid_cell
    except:
        print(path)
        continue

df_index['qa_single_row_or_col'] = df_index[['csv_row_count', 'csv_column_count']].apply(
    lambda x: x['csv_row_count'] == 1 or x['csv_column_count'] == 1, axis=1
)
df_index['qa_blank_cell_percent'] = df_index[['csv_row_count', 'csv_column_count', 'csv_null_cell_count']].apply(
    lambda x: round(100 * x['csv_null_cell_count'] / (x['csv_row_count'] * x['csv_column_count']), 2), axis=1
)
df_index['qa_cid_cell_percent'] = df_index[['csv_row_count', 'csv_column_count', 'csv_null_cell_count', 'csv_cid_cell_count']].apply(
    lambda x: round(100 * x['csv_cid_cell_count'] / (x['csv_row_count'] * x['csv_column_count'] - x['csv_null_cell_count']), 2), axis=1
)
# Calculate duplicates
df_table_count = df_index.groupby(['Title', 'Data ID', 'PDF Page Number'])['csvFullPath'].count()\
    .reset_index().rename(columns={'csvFullPath': 'count'})
df_duplicate = df_table_count[df_table_count['count'] > 1]

df_index = df_index.merge(df_duplicate, how='left', on=['Title', 'Data ID', 'PDF Page Number'])
df_index['qa_duplicate'] = df_index['count'].notna()

df_index['qa_single_row_or_col'].sum()  # 0
df_index[df_index['qa_blank_cell_percent'] > 72].shape[0]  # 6
df_index[df_index['qa_cid_cell_percent'] > 80].shape[0]  # 6
df_index['qa_blank'] = df_index['qa_blank_cell_percent'] > 72
df_index['qa_cid'] = df_index['qa_cid_cell_percent'] > 80
df_index['qa_any'] = df_index[['qa_blank', 'qa_cid', 'qa_duplicate', 'qa_single_row_or_col']].any(axis=1)

df_pdf = df_index.groupby('PDF Download URL')[['qa_single_row_or_col', 'qa_blank', 'qa_cid', 'qa_duplicate','qa_any']].sum().reset_index()
df_pdf_count = df_index.groupby('PDF Download URL')['csvFullPath'].count().reset_index().rename(columns={'csvFullPath': 'total_csv'})
df_pdf = df_pdf.merge(df_pdf_count)

df_pdf['single_%'] = df_pdf[['qa_single_row_or_col', 'total_csv']].apply(lambda x: 100*round(x['qa_single_row_or_col']/x['total_csv'], 2), axis=1)
df_pdf['blank_%'] = df_pdf[['qa_blank', 'total_csv']].apply(lambda x: 100*round(x['qa_blank']/x['total_csv'], 2), axis=1)
df_pdf['cid_%'] = df_pdf[['qa_cid', 'total_csv']].apply(lambda x: 100*round(x['qa_cid']/x['total_csv'], 2), axis=1)
df_pdf['duplicate_%'] = df_pdf[['qa_duplicate', 'total_csv']].apply(lambda x: 100*round(x['qa_duplicate']/x['total_csv'], 2), axis=1)
df_pdf['any_%'] = df_pdf[['qa_any', 'total_csv']].apply(lambda x: 100*round(x['qa_any']/x['total_csv'], 2), axis=1)

df_pdf_meta = df_index[['Data ID', 'PDF Download URL', 'Application Short Name']].drop_duplicates()
df_pdf = df_pdf.merge(df_pdf_meta, on='PDF Download URL')
df_pdf = df_pdf.sort_values('any_%', ascending=False, ignore_index=True)\
    [['Data ID','Application Short Name','qa_single_row_or_col','qa_blank','qa_cid','qa_duplicate','qa_any','total_csv','single_%','blank_%','cid_%','duplicate_%','any_%']]

df_pdf[['Data ID','Application Short Name','any_%']]
#    Data ID        Application Short Name  any_%
# 0  3970830  NGTL West Path Delivery 2022    6.0
# 1  3974826  NGTL West Path Delivery 2023    4.0
# 2  3970829  NGTL West Path Delivery 2022    2.0
# 3  4003703  NGTL West Path Delivery 2023    1.0
# 4  3931508  NGTL West Path Delivery 2022    0.0
# 5  3969837  NGTL West Path Delivery 2022    0.0
# 6  3970827  NGTL West Path Delivery 2022    0.0
# 7  3970828  NGTL West Path Delivery 2022    0.0
# 8  3974108  NGTL West Path Delivery 2023    0.0
# 9  3974307  NGTL West Path Delivery 2023    0.0

