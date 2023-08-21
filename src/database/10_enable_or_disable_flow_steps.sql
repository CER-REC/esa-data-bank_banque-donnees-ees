-- update 0/1 based on whether to run the step
-- specify application id
UPDATE Pdf
SET Pdf.PageTextExtracted = 0,
	Pdf.RotatedPageTextExtracted = 0,
	Pdf.CamelotTableExtracted = 0,
	Pdf.BlockExtracted = 0, 
	Pdf.TOCItemExtracted = 0,
	Pdf.PageMetadataExtracted = 0
FROM Username_BERDI.Pdf Pdf
INNER JOIN Username_BERDI.Application App ON Pdf.ApplicationId = App.ApplicationId
AND App.ApplicationId = 1; 