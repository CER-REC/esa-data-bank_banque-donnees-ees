import pandas as pd
import time
import os
from pathlib import Path
import multiprocessing as mp
from multiprocessing import freeze_support
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
from file_preparation import download_file, rotate_pdf, pickle_pdf_xml
from pdf_metadata import get_pdf_metadata


if __name__ == "__main__":

    # Necesary to avoid the error with multiprocessing
    # For more info (Windows): https://www.kite.com/python/docs/exceptions.RuntimeError
    # If using Linux/MacOS: https://pythonspeed.com/articles/python-multiprocessing/
    freeze_support()

    # Update the path when adding a new list of projects
    ROOT_PATH = Path(__file__).resolve().parents[2]
    Index0_path = str(
        ROOT_PATH
        / "data"
        / "raw"
        / "index_for_projects"
        / "Index_of_PDFs_for_Fall_2022_application_refresh.csv"
    )

    # Load the list of projects
    Index0 = pd.read_csv(Index0_path, encoding ='utf-8-sig')

    # Download files
    count = download_file(str(ROOT_PATH), Index0)
    print("{} Files were downloaded from {} URL links".format(count, len(Index0)))

    # Rotate files
    count = rotate_pdf(str(ROOT_PATH), Index0)
    print("{} Files were successfully rotated".format(count))

    # Convert to pickle files
    for pdf_folder_name, pickle_file_folder_name in {
        ("pdfs", "pickle_files"),
        ("rotated_pdfs", "pickle_files_rotated"),
    }:
        pdf_folder_path = os.path.join(str(ROOT_PATH), "data\\raw", pdf_folder_name)
        pdf_file_paths = [
            os.path.join(pdf_folder_path, file)
            for file in os.listdir(pdf_folder_path)
            if file.endswith(".pdf")
        ]
        pickle_folder_path = os.path.join(
            str(ROOT_PATH), "data\\processed", pickle_file_folder_name
        )

        # multiprocessing
        args = [(file, pickle_folder_path) for file in pdf_file_paths]
        starttime = time.time()
        with mp.Pool(mp.cpu_count()) as pool:
            pool.starmap(pickle_pdf_xml, args)
        print(
            "{} Files were successfully converted to pickle files in {} seconds".format(
                len(pdf_file_paths), time.time() - starttime
            )
        )
        # time ends and delta displayed
        print("That took {} seconds".format(time.time() - starttime))

    # Add metadata and export to csv
    Index1 = get_pdf_metadata(str(ROOT_PATH), Index0)
    metadata_file_path = os.path.join(
        str(ROOT_PATH),
        "data/interim/Intermediate_Index_Files/Index_of_PDFs_for_Fall_2022_application_refresh_processed.csv",
    )
    Index1.to_csv(metadata_file_path, index=False, encoding="utf-8-sig")
