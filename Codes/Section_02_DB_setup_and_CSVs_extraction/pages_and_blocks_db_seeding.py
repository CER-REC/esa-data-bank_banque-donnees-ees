import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from Database_Connection_Files.connect_to_database import connect_to_db
from dotenv import load_dotenv
from multiprocessing import Pool
import time
from sqlalchemy import text
import os
import pandas as pd
import fitz
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import traceback


# Load environment variables (from .env file) for the database
engine = connect_to_db()

# Load environment variables (from .env file) for the PDF folder path
pdf_files_folder = Path(os.getenv("PDFS_FILEPATH"))

# Careful! Deletes all pages and blocks data from the DB!
# noinspection SqlWithoutWhere
# def clear_figures_db():
#     with engine.connect() as conn:
#         result2 = conn.execute("DELETE FROM blocks;")
#         print(f"Deleted {result2.rowcount} blocks.")
#         result1 = conn.execute("DELETE FROM pages;")
#         print(f"Deleted {result1.rowcount} pages.")


def insert(pdf):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            pdf_file_path = pdf_files_folder.joinpath(f"{pdf['pdfId']}.pdf")
            # noinspection PyUnresolvedReferences
            doc = fitz.open(pdf_file_path)
            for page in doc:
                figures = page.searchFor('Figure')
                page_num = page.number + 1
                rotation = page.rotation
                try:
                    image_list = page.getImageList()  # get list of used images
                except Exception as e:
                    image_list = []
                    print('Error getting image list for:', pdf['pdfId'], page_num, e)
                num_images = len(image_list)
                page_text = page.getText('dict')  # list, extract the page’s text
                width = page_text['width']
                height = page_text['height']
                media_x0 = page.MediaBox[0]
                media_y0 = page.MediaBox[1]
                media_x1 = page.MediaBox[2]
                media_y1 = page.MediaBox[3]
                media_width = page.MediaBoxSize[0]
                media_height = page.MediaBoxSize[1]
                page_area = width * height

                with engine.connect() as conn:
                    stmt = "INSERT INTO pages (pdfId,page_num,width,height,rotation," \
                           "figures,num_images,media_x0,media_y0,media_x1,media_y1," \
                           "media_width,media_height,page_area) " \
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    params = (pdf['pdfId'], page_num, width, height, rotation,
                              len(figures), num_images, media_x0, media_y0, media_x1, media_y1,
                              media_width, media_height, page_area,)
                    conn.execute(stmt, params)

                for index, block in enumerate(page_text['blocks']):
                    t = block['type']
                    bbox = block['bbox']
                    if t == 1:
                        ext, color, xres, yres, bpc, image = block['ext'], block['colorspace'], block['xres'], block[
                            'yres'], block['bpc'], block['image']
                        block_width, block_height = block['width'], block['height']
                        block_area = block_width * block_height
                    else:
                        ext, color, xres, yres, bpc, image = None, None, None, None, None, None
                        block_width, block_height = None, None
                        block_area = None

                    bbox_x0, bbox_y0, bbox_x1, bbox_y1 = bbox

                    bbox_width = bbox_x1 - bbox_x0
                    bbox_height = bbox_y1 - bbox_y0
                    bbox_area = bbox_width * bbox_height
                    bbox_area_image = bbox_area * t

                    with engine.connect() as conn:
                        stmt = text("INSERT INTO blocks (pdfId,page_num,type,block_width,block_height,"
                                    "bbox_x0,bbox_y0,bbox_x1,bbox_y1,ext,color,xres,yres,bpc,block_area,"
                                    "bbox_width,bbox_height,bbox_area,bbox_area_image, block_order) "
                                    "VALUES (:pdfId,:page_num,:type,:block_width,:block_height,"
                                    ":bbox_x0,:bbox_y0,:bbox_x1,:bbox_y1,:ext,:color,:xres,:yres,:bpc,:block_area,"
                                    ":bbox_width,:bbox_height,:bbox_area,:bbox_area_image,:block_order);")

                        params = {'pdfId': pdf['pdfId'], 'page_num': page_num, 'width': width, 'height': height,
                                  'rotation': rotation, 'figures': len(figures),
                                  'num_images': num_images, 'type': t, 'block_width': block_width,
                                  'block_height': block_height, "block_area": block_area, 'media_x0': media_x0,
                                  'media_y0': media_y0, 'media_x1': media_x1, 'media_y1': media_y1,
                                  'media_width': media_width, 'media_height': media_height, 'bbox_x0': bbox_x0,
                                  'bbox_y0': bbox_y0, 'bbox_x1': bbox_x1, 'bbox_y1': bbox_y1, 'ext': ext,
                                  'color': color, 'xres': xres, 'yres': yres, 'bpc': bpc, "bbox_width": bbox_width,
                                  "bbox_height": bbox_height, "bbox_area": bbox_area,
                                  "bbox_area_image": bbox_area_image, "block_order": index + 1}
                        conn.execute(stmt, params)
            with engine.connect() as conn:
                statement = text("UPDATE pdfs SET pagesBlocksExtracted = 1 WHERE pdfId = :pdfId;")
                conn.execute(statement, {"pdfId": pdf['pdfId']})
            print(f"{pdf['pdfId']} is done.")
        except Exception as e:
            print(f"{pdf['pdfId']}: ERROR! {e}")
            traceback.print_tb(e.__traceback__)
        finally:
            return buf.getvalue()


def insert_pages_and_blocks():
    stmt = text("SELECT pdfId, totalPages FROM pdfs WHERE pagesBlocksExtracted = 0 ORDER BY totalPages DESC;")
    with engine.connect() as conn:
        df = pd.read_sql(stmt, conn)
    args = df.to_dict("records")

    print(f"Items to process: {len(args)}")
    start_time = time.time()

    # Sequential mode - if using, please comment out the multiprocessing mode code
    # for arg in args[-10:]:
    #     result = insert_pdf(arg)
    #     print(result, end='', flush=True)

    # Multiprocessing mode - if using, please comment out the sequential mode code
    with Pool() as pool:
        results = pool.map(insert, args, chunksize=1)
    for result in results:
        print(result, end='', flush=True)

    d = round(time.time() - start_time)
    print(f"Done {len(args)} in {d} seconds ({round(d / 60, 2)} min or {round(d / 3600, 2)} hours)")


if __name__ == "__main__":
    insert_pages_and_blocks()
