import os
from dotenv import load_dotenv
import sqlalchemy as sa


load_dotenv(".env", override=True)

sql_server = os.getenv("SQL_SERVER_NAME")
sql_db = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
schema = os.getenv("DATABASE_SCHEMA")

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};" +
    f"Server={sql_server};" +
    f"Database={sql_db};" +
    (f"Username={username};" if username else '') +
    (f"Password={password};" if password else '') +
    "Trusted_Connection=yes;"
)
connection_url = sa.engine.URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)

engine = sa.create_engine(connection_url, fast_executemany=True)
