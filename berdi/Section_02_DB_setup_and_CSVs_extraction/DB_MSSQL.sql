USE DS_TEST;
GO

DROP TABLE IF EXISTS BERDI.toc;
DROP TABLE IF EXISTS BERDI.pages;
DROP TABLE IF EXISTS BERDI.csvs;
DROP TABLE IF EXISTS BERDI.blocks;
DROP TABLE IF EXISTS BERDI.pages_normal_txt;
DROP TABLE IF EXISTS BERDI.pages_rotated90_txt;
DROP TABLE IF EXISTS BERDI.pdfs;

DROP SCHEMA IF EXISTS BERDI;
GO
CREATE SCHEMA BERDI;
GO


CREATE TABLE BERDI.pdfs (
	pdfId					INT PRIMARY KEY,
	totalPages				INT NOT NULL,
	csvsExtracted			VARCHAR(255) DEFAULT NULL,
	xmlContent				TEXT,
	hearingOrder			TEXT,
	application_name		TEXT,
	application_title_short	TEXT,
	short_name				VARCHAR(255) DEFAULT NULL,
	commodity				TEXT,
	pagesBlocksExtracted	INT DEFAULT 0,
	folder_name				TEXT
)


CREATE TABLE BERDI.toc (
	assigned_count			INT DEFAULT NULL,
	title_type				VARCHAR(255) NOT NULL,
	titleTOC				TEXT NOT NULL,
	page_name				TEXT NOT NULL,
	toc_page_num			INT NOT NULL,
	toc_pdfId				INT NOT NULL,
	toc_title_order			INT NOT NULL,
	PRIMARY KEY (toc_page_num, toc_pdfId, toc_title_order),
	CONSTRAINT BERDI_pdf_toc FOREIGN KEY (toc_pdfId) REFERENCES BERDI.pdfs (pdfId) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BERDI.pages (
	pdfId					INT NOT NULL,
	page_num				INT NOT NULL,
	width					INT NOT NULL,
	height					INT NOT NULL,
	rotation				INT NOT NULL,
	figures					INT NOT NULL,
	num_images				INT NOT NULL,
	media_x0				INT NOT NULL,
	media_y0				INT NOT NULL,
	media_x1				INT NOT NULL,
	media_y1				INT NOT NULL,
	media_width				INT NOT NULL,
	media_height			INT NOT NULL,
	page_area				INT NOT NULL,
	PRIMARY KEY (pdfId,page_num),
	CONSTRAINT BERDI_pdf_pages FOREIGN KEY (pdfId) REFERENCES BERDI.pdfs (pdfId) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BERDI.csvs (
	csvId					VARCHAR(255) NOT NULL,
	csvFileName				VARCHAR(255) NOT NULL,
	csvFullPath				TEXT NOT NULL,
	pdfId					INT NOT NULL,
	page					INT NOT NULL,
	tableNumber				INT NOT NULL,
	topRowJson				TEXT NOT NULL,  -- it is json type in mysql
	titleTag				TEXT,
	titleTOC				TEXT,
	titleFinal				TEXT,
	csvRows					INT NOT NULL,
	csvColumns				INT NOT NULL,
	method					VARCHAR(255) NOT NULL,
	accuracy				FLOAT NOT NULL,
	whitespace				FLOAT NOT NULL,
	csvText					TEXT NOT NULL,  -- it is json type in mysql
	dt_created				DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	hasContent				TINYINT DEFAULT NULL,
	PRIMARY KEY (csvId),
	CONSTRAINT BERDI_pdf_csvs FOREIGN KEY (pdfId) REFERENCES BERDI.pdfs (pdfId) ON DELETE CASCADE ON UPDATE CASCADE
) ;


CREATE TABLE BERDI.blocks (
	pdfId					INT NOT NULL,
	page_num				INT NOT NULL,
	block_order				INT NOT NULL,
	type					INT NOT NULL,
	block_width				INT DEFAULT NULL,
	block_height			INT DEFAULT NULL,
	bbox_x0					FLOAT NOT NULL,
	bbox_y0					FLOAT NOT NULL,
	bbox_x1					FLOAT NOT NULL,
	bbox_y1					FLOAT NOT NULL,
	ext						TEXT,
	color					INT DEFAULT NULL,
	xres					INT DEFAULT NULL,
	yres					INT DEFAULT NULL,
	bpc						INT DEFAULT NULL,
	block_area				INT DEFAULT NULL,
	bbox_width				FLOAT NOT NULL,
	bbox_height				FLOAT NOT NULL,
	bbox_area				FLOAT NOT NULL,
	bbox_area_image			FLOAT NOT NULL,
	titleTOC				TEXT,
	page_name				TEXT,
	titleTag				TEXT,
	titleFinal				TEXT,
	PRIMARY KEY (pdfId,page_num,block_order),
	CONSTRAINT BERDI_pdfId_and_page FOREIGN KEY (pdfId, page_num) REFERENCES BERDI.pages (pdfId, page_num) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BERDI.pages_normal_txt (
	pdfId					INT NOT NULL,
	page_num				INT NOT NULL,
	content					TEXT,
	clean_content			TEXT,
	PRIMARY KEY (pdfId, page_num),
	CONSTRAINT BERDI_pdf_pages_normal_txt FOREIGN KEY (pdfId) REFERENCES BERDI.pdfs (pdfId) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BERDI.pages_rotated90_txt (
	pdfId					INT NOT NULL,
	page_num				INT NOT NULL,
	content					TEXT,
	clean_content			TEXT,
	PRIMARY KEY (pdfId, page_num),
	CONSTRAINT BERDI_pdf_pages_rotated90_txt FOREIGN KEY (pdfId) REFERENCES BERDI.pdfs (pdfId) ON DELETE CASCADE ON UPDATE CASCADE
);
