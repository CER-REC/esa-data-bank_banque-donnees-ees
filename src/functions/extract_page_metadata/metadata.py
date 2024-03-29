from enum import Enum

class PageMetadataAttribute(Enum):
    """ Enum for columns in PageMetadata attributes """
    NO_OF_IMAGES = "no_of_images"
    AREA_OF_IMAGES = "area_of_images"
    WORDS_IN_PAGE = "words_in_page"
    WORD_COUNT_SCALE = "word_count_scale"
    IN_SCALE_GROUP = "in_scale_group"
    WORD_COUNT_KM = "word_count_km"
    WORD_COUNT_M = "word_count_m"
    WORD_COUNT_METER = "word_count_meter"
    WORD_COUNT_LEGEND = "word_count_legend"
    WORD_COUNT_FIGURE = "word_count_figure"
    IN_FIGURE_GROUP = "in_figure_group"
    WORD_COUNT_MAP = "word_count_map"
    WORD_COUNT_ALIGNMENT_SHEET = "word_count_alignment_sheet"
    WORD_COUNT_SHEET = "word_count_sheet"
    WORD_COUNT_NORTH = "word_count_north"
    WORD_COUNT_N = "word_count_n"
