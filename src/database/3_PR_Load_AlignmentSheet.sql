CREATE PROC test_BERDI.PR_Load_AlignmentSheet
	@intPdgPageId INT
AS
SET XACT_ABORT ON;
BEGIN TRAN;
	INSERT INTO test_BERDI.Content (PdfPageId, Type)
	VALUES (@intPdgPageId, 'AlignmentSheet');

	INSERT INTO test_BERDI.AlignmentSheet(AlignmentSheetId, PdfPageId)
	VALUES (SCOPE_IDENTITY(), @intPdgPageId)

COMMIT TRAN;
GO
