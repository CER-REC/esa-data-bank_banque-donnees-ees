USE DS_TEST
GO

DECLARE @schema_name varchar(20) 
SET @schema_name = 'Username_BERDI'

IF NOT EXISTS (SELECT name FROM sys.schemas WHERE name = @schema_name)
BEGIN
	EXEC('CREATE SCHEMA ' + @schema_name)
END


CREATE TABLE Username_BERDI.Application (
	ApplicationId int IDENTITY(1,1) PRIMARY KEY,
	InsertDateTime datetime NOT NULL DEFAULT (getdate()),
	ModifiedDateTime datetime NOT NULL DEFAULT (getdate()),
	RTSApplicationId int NOT NULL UNIQUE,
	ApplicationName varchar(200),
	ApplicationShortName varchar(100),
	ApplicationFilingDate date,
	ApplicationType varchar(100),
	ApplicationURL varchar(200),
	CompanyName varchar(200),
	Commodity varchar(50),
	DecisionURL varchar(200),
	HearingOrder varchar(200),
	PipelineLocation varchar(200),
	PipelineStatus varchar(100),
	ApplicationNameAbbrev varchar(50),
	ApplicationNameFrench varchar(200),
	ApplicationShortNameFrench varchar(100)
);

CREATE TABLE Username_BERDI.Pdf (
	PdfId int IDENTITY(1,1) PRIMARY KEY,
	ApplicationId int NOT NULL,
	InsertDateTime datetime NOT NULL DEFAULT (getdate()),
	ModifiedDateTime datetime NOT NULL DEFAULT (getdate()),
	RegdocsDataId int NOT NULL UNIQUE,
	FileName varchar(400),
	ESAFolderURL varchar(200),
	PDFDownloadURL varchar(200),
	ConsultantName varchar(200),
	ESASections varchar(max),
	ESASectionsFrench varchar(max),
	FilePath varchar(200),
	PageTextExtracted bit NOT NULL DEFAULT 0,
	RotatedPageTextExtracted bit NOT NULL DEFAULT 0,
	CamelotTableExtracted bit NOT NULL DEFAULT 0,
	BlockExtracted bit NOT NULL DEFAULT 0,
	TOCItemExtracted bit NOT NULL DEFAULT 0,
	PageMetadataExtracted bit NOT NULL DEFAULT 0,
	ContainsIK bit,
	HasGoodQualityTable bit

	CONSTRAINT [FK_Pdf_Application] FOREIGN KEY (ApplicationId) REFERENCES Username_BERDI.Application(ApplicationId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.PdfPage (
	PdfPageId int IDENTITY(1,1) PRIMARY KEY,
	PdfId int NOT NULL,
	PageNumber int NOT NULL,
	RawText varchar(max),
	CleanText varchar(max),
	RawTextRotated90 varchar(max),
	CleanTextRotated90 varchar(max)

	CONSTRAINT [FK_PdfPage_PdfPage] FOREIGN KEY (PdfId) REFERENCES Username_BERDI.Pdf(PdfId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.CamelotTable (
	CamelotTableId int IDENTITY(1,1) PRIMARY KEY,
	PdfPageId int NOT NULL,
	OrderNumber int NOT NULL,
	NumberOfRows int,
	NumberOfColumns int,
	WhitespacePercent int,
	HasContent bit,
	JsonText varchar(max)

	CONSTRAINT [FK_CamelotTable_PdfPage] FOREIGN KEY (PdfPageId) REFERENCES Username_BERDI.PdfPage(PdfPageId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.Block (
	BlockId int IDENTITY(1,1) PRIMARY KEY,
	PdfPageId int NOT NULL,
	OrderNumber int NOT NULL,
	BboxArea float NOT NULL,
	IsImage bit NOT NULL,

	CONSTRAINT [FK_Block_PdfPage] FOREIGN KEY (PdfPageId) REFERENCES Username_BERDI.PdfPage(PdfPageId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.PageMetadata (
    PageMetadataId int IDENTITY(1,1) PRIMARY KEY,
    PdfPageId int NOT NULL,
    AttributeKey varchar(800) NOT NULL,
    AttributeValue varchar(4000),
    AttributeType varchar(80) NOT NULL

    CONSTRAINT [FK_PageMetadata_PdfPage] FOREIGN KEY (PdfPageId) REFERENCES Username_BERDI.PdfPage(PdfPageId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.TOC (
	TOCId int IDENTITY(1,1) PRIMARY KEY,
	PdfPageId int NOT NULL,
	OrderNumber int NOT NULL,
	ContentType varchar(50),
	ContentTitle varchar(1000)

	CONSTRAINT [FK_TOC_PdfPage] FOREIGN KEY (PdfPageId) REFERENCES Username_BERDI.PdfPage(PdfPageId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.TOCReferredPdfPage (
    TOCId int NOT NULL,
    PdfPageId int NOT NULL

    CONSTRAINT [UC_TOC_PdfPage] UNIQUE (TOCId, PdfPageId),
    CONSTRAINT [FK_TOCReferredPdfPage_TOC] FOREIGN KEY (TOCId) REFERENCES Username_BERDI.TOC(TOCId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.TableElementGroup (
	TableElementGroupId int IDENTITY(1,1) PRIMARY KEY,
	ZipFolderName varchar(1000)
);

CREATE TABLE Username_BERDI.Content (
	ContentId int IDENTITY(1,1) PRIMARY KEY,
	PdfPageId int NOT NULL,
	Type varchar(50) NOT NULL,
	Title varchar(1000),
	FrenchTitle varchar(1000),
	ContainsIK bit

	CONSTRAINT [FK_Content_PdfPage] FOREIGN KEY (PdfPageId) REFERENCES Username_BERDI.PdfPage(PdfPageId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.TableElement (
	TableElementId int PRIMARY KEY,
	CamelotTableId int NOT NULL,
	PdfPageId int NOT NULL,
	TitleTOC varchar(1000), 
	TitleText varchar(1000), 
	FileName varchar(1000),
	FrenchFileName varchar(1000),
	IsGoodQuality bit,
	TableElementGroupId int

	CONSTRAINT [FK_TableElement_Content] FOREIGN KEY (TableElementId) REFERENCES Username_BERDI.Content(ContentId) ON DELETE CASCADE,
	CONSTRAINT [FK_TableElement_Group] FOREIGN KEY (TableElementGroupId) REFERENCES Username_BERDI.TableElementGroup(TableElementGroupId) ON DELETE SET NULL

);

CREATE TABLE Username_BERDI.Figure (
	FigureId int PRIMARY KEY,
	BlockId int NOT NULL,
	PdfPageId int NOT NULL,
	TitleTOC varchar(1000),
	TitleText varchar(1000),

	CONSTRAINT [FK_Figure_Content] FOREIGN KEY (FigureId) REFERENCES Username_BERDI.Content(ContentId) ON DELETE CASCADE

);

CREATE TABLE Username_BERDI.AlignmentSheet (
	AlignmentSheetId int PRIMARY KEY,
	PdfPageId int NOT NULL,
	Title varchar(1000),
	FigureId int

	CONSTRAINT [FK_AlignmentSheet_Content] FOREIGN KEY (AlignmentSheetId) REFERENCES Username_BERDI.Content(ContentId) ON DELETE CASCADE

);

CREATE TABLE Username_BERDI.ValueComponent (
	ValueComponentId int IDENTITY(1,1) PRIMARY KEY,
	ValueComponent varchar(200) UNIQUE
);

CREATE TABLE Username_BERDI.ContentValueComponentMapping (
	ContentId int NOT NULL,
	ValueComponentId int NOT NULL,
	FrequencyCount int DEFAULT 0

	CONSTRAINT [UC_Content_ValueComponent] UNIQUE (ContentId, ValueComponentId),
	CONSTRAINT [FK_Mapping_Content] FOREIGN KEY (ContentId) REFERENCES Username_BERDI.Content(ContentId) ON DELETE CASCADE,
	CONSTRAINT [FK_Mapping_ValueComponent] FOREIGN KEY (ValueComponentId) REFERENCES Username_BERDI.ValueComponent(ValueComponentId) ON DELETE CASCADE
);

CREATE TABLE Username_BERDI.Translation (
	EnglishExpression varchar(max),
	FrenchTranslation varchar(max)
);