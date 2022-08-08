import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2].resolve()))
from berdi.Database_Connection_Files.connect_to_sqlserver_database import connect_to_db
import os
import pandas as pd
import PyPDF2
from tika import parser
import tika
import time
from multiprocessing import Pool, freeze_support
import re
from bs4 import BeautifulSoup
import traceback
from dotenv import load_dotenv


REPO_ROOT = Path(__file__).parents[2].resolve()
RAW_DATA = "data/raw"

# Load environment variables (from .env file) for the database
load_dotenv(
    dotenv_path=REPO_ROOT / "berdi/Database_Connection_Files" / ".env", override=True
)
conn = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path
# In order to extract the content from the PDFs, it is important to
# rotate the PDFs that are not in the normal top-to-bottom structure.
# The rotate_pdf function will rotate those PDFs to a normal structure.
pdf_files_folder_normal = REPO_ROOT / RAW_DATA / "pdfs"
pdf_files_folder_rotated90 = REPO_ROOT / RAW_DATA / "rotated_pdfs"
#pdf_files_folder_rotated270 = REPO_ROOT / RAW_DATA / "rotated_pdfs"

if not pdf_files_folder_normal.exists():
    print(pdf_files_folder_normal, "does not exist!")
if not pdf_files_folder_rotated90.exists():
    print(pdf_files_folder_rotated90, "does not exist!")
# if not pdf_files_folder_rotated270.exists():
#     print(pdf_files_folder_rotated270, "does not exist!")

# Tika configuration

# IMPORTANT: Before running this script, make sure you go through the following steps:
# 0. The following steps allow you to configure the Tika server to allow extraction of much bigger PDF files.
# Otherwise, the script will fail when you try to extract bigger files (especially when using multiprocessing).
# 1. Download: the java runtime (64-bit version) from https://www.java.com/en/download/manual.jsp
# Note: You can also use the jar file inside this directory and skip to step 3.
# 2. If you want to update tika version, go to: https://tika.apache.org/download.html
# 3. Run: java -d64 -jar -Xms40g -Xmx40g tika-server-standard-2.1.0.jar
# Adjust the memory (40g in this case) to 2/3rds of RAM you have available
# (Optional): if you know how to use docker, spin one of the containers here instead of downloading tika: https://hub.docker.com/r/apache/tika
# Note: the code runs slower on Windows if you use Docker because Windows needs to create a linux virtual environment.

# Set up Tika to extract text content from PDFs
tika.TikaClientOnly = True
os.environ["TIKA_STARTUP_MAX_RETRY"] = "10"
os.environ["TIKA_CLIENT_ONLY"] = "True"
os.environ["TIKA_SERVER_ENDPOINT"] = "http://127.0.0.1:9998"

tmp_folder = Path.cwd().joinpath("tmp")


# Careful! Removes all data!
def clear_db():
    """This function removes all data from the database."""

    stmt1 = "DELETE FROM pages_normal_txt;"
    stmt2 = "DELETE FROM pages_normal_xml;"
    stmt3 = "DELETE FROM pages_rotated90_txt;"
    stmt4 = "DELETE FROM pages_rotated90_xml;"
    stmt5 = "DELETE FROM pages_rotated270_txt;"
    stmt6 = "DELETE FROM pages_rotated270_xml;"
    with conn:
        cursor = conn.cursor()
        cursor.execute(stmt1)
        cursor.execute(stmt2)
        cursor.execute(stmt3)
        cursor.execute(stmt4)
        cursor.execute(stmt5)
        cursor.execute(stmt6)
    print("DB is cleared")


def clean_tmp():
    g = list(tmp_folder.glob("*.pdf"))
    for f in g:
        try:
            f.unlink()
        except Exception as e:
            print(e)
    print(f"Attempted to clean up {len(g)} files the tmp folder")


def clean_text(txt):
    rgx = re.compile(r"[^\w`~!@#$%^&*()_=+[{}|;:\',<.>/?\-\\\"\]]+")
    result = re.sub(rgx, " ", txt)
    return result.strip()


def insert_content(row):
    """This function extracts the text content from the PDFs and inserts it into the database."""

    pdf_id, total_pages = row["pdfId"], int(row["totalPages"])

    # Using PyPDF2 and Tika's parser method to extract PDF contents
    def process_pdf(pdf_folder, table_name, xml):
        # print(f"Starting {pdf_id}")
        if table_name == "pages_rotated90_txt":
            pdf = pdf_folder.joinpath(f"{pdf_id}_Rotated.pdf")
        else:
            pdf = pdf_folder.joinpath(f"{pdf_id}.pdf")
        if not pdf.exists():
            raise Exception(f"{pdf} does not exist! :(")
        with pdf.open(mode="rb") as infile, connect_to_db() as conn:
            cursor = conn.cursor()
            reader = PyPDF2.PdfFileReader(infile)
            if reader.isEncrypted:
                reader.decrypt("")
            # Looping for every PDF page and storing page contents into database table
            for p in range(1, total_pages + 1):
                check = f"SELECT pdfId FROM [DS_TEST].BERDI.{table_name} WHERE pdfId = ? AND page_num = ?"
                result = cursor.execute(check, (pdf_id, p))
                if result.rowcount > 0:
                    continue
                print(f"Working through {pdf_id} - page {p}")
                writer = PyPDF2.PdfFileWriter()
                writer.addPage(reader.getPage(p - 1))  # Reads from 0 page
                random_file = tmp_folder.joinpath(f"{os.urandom(24).hex()}.pdf")
                with random_file.open(mode="wb") as outfile:
                    writer.write(outfile)
                content = parser.from_file(
                    outfile.name, xmlContent=xml, requestOptions={"timeout": 300}
                )[
                    "content"
                ]  # Tika's parser extracts content of one page
                if content is None:
                    content = ""
                content = content.strip()
                # Using the custom clean_text function to strip the contents of specific characters with regex
                cleaned_content = clean_text(content)

                random_file.unlink()

                stmt = f"INSERT INTO [DS_TEST].BERDI.{table_name} (pdfId, page_num, content, clean_content) VALUES (?, ?, ?, ?);"
                result = cursor.execute(stmt, (pdf_id, p, content, cleaned_content))
                if result.rowcount != 1:
                    raise Exception(
                        f"{pdf_id}-{p}: ERROR! Updated {result.rowcount} rows!"
                    )

    # process_pdf(
    #     pdf_folder=pdf_files_folder_normal, table_name="pages_normal_xml", xml=True
    # )
    process_pdf(
        pdf_folder=pdf_files_folder_normal, table_name="pages_normal_txt", xml=False
    )
    # process_pdf(
    #     pdf_folder=pdf_files_folder_rotated90,
    #     table_name="pages_rotated90_xml",
    #     xml=True,
    # )
    process_pdf(
        pdf_folder=pdf_files_folder_rotated90,
        table_name="pages_rotated90_txt",
        xml=False,
    )
    # process_pdf(
    #     pdf_folder=pdf_files_folder_rotated270,
    #     table_name="pages_rotated270_xml",
    #     xml=True,
    # )
    # process_pdf(
    #     pdf_folder=pdf_files_folder_rotated270,
    #     table_name="pages_rotated270_txt",
    #     xml=False,
    # )


def insert_contents(multiprocessing=False):
    """
    Inserts the text content of the PDFs into the database by using the
    insert_content function either sequentially or with multiprocessing.
    """

    t = time.time()

    # Reading from the MySQL Database and creating dataframe from query
    stmt = "SELECT pdfId, totalPages FROM [DS_TEST].BERDI.pdfs ORDER BY totalPages;"
    with conn:
        df = pd.read_sql(stmt, conn)
    data = df.to_dict("records")

    parser.from_file(__file__)  # testing tika server
    print("Server apparently works...")

    clean_tmp()
    skipping = []
    current_id = None
    if multiprocessing == False:
        for row in data:
            try:
                current_id = row["pdfId"]
                insert_content(row)
                print(f"Done {current_id}")
            except Exception as e:
                skipping.append(current_id)
                print(f"ERROR! {current_id}: {e}")
    else:
        # Running the insert_content function with multiprocessing
        with Pool(96) as pool:
            pool.map(insert_content, data, chunksize=1)

        count = 0
        while True:
            try:
                clean_tmp()
                with Pool() as pool:
                    pool.map(insert_content, data, chunksize=1)
            except Exception as e:
                print("\n===========================================================\n")
                print(f"Counter: {count}: {e}")
                traceback.print_tb(e.__traceback__)
                print("\n===========================================================\n")
                count += 1
            else:
                print(f"Final counter value is {count}")
                break

    sec = round(time.time() - t)
    print(
        f"Done {len(data)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)"
    )


def insert_clean_content(table):
    """Cleans the text content of the PDFs saved in the database and updates the database."""

    t = time.time()

    stmt = f"SELECT pdfId, page_num, content FROM [DS_TEST].BERDI.{table} WHERE clean_content IS NULL;"
    with conn:
        cursor = conn.cursor()
        df = pd.read_sql(stmt, conn)
        data = df.to_dict("records")
        for item in data:
            cleaned_text = clean_text(item["content"])
            query = f"UPDATE [DS_TEST].BERDI.{table} SET clean_content = ? WHERE pdfId = ? AND page_num = ?"
            result = cursor.execute(
                query, (cleaned_text, item["pdfId"], item["page_num"])
            )
            if result.rowcount != 1:
                raise Exception(f"{item}: updated {result.rowcount} rows")
            print(item["pdfId"], item["page_num"], "is done")

    sec = round(time.time() - t)
    print(
        f"Done {len(data)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)"
    )


def insert_clean_contents():
    insert_clean_content("pages_normal_txt")
    insert_clean_content("pages_rotated90_txt")
    # insert_clean_content("pages_rotated270_txt")


def rotate_pdf(pdf):
    """Rotates the PDFs so that they are all in the correct orientation."""

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
    # pdf_path270 = pdf_files_folder_rotated270.joinpath(f"{pdf.stem}.pdf")
    rotate(pdf_path90, 90)
    # rotate(pdf_path270, 270)


def rotate_pdfs(multiprocessing=False):
    """
    Rotates the PDFs so that they are all in the correct orientation using
    the rotate_pdf function either sequentially or with multiprocessing.

    multiprocessing: bool
        If True, the PDFs are rotated using multiprocessing.
    """

    t = time.time()
    pdfs = list(pdf_files_folder_normal.glob("*.pdf"))

    if multiprocessing == False:
        for pdf_file in pdfs:
            rotate_pdf(pdf_file)
    else:
        with Pool() as pool:
            pool.map(rotate_pdf, pdfs, chunksize=1)

    sec = round(time.time() - t)
    print(
        f"Done {len(pdfs)} in {sec} seconds ({round(sec / 60, 2)} min or {round(sec / 3600, 2)} hours)"
    )


def clean_xml(xml_string):
    """Cleans text from the PDFs by removing unecessary XML tags and whitespace."""

    soup = BeautifulSoup(xml_string, features="lxml")
    page = soup.find("div", class_="page")
    for tag in page.find_all():
        if (
            len(tag.get_text(strip=True)) == 0
        ):  # removing empty tags like <p></p> or <p />
            tag.extract()
        tag.string = tag.get_text(
            strip=True
        )  # trimming whitespace in the beginning/end
    output = "".join(str(child) for child in page.findChildren(recursive=False))
    return output


if __name__ == "__main__":
    freeze_support()

    # # Caution! Removes all data!
    # # Only make clear_database = True, if you want to remove all data from the database.
    # # Making this part verbose and commenting it to prevent accidental deletion of data.
    # clear_database = False
    # if clear_database == True:
    #     clear_db()
    #rotate_pdfs(multiprocessing=True)
    insert_contents(multiprocessing=False)
    insert_clean_contents()
