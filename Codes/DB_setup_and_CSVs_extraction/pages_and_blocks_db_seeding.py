import re
from pathlib import Path
from dotenv import load_dotenv
from multiprocessing import Pool
import time
from sqlalchemy import text, create_engine
import sqlalchemy
import os
import pandas as pd
import json
import fitz
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import traceback


load_dotenv(override=True)
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
engine_string = f"mysql+mysqldb://{user}:{password}@{host}/{database}?charset=utf8mb4"
engine = create_engine(engine_string)

pdf_files_folder = Path("//luxor/data/branch/Environmental Baseline Data\Version 4 - Final/PDF")


def get_all_pdfs():
    with engine.connect() as conn:
        stmt = text("SELECT pdfId, totalPages FROM pdfs ORDER BY totalPages DESC;")
        df = pd.read_sql(stmt, conn)
        return df.to_dict("records")


def clear_figures_DB():
    with engine.connect() as conn:
        result2 = conn.execute("DELETE FROM blocks;")
        print(f"Deleted {result2.rowcount} blocks.")
        result1 = conn.execute("DELETE FROM pages;")
        print(f"Deleted {result1.rowcount} pages.")


def insert_pdf(pdf):
    buf = StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            pdf_file_path = pdf_files_folder.joinpath(f"{pdf['pdfId']}.pdf")
            doc = fitz.open(pdf_file_path)
            for page in doc:
                figures = page.searchFor('Figure')
                page_num = page.number + 1
                rotation = page.rotation
                try:
                    image_list = page.getImageList()  # get list of used images
                except:
                    image_list = []
                    print('Error getting image list for:', pdf['pdfId'], page_num)
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
                    result = conn.execute(stmt, params)

                for index, block in enumerate(page_text['blocks']):
                    t = block['type']
                    bbox = block['bbox']
                    if t == 1:
                        ext, color, xres, yres, bpc, image = block['ext'], block['colorspace'], block['xres'], block['yres'], block['bpc'], block['image']
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
                        result = conn.execute(stmt, params)
            print(f"{pdf['pdfId']} is done.")
        except Exception as e:
            print(f"{pdf['pdfId']}: ERROR! {e}")
            traceback.print_tb(e.__traceback__)
        finally:
            return buf.getvalue()


def insert_pdfs(args):
    print(f"Items to process: {len(args)}")
    start_time = time.time()

    # Sequential mode
    # for arg in args[-2:-1]:
    #     result = insert_pdf(arg)
    #     print(result[:-1])

    # Multiprocessing mode
    with Pool() as pool:
        results = pool.map(insert_pdf, args, chunksize=1)
    for result in results:
        print(result[:-1])

    duration = round(time.time() - start_time)
    print(f"Done {len(args)} in {duration} seconds ({round(duration/60, 2)} min or {round(duration/3600, 2)} hours)")


if __name__ == "__main__":
    clear_figures_DB()  # Careful! Deletes all pages and blocks data from the DB!
    data = get_all_pdfs()
    insert_pdfs(data)
