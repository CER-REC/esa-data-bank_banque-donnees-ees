from dotenv import load_dotenv
import pyodbc
import os

def connect_to_db():
    load_dotenv(override=True)  # load environment variables from .env file
    sql_server = os.getenv('SQL_SERVER')
    sql_db = os.getenv('SQL_DATABASE')

    connection = pyodbc.connect('Driver={SQL Server Native Client 11.0};' +
                        'Server={};'.format(sql_server) + 
                        'Database={};'.format(sql_db) +
                        'Trusted_Connection=yes;')
    return connection
