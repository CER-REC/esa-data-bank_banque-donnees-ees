from collections import defaultdict
import pandas as pd
from src.util.database_connection import engine, schema
from src.functions.extract_page_metadata.upsert_metadata import upsert_metadata
from src.functions.extract_page_metadata.models import PageMetadataColumn, BlockColumn, PdfPageColumn, PdfColumn
from src.functions.extract_page_metadata.metadata import PageMetadataAttribute
from src.util.attribute_types import AttributeType
from src.util.exception_and_logging.handle_exception import ExceptionHandler

def count_words(words, choices):
    """
        This function counts the number of words matches exactly inside the 
        set of words given in the choice list

        Parameters
        --------------
        words (list[string]): list of words as string
        choices (list[string]): list of words as string

        Returns:
        -------------
        number of words matching word supplied in choice
    """
    counter = 0
    for word in words:
        if word.strip().lower() in choices:
            counter += 1
    return counter

def add_metadata(dt_metadata, page_id, metadata_name, metadata_value, metadata_type):
    """
        This function updates the dictionary containing all features

        Parameters
        --------------
        dt_metadata (dictionary): dictionary of features, keys are as follows
            PdfPageId (list[string])
            AttributeKey (list[string])
            AttributeValue (list[string])
            AttributeType (list[string])
        page_id (string): id of the page
        metadata_name (string): name of the feature to be updated
        metadata_value: value of the feature to be updated
        metadata_type: attribute type of the feature (i.e., FLOAT, INTEGER, STRING, BOOLEAN)

        Returns:
        -------------
        None
    """
    dt_metadata[PageMetadataColumn.PDF_PAGE_ID.value].append(page_id)
    dt_metadata[PageMetadataColumn.ATTRIBUTE_KEY.value].append(metadata_name)
    dt_metadata[PageMetadataColumn.ATTRIBUTE_VALUE.value].append(str(metadata_value))
    dt_metadata[PageMetadataColumn.ATTRIBUTE_TYPE.value].append(metadata_type)

def extract_page_metadata(pdf_id):
    """
        This function extracts metadata for all the pages from a pdf document.
    """
    with ExceptionHandler("Error querying Blocks for page metadata calculation"), engine.begin() as conn:

        # mapping between PdfPageId and PageNumber
        # need this information to extract PdfPageId from PageNumber for a given pdf with a PdfId
        query = f"""
                    SELECT PdfPage.{PdfPageColumn.PDF_PAGE_ID.value}, 
                        Block.{BlockColumn.BBOX_AREA.value}, 
                        Block.{BlockColumn.IS_IMAGE.value}, 
                        PdfPage.{PdfPageColumn.RAW_TEXT.value}
                    FROM {schema}.PdfPage AS PdfPage
                        LEFT JOIN {schema}.Block AS Block
                            ON Block.{BlockColumn.PDF_PAGE_ID.value} = PdfPage.{PdfPageColumn.PDF_PAGE_ID.value}
                    WHERE PdfPage.{PdfPageColumn.PDF_ID.value} = {pdf_id};
                """
        df_blocks = pd.read_sql(query, con=conn)

    # list of unique page_id values from the block table
    page_ids = df_blocks[PdfPageColumn.PDF_PAGE_ID.value].unique()

    # initialize metadata dictionary
    # keys are as follows:
    #   PdfPageId, AttributeKey, AttributeValue, and AttributeType
    dt_metadata = defaultdict(list)

    for page_id in page_ids:

        # extract block with current page_id
        df_current_block = df_blocks[df_blocks.PdfPageId == page_id]

        no_of_images = df_current_block[df_current_block.IsImage.notna() & df_current_block.IsImage].PdfPageId.count()
        # metadata 1: number of images in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.NO_OF_IMAGES.value,
                        no_of_images,
                        AttributeType.INTEGER.value)

        area_of_images = df_current_block[df_current_block.IsImage.notna() & df_current_block.IsImage].BboxArea.sum()
        # metadata 2: area occupied by images in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.AREA_OF_IMAGES.value,
                        area_of_images,
                        AttributeType.FLOAT.value)

        content = df_current_block[PdfPageColumn.RAW_TEXT.value].values[0]
        word_list = content.split()

        words_in_page = len(word_list)
        # metadata 3: number of words in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORDS_IN_PAGE.value,
                        words_in_page,
                        AttributeType.INTEGER.value)

        word_count_scale = count_words(word_list, ["scale"])
        sc_grp = 1 if word_count_scale > 0 else 0
        # metadata 4: number of times the word - "scale" appears in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_SCALE.value,
                        word_count_scale,
                        AttributeType.INTEGER.value)
        # metadata 5: whether the page is part of the scale group
        # a page is part of the scale group if the word - "scale"
        # appears at least one in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.IN_SCALE_GROUP.value,
                        sc_grp,
                        AttributeType.INTEGER.value)

        word_count_km_kilometers = count_words(word_list, ["kilometre", "kilometer", "km", "kilometres", "kilometers"])
        # metadata 6: number of times the word - (kilometre/kilometer/km)
        # appears in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_KM.value,
                        word_count_km_kilometers,
                        AttributeType.INTEGER.value)

        word_count_m = count_words(word_list, ["m"])
        # metadata 7: number of times the word - "m"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_M.value,
                        word_count_m,
                        AttributeType.INTEGER.value)

        word_count_meter = count_words(word_list, ["meter", "metre", "meters", "metres"])
        # metadata 8: number of times the word - "meter"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_METER.value,
                        word_count_meter,
                        AttributeType.INTEGER.value)

        word_count_legend = count_words(word_list, ["legend", "legends"])
        # metadata 9: number of times the word - "legend"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_LEGEND.value,
                        word_count_legend,
                        AttributeType.INTEGER.value)

        word_count_figure = count_words(word_list, ["figure", "figures"])
        fig_grp = 1 if word_count_figure > 0 else 0
        # metadata 10: number of times the word - "figure"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_FIGURE.value,
                        word_count_figure,
                        AttributeType.INTEGER.value)
        # metadata 11: whether the page is part of the figure group
        # a page is part of the scale group if the word - "figure"
        # appears at least one in the page
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.IN_FIGURE_GROUP.value,
                        fig_grp,
                        AttributeType.INTEGER.value)

        word_count_map = count_words(word_list, ["map", "maps"])
        # metadata 12: number of times the word - "map"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_MAP.value,
                        word_count_map,
                        AttributeType.INTEGER.value)

        word_count_alignment_sheet = count_words(word_list, ["alignment sheet", "alignment sheets"])
        # metadata 13: number of times the word - "alignment sheet"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_ALIGNMENT_SHEET.value,
                        word_count_alignment_sheet,
                        AttributeType.INTEGER.value)

        word_count_sheet = count_words(word_list, ["sheet", "sheets"])
        # metadata 14: number of times the word - "sheet"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_SHEET.value,
                        word_count_sheet,
                        AttributeType.INTEGER.value)

        word_count_north = count_words(word_list, ["north"])
        # metadata 15: number of times the word - "north"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_NORTH.value,
                        word_count_north,
                        AttributeType.INTEGER.value)

        word_count_n = count_words(word_list, ["n"])
        # metadata 16: number of times the word - "n"
        add_metadata(dt_metadata,
                        page_id,
                        PageMetadataAttribute.WORD_COUNT_N.value,
                        word_count_n,
                        AttributeType.INTEGER.value)

    if not dt_metadata:
        # update PageMetadataExtracted to 1 after page metadata extraction, even though no page metadata found
        with ExceptionHandler(f"Error updating PageMetadataExtracted column in Pdf table for PdfId - {pdf_id}"), \
                engine.begin() as db_con:
            db_con.exec_driver_sql(f""" UPDATE {schema}.Pdf SET {PdfColumn.PAGEMETADATAEXTRACTED.value} = 1
                                    WHERE {PdfColumn.PDF_ID.value} = {pdf_id};""")

    upsert_metadata(pdf_id, dt_metadata)
