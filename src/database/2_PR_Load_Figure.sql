CREATE PROC test_BERDI.PR_Load_Figure
	@intBlockId INT,
	@intPdfPageId INT
AS
SET XACT_ABORT ON;
BEGIN TRAN;

INSERT INTO test_BERDI.Content (PdfPageId, Type)
    VALUES (@intPdfPageId, 'Figure');

INSERT INTO test_BERDI.Figure (FigureId, BlockId, PdfPageId)
    VALUES (SCOPE_IDENTITY(), @intBlockId, @intPdfPageId);

COMMIT TRAN;
GO
