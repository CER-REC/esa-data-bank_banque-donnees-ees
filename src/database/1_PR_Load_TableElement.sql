CREATE PROC test_BERDI.PR_Load_TableElement
    @intCamelotTableId INT,
    @intPdfPageId INT
AS
SET XACT_ABORT ON;
BEGIN TRAN;

INSERT INTO test_BERDI.Content (PdfPageId, Type)
       VALUES (@intPdfPageId, 'TableElement');

INSERT INTO test_BERDI.TableElement (TableElementId, CamelotTableId, PdfPageId)
       VALUES (SCOPE_IDENTITY(), @intCamelotTableId, @intPdfPageId);

COMMIT TRAN;
GO
