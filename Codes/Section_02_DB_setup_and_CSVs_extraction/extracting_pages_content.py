import sys
from pathlib import Path
from Codes.Database_Connection_Files.connect_to_database import connect_to_db
from dotenv import load_dotenv
import os
import pandas as pd
import PyPDF2
from tika import parser
import tika
import time
from multiprocessing import Pool
import re
from bs4 import BeautifulSoup
sys.path.append(str(Path(__file__).parent.parent.absolute()))

# Load environment variables from .env file
load_dotenv(override=True)

# Load environment variables (from .env file) for the database
engine = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path
# In order to extract the content from the PDFs, it is important to
# rotate the PDFs that are not in the normal top-to-bottom structure.
# You will likely need to run this code first and the PDFs with bad
# results are likely due to the PDF structure. Put the PDFs that
# need to be rotated by 90 degrees in a PDF_rotated90 folder and
# those that need to be rotated by 270 in a PDF_rotated270 folder.
# The rotate_pdf function will rotate those PDFs to a normal structure.
pdf_files_folder_normal = Path(os.getenv("PDFS_FILEPATH"))
pdf_files_folder_rotated90 = Path(os.getenv("PDFS_FILEPATH") + "_Rotated")
pdf_files_folder_rotated270 = Path(os.getenv("PDFS_FILEPATH") + "_rotated270")

if not pdf_files_folder_normal.exists():
    print(pdf_files_folder_normal, "does not exist!")
if not pdf_files_folder_rotated90.exists():
    print(pdf_files_folder_rotated90, "does not exist!")
if not pdf_files_folder_rotated270.exists():
    print(pdf_files_folder_rotated270, "does not exist!")

# Increase max size of pandas dataframe output when using a notebook
pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1200)

# Set up Tika to extract text content from PDFs
tika.TikaClientOnly = True
os.environ["TIKA_STARTUP_MAX_RETRY"] = "10"
os.environ["TIKA_CLIENT_ONLY"] = "True"
os.environ["TIKA_SERVER_ENDPOINT"] = "http://127.0.0.1:9998"

tmp_folder = Path.cwd().joinpath("tmp")


# Careful! Removes all data!
# def clear_db():
#     stmt1 = "DELETE FROM pages_normal_txt;"
#     stmt2 = "DELETE FROM pages_normal_xml;"
#     stmt3 = "DELETE FROM pages_rotated90_txt;"
#     stmt4 = "DELETE FROM pages_rotated90_xml;"
#     stmt5 = "DELETE FROM pages_rotated270_txt;"
#     stmt6 = "DELETE FROM pages_rotated270_xml;"
#     with engine.connect() as conn:
#         conn.execute(stmt1)
#         conn.execute(stmt2)
#         conn.execute(stmt3)
#         conn.execute(stmt4)
#         conn.execute(stmt5)
#         conn.execute(stmt6)
#     print("DB is cleared")


def clean_tmp():
    g = list(tmp_folder.glob("*.pdf"))
    for f in g:
        try:
            f.unlink()
        except Exception as e:
            print(e)
    print(f"Attempted to clean up {len(g)} files the tmp folder")


def clean_text(txt):
    rgx = re.compile(r'[^\w`~!@#$%^&*()_=+[{}|;:\',<.>/?\-\\\"\]]+')
    result = re.sub(rgx, " ", txt)
    return result.strip()


def insert_content(row):
    pdf_id, total_pages = row["pdfId"], int(row["totalPages"])

    # Using PyPDF2 and Tika's parser method to extract PDF contents
    def process_pdf(pdf_folder, table_name, xml):
        # print(f"Starting {pdf_id}")
        if table_name == 'pages_rotated90_txt':
            pdf = pdf_folder.joinpath(f"{pdf_id}_Rotated.pdf")
        else:
            pdf = pdf_folder.joinpath(f"{pdf_id}.pdf")
        if not pdf.exists():
            raise Exception(f"{pdf} does not exist! :(")
        with pdf.open(mode="rb") as infile, engine.connect() as conn:
            reader = PyPDF2.PdfFileReader(infile)
            if reader.isEncrypted:
                reader.decrypt("")
            # Looping for every PDF page and storing page contents into database table
            for p in range(1, total_pages + 1):
                check = f"SELECT pdfId FROM {table_name} WHERE pdfId = %s AND page_num = %s;"
                result = conn.execute(check, (pdf_id, p))
                if result.rowcount > 0:
                    continue
                print(f"Working through {pdf_id} - page {p}")
                writer = PyPDF2.PdfFileWriter()
                writer.addPage(reader.getPage(p - 1))  # Reads from 0 page
                random_file = tmp_folder.joinpath(f"{os.urandom(24).hex()}.pdf")
                with random_file.open(mode="wb") as outfile:
                    writer.write(outfile)
                content = parser.from_file(outfile.name, xmlContent=xml, requestOptions={'timeout': 300})["content"] # Tika's parser extracts content of one page
                if content is None:
                    content = ""
                content = content.strip()
                # Using the custom clean_text function to strip the contents of specific characters with regex
                cleaned_content = clean_text(content)

                random_file.unlink()

                stmt = f"INSERT INTO {table_name} (pdfId, page_num, content, clean_content) VALUES (%s,%s,%s,%s);"
                result = conn.execute(stmt, (pdf_id, p, content, cleaned_content))
                if result.rowcount != 1:
                    raise Exception(f"{pdf_id}-{p}: ERROR! Updated {result.rowcount} rows!")

    # process_pdf(pdf_folder=pdf_files_folder_normal, table_name="pages_normal_xml", xml=True)
    # process_pdf(pdf_folder=pdf_files_folder_normal, table_name="pages_normal_txt", xml=False)
    # process_pdf(pdf_folder=pdf_files_folder_rotated90, table_name="pages_rotated90_xml", xml=True)
    process_pdf(pdf_folder=pdf_files_folder_rotated90, table_name="pages_rotated90_txt", xml=False)
    # process_pdf(pdf_folder=pdf_files_folder_rotated270, table_name="pages_rotated270_xml", xml=True)
    # process_pdf(pdf_folder=pdf_files_folder_rotated270, table_name="pages_rotated270_txt", xml=False)


def insert_contents():
    t = time.time()

    # Reading from the MySQL Database and creating dataframe from query
    stmt = "SELECT pdfId, totalPages FROM pdfs ORDER BY totalPages;"
    with engine.connect() as conn:
        df = pd.read_sql(stmt, conn)
    data = df.to_dict("records")

    # java -d64 -jar -Xms50g -Xmx50g tika-server-1.24.jar
    parser.from_file(__file__)  # testing tika server
    print('Server apparently works...')

    clean_tmp()
    skipping = []
    current_id = None
    for row in data:
        try:
            current_id = row["pdfId"]
            insert_content(row)
            print(f"Done {current_id}")
        except Exception as e:
            skipping.append(current_id)
            print(f"ERROR! {current_id}: {e}")
    # print(skipping)

    # for row in data:
    #     insert_content(row)

    # Running the insert_content function with multiprocessing
    # with Pool(96) as pool:
    #     pool.map(insert_content, data, chunksize=1)

    # count = 0
    # while True:
    #     try:
    #         clean_tmp()
    #         with Pool() as pool:
    #             pool.map(insert_content, data, chunksize=1)
    #     except Exception as e:
    #         print("\n===========================================================\n")
    #         print(f"Counter: {count}: {e}")
    #         traceback.print_tb(e.__traceback__)
    #         print("\n===========================================================\n")
    #         count += 1
    #     else:
    #         print(f"Final counter value is {count}")
    #         break

    sec = round(time.time() - t)
    print(f"Done {len(data)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)")


def insert_clean_content(table):
    t = time.time()

    stmt = f"SELECT pdfId, page_num, content FROM {table} WHERE clean_content IS NULL;"
    with engine.connect() as conn:
        df = pd.read_sql(stmt, conn)
        data = df.to_dict("records")
        for item in data:
            cleaned_text = clean_text(item["content"])
            query = f"UPDATE {table} SET clean_content = %s WHERE pdfId = %s AND page_num = %s"
            result = conn.execute(query, (cleaned_text, item["pdfId"], item["page_num"]))
            if result.rowcount != 1:
                raise Exception(f"{item}: updated {result.rowcount} rows")
            print(item["pdfId"], item["page_num"], "is done")

    sec = round(time.time() - t)
    print(f"Done {len(data)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)")


def insert_clean_contents():
    insert_clean_content("pages_normal_txt")
    insert_clean_content("pages_rotated90_txt")
    # insert_clean_content("pages_rotated270_txt")


def rotate_pdf(pdf):
    def rotate(target_pdf, rotation):
        if target_pdf.exists():
            return
        with pdf.open(mode="rb") as in_file, target_pdf.open(mode="wb") as out_file:
            reader = PyPDF2.PdfFileReader(in_file)
            writer = PyPDF2.PdfFileWriter()
            for p in range(reader.getNumPages()):
                page = reader.getPage(p)
                page.rotateClockwise(rotation)
                writer.addPage(page)
            writer.write(out_file)

    pdf_path90 = pdf_files_folder_rotated90.joinpath(f"{pdf.stem}.pdf")
    pdf_path270 = pdf_files_folder_rotated270.joinpath(f"{pdf.stem}.pdf")
    rotate(pdf_path90, 90)
    rotate(pdf_path270, 270)
    # print(f"Done {pdf.stem}")


def rotate_pdfs():
    t = time.time()

    pdfs = list(pdf_files_folder_normal.glob("*.pdf"))

    # for pdf_file in pdfs:
    #     rotate_pdf(pdf_file)

    with Pool() as pool:
        pool.map(rotate_pdf, pdfs, chunksize=1)

    sec = round(time.time() - t)
    print(f"Done {len(pdfs)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)")


def clean_xml(xml_string):
    soup = BeautifulSoup(xml_string, features="lxml")
    page = soup.find('div', class_="page")
    for tag in page.find_all():
        if len(tag.get_text(strip=True)) == 0:  # removing empty tags like <p></p> or <p />
            tag.extract()
        tag.string = tag.get_text(strip=True)  # trimming whitespace in the beginning/end
    output = "".join(str(child) for child in page.findChildren(recursive=False))
    return output


if __name__ == "__main__":
    # rotate_pdfs() # run this if you need to rotate PDFs
    insert_contents()
    # insert_clean_contents()
