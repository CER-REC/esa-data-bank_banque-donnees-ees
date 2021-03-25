import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))
from Database_Connection_Files.connect_to_database import connect_to_db
from sqlalchemy import text
import pandas as pd
import os

# engine = connect_to_db()

# stmt = text("SELECT pdfId, totalPages FROM pdfs ORDER BY totalPages DESC;")
# with engine.connect() as conn:
#     df = pd.read_sql(stmt, conn)
#     print(df.head())

print(Path(os.getenv("PDFS_FILEPATH")))