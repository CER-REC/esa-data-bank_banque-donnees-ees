from enum import Enum

class PdfPageColumn(Enum):
    """ Enum for text columns in PdgPage table """
    PDF_PAGE_ID = "PdfPageId"
    PDF_ID = "PdfId"
    PAGE_NUMBER = "PageNumber"
    RAW_TEXT = "RawText"
    CLEAN_TEXT = "CleanText"
    RAW_ROTATED90_TEXT = "RawTextRotated90"
    CLEAN_ROTATED90_TEXT = "CleanTextRotated90"

class PageMetadataColumn(Enum):
    """ Enum for columns in PageMetadata table """
    PDF_PAGE_ID = "PdfPageId"
    ATTRIBUTE_KEY = "AttributeKey"
    ATTRIBUTE_VALUE = "AttributeValue"
    ATTRIBUTE_TYPE = "AttributeType"

class BlockColumn(Enum):
    """ Enum for columns in Block table """
    BLOCK_ID = "BlockId"
    PDF_PAGE_ID = "PdfPageId"
    ORDER_NUMBER = "OrderNumber"
    BBOX_AREA = "BboxArea"
    IS_IMAGE = "IsImage"

class PdfColumn(Enum):
    """ Enum for columns in Pdf table """
    PDF_ID = "PdfId"
    APPLICATION_ID = "ApplicationId"
    INSERT_DATE_TIME = "InsertDateTime"
    MODIFIED_DATE_TIME = "ModifiedDateTime"
    REGDOCS_DATA_ID = "RegdocsDataId"
    FILE_NAME = "FileName"
    ESA_FOLDER_URL = "ESAFolderURL"
    PDF_DOWNLOAD_URL = "PDFDownloadURL"
    CONSULTANT_NAME = "ConsultantName"
    ESA_SECTIONS = "ESASections"
    ESA_SECTIONS_FRENCH = "ESASectionsFrench"
    FILE_PATH = "FilePath"
    PAGE_TEXT_EXTRACTED = "PageTextExtracted"
    ROTATEDPAGETEXTEXTRACTED = "RotatedPageTextExtracted"
    CAMELOTTABLEEXTRACTED = "CamelotTableExtracted"
    BLOCKEXTRACTED = "BlockExtracted"
    TOCITEMEXTRACTED = "TOCItemExtracted"
    PAGEMETADATAEXTRACTED = "PageMetadataExtracted"
    CONTAINSIK = "ContainsIK"
    HASGOODQUALITYTABLE = "HasGoodQualityTable"
