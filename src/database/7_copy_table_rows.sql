-- The following sql statements enable copying 
-- the entire table (including the identity column)
-- from the source schema to the destination schema
-- [CAUTION] the destination schema records will be completely 
-- [CAUTION] replaced by the source schema

USE DS_TEST
GO

DECLARE @Source varchar(20) 
SET @Source = 'Username1_BERDI'
DECLARE @Destination varchar(20) 
SET @Destination = 'Username2_BERDI'

DECLARE @SQL_Application_DELETE VARCHAR(MAX)
DECLARE @SQL_Application_INSERT VARCHAR(MAX)
SET @SQL_Application_DELETE = CONCAT('DELETE FROM ', @Destination, '.Application')
SET @SQL_Application_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.Application ON ', 
'INSERT INTO ', @Destination, '.Application ',
'(ApplicationId, InsertDateTime, ModifiedDateTime, RTSApplicationId, ApplicationName, ApplicationShortName,
ApplicationFilingDate, ApplicationType, ApplicationURL, CompanyName, Commodity, DecisionURL,
HearingOrder, PipelineLocation, PipelineStatus, ApplicationNameAbbrev, ApplicationNameFrench, ApplicationShortNameFrench) ', 
'SELECT * FROM ', @Source, '.Application ',
'SET IDENTITY_INSERT ', @Destination, '.Application OFF')

DECLARE @SQL_Pdf_DELETE VARCHAR(MAX)
DECLARE @SQL_Pdf_INSERT VARCHAR(MAX)
SET @SQL_Pdf_DELETE = CONCAT('DELETE FROM ', @Destination, '.Pdf')
SET @SQL_Pdf_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.Pdf ON ',
'INSERT INTO ', @Destination, '.Pdf ',
'(PdfId, ApplicationId, InsertDateTime, ModifiedDateTime, RegdocsDataId, FileName, ESAFolderURL,
PDFDownloadURL, ConsultantName, ESASections, ESASectionsFrench, FilePath, PageTextExtracted,
RotatedPageTextExtracted, CamelotTableExtracted, BlockExtracted, TOCItemExtracted,
PageMetadataExtracted, ContainsIK, HasGoodQualityTable) ', 
'SELECT * FROM ', @Source, '.Pdf ',
'SET IDENTITY_INSERT ', @Destination, '.Pdf OFF')

DECLARE @SQL_PdfPage_DELETE VARCHAR(MAX)
DECLARE @SQL_PdfPage_INSERT VARCHAR(MAX)
SET @SQL_PdfPage_DELETE = CONCAT('DELETE FROM ', @Destination, '.PdfPage')
SET @SQL_PdfPage_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.PdfPage ON ', 
'INSERT INTO ', @Destination, '.PdfPage ', 
'(PdfPageId, PdfId, PageNumber, RawText, CleanText, RawTextRotated90, CleanTextRotated90) ', 
'SELECT * FROM ', @Source, '.PdfPage ',
'SET IDENTITY_INSERT ', @Destination, '.PdfPage OFF')


DECLARE @SQL_CamelotTable_DELETE VARCHAR(MAX)
DECLARE @SQL_CamelotTable_INSERT VARCHAR(MAX)
SET @SQL_CamelotTable_DELETE = CONCAT('DELETE FROM ', @Destination, '.CamelotTable')
SET @SQL_CamelotTable_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.CamelotTable ON ', 
'INSERT INTO ', @Destination, '.CamelotTable ', 
'(CamelotTableId, PdfPageId, OrderNumber, NumberOfRows, NumberOfColumns, 
WhitespacePercent, HasContent, JsonText) ', 
'SELECT * FROM ', @Source, '.CamelotTable ',
'SET IDENTITY_INSERT ', @Destination, '.CamelotTable OFF')


DECLARE @SQL_Block_DELETE VARCHAR(MAX)
DECLARE @SQL_Block_INSERT VARCHAR(MAX)
SET @SQL_Block_DELETE = CONCAT('DELETE FROM ', @Destination, '.Block')
SET @SQL_Block_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.Block ON ', 
'INSERT INTO ', @Destination, '.Block ', 
'(BlockId, PdfPageId, OrderNumber, BboxArea, IsImage) ', 
'SELECT * FROM ', @Source, '.Block ',
'SET IDENTITY_INSERT ', @Destination, '.Block OFF')


DECLARE @SQL_PageMetadata_DELETE VARCHAR(MAX)
DECLARE @SQL_PageMetadata_INSERT VARCHAR(MAX)
SET @SQL_PageMetadata_DELETE = CONCAT('DELETE FROM ', @Destination, '.PageMetadata')
SET @SQL_PageMetadata_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.PageMetadata ON ', 
'INSERT INTO ', @Destination, '.PageMetadata ', 
'(PageMetadataId, PdfPageId, AttributeKey, AttributeValue, AttributeType) ', 
'SELECT * FROM ', @Source, '.PageMetadata ',
'SET IDENTITY_INSERT ', @Destination, '.PageMetadata OFF')

DECLARE @SQL_TOC_DELETE VARCHAR(MAX)
DECLARE @SQL_TOC_INSERT VARCHAR(MAX)
SET @SQL_TOC_DELETE = CONCAT('DELETE FROM ', @Destination, '.TOC')
SET @SQL_TOC_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.TOC ON ', 
'INSERT INTO ', @Destination, '.TOC ', 
'(TOCId, PdfPageId, OrderNumber, ContentType, ContentTitle) ', 
'SELECT * FROM ', @Source, '.TOC ',
'SET IDENTITY_INSERT ', @Destination, '.TOC OFF')

DECLARE @SQL_TOCReferredPdfPage_DELETE VARCHAR(MAX)
DECLARE @SQL_TOCReferredPdfPage_INSERT VARCHAR(MAX)
SET @SQL_TOCReferredPdfPage_DELETE = CONCAT('DELETE FROM ', @Destination, '.TOCReferredPdfPage')
SET @SQL_TOCReferredPdfPage_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.TOCReferredPdfPage ', 
'(TOCId, PdfPageId) ', 
'SELECT * FROM ', @Source, '.TOCReferredPdfPage')

DECLARE @SQL_TableElementGroup_DELETE VARCHAR(MAX)
DECLARE @SQL_TableElementGroup_INSERT VARCHAR(MAX)
SET @SQL_TableElementGroup_DELETE = CONCAT('DELETE FROM ', @Destination, '.TableElementGroup')
SET @SQL_TableElementGroup_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.TableElementGroup ON ', 
'INSERT INTO ', @Destination, '.TableElementGroup ', 
'(TableElementGroupId, ZipFolderName) ', 
'SELECT * FROM ', @Source, '.TableElementGroup ',
'SET IDENTITY_INSERT ', @Destination, '.TableElementGroup OFF')

DECLARE @SQL_Content_DELETE VARCHAR(MAX)
DECLARE @SQL_Content_INSERT VARCHAR(MAX)
SET @SQL_Content_DELETE = CONCAT('DELETE FROM ', @Destination, '.Content')
SET @SQL_Content_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.Content ON ', 
'INSERT INTO ', @Destination, '.Content ', 
'(ContentId, PdfPageId, Type, Title, FrenchTitle, ContainsIK) ', 
'SELECT * FROM ', @Source, '.Content ',
'SET IDENTITY_INSERT ', @Destination, '.Content OFF')


DECLARE @SQL_TableElement_DELETE VARCHAR(MAX)
DECLARE @SQL_TableElement_INSERT VARCHAR(MAX)
SET @SQL_TableElement_DELETE = CONCAT('DELETE FROM ', @Destination, '.TableElement')
SET @SQL_TableElement_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.TableElement ', 
'(TableElementId, CamelotTableId, PdfPageId, TitleTOC, TitleText, FileName, 
FrenchFileName, IsGoodQuality, TableElementGroupId) ', 
'SELECT * FROM ', @Source, '.TableElement')


DECLARE @SQL_Figure_DELETE VARCHAR(MAX)
DECLARE @SQL_Figure_INSERT VARCHAR(MAX)
SET @SQL_Figure_DELETE = CONCAT('DELETE FROM ', @Destination, '.Figure')
SET @SQL_Figure_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.Figure ', 
'(FigureId, BlockId, PdfPageId, TitleTOC, TitleText) ', 
'SELECT * FROM ', @Source, '.Figure')

DECLARE @SQL_AlignmentSheet_DELETE VARCHAR(MAX)
DECLARE @SQL_AlignmentSheet_INSERT VARCHAR(MAX)
SET @SQL_AlignmentSheet_DELETE = CONCAT('DELETE FROM ', @Destination, '.AlignmentSheet')
SET @SQL_AlignmentSheet_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.AlignmentSheet ', 
'(AlignmentSheetId, PdfPageId, Title, FigureId) ', 
'SELECT * FROM ', @Source, '.AlignmentSheet')


DECLARE @SQL_ValueComponent_DELETE VARCHAR(MAX)
DECLARE @SQL_ValueComponent_INSERT VARCHAR(MAX)
SET @SQL_ValueComponent_DELETE = CONCAT('DELETE FROM ', @Destination, '.ValueComponent')
SET @SQL_ValueComponent_INSERT = CONCAT('SET IDENTITY_INSERT ', @Destination, '.ValueComponent ON ', 
'INSERT INTO ', @Destination, '.ValueComponent ', 
'(ValueComponentId, ValueComponent) ', 
'SELECT * FROM ', @Source, '.ValueComponent ',
'SET IDENTITY_INSERT ', @Destination, '.ValueComponent OFF')


DECLARE @SQL_ContentValueComponentMapping_DELETE VARCHAR(MAX)
DECLARE @SQL_ContentValueComponentMapping_INSERT VARCHAR(MAX)
SET @SQL_ContentValueComponentMapping_DELETE = CONCAT('DELETE FROM ', @Destination, '.ContentValueComponentMapping')
SET @SQL_ContentValueComponentMapping_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.ContentValueComponentMapping ', 
'(ContentId, ValueComponentId, FrequencyCount) ', 
'SELECT * FROM ', @Source, '.ContentValueComponentMapping')

DECLARE @SQL_Translation_DELETE VARCHAR(MAX)
DECLARE @SQL_Translation_INSERT VARCHAR(MAX)
SET @SQL_Translation_DELETE = CONCAT('DELETE FROM ', @Destination, '.Translation')
SET @SQL_Translation_INSERT = CONCAT( 
'INSERT INTO ', @Destination, '.Translation ', 
'(EnglishExpression, FrenchTranslation) ', 
'SELECT * FROM ', @Source, '.Translation')

BEGIN
EXEC(@SQL_Application_DELETE)
EXEC(@SQL_Pdf_DELETE)
EXEC(@SQL_PdfPage_DELETE)
EXEC(@SQL_CamelotTable_DELETE)
EXEC(@SQL_Block_DELETE)
EXEC(@SQL_PageMetadata_DELETE)
EXEC(@SQL_TOC_DELETE)
EXEC(@SQL_TOCReferredPdfPage_DELETE)
EXEC(@SQL_TableElementGroup_DELETE)
EXEC(@SQL_Content_DELETE)
EXEC(@SQL_TableElement_DELETE)
EXEC(@SQL_Figure_DELETE)
EXEC(@SQL_AlignmentSheet_DELETE)
EXEC(@SQL_ContentValueComponentMapping_DELETE)
EXEC(@SQL_Translation_DELETE)
EXEC(@SQL_Application_INSERT)
EXEC(@SQL_Pdf_INSERT)
EXEC(@SQL_PdfPage_INSERT)
EXEC(@SQL_CamelotTable_INSERT)
EXEC(@SQL_Block_INSERT)
EXEC(@SQL_PageMetadata_INSERT)
EXEC(@SQL_TOC_INSERT)
EXEC(@SQL_TOCReferredPdfPage_INSERT)
EXEC(@SQL_TableElementGroup_INSERT)
EXEC(@SQL_Content_INSERT)
EXEC(@SQL_TableElement_INSERT)
EXEC(@SQL_Figure_INSERT)
EXEC(@SQL_AlignmentSheet_INSERT)
EXEC(@SQL_ValueComponent_INSERT)
EXEC(@SQL_ContentValueComponentMapping_INSERT)
EXEC(@SQL_Translation_INSERT)
END