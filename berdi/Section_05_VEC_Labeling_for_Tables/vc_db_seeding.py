import sys
import pyodbc as odbc
import pandas as pd

drop_table = 0 # 0: don't drop, 2: drop table. Used for testing.

records = [
    ['Bulletproof 2', 'Movie', '2021-01-09', 2020],
    ['Street Food', 'TV Show', None, 2019]
]

DRIVER = 'SQL Server Native Client 11.0'
SERVER_NAME = 'DSQL23CAP'
DATABASE_NAME = 'DS_TEST'
TABLE_NAME = 'test_table'

conn_string = f"""
                DRIVER={{{DRIVER}}};
                SERVER={SERVER_NAME};
                DATABASE={DATABASE_NAME};
                Trusted_connection=yes;
                """

try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()
else: # executes if there are no exceptions
    cursor = conn.cursor()

create_table_statement = f"""
    CREATE TABLE {TABLE_NAME} (
         nvarchar(257),
        entertainment_type nvarchar(255),
        date date,
        year int
    );
"""
if cursor.tables(table=TABLE_NAME, tableType='TABLE').fetchone(): # Checks if table exists; if not, it creates the table. True==1, False==0. 
    print('table already exists')
else:
    print('table does not exist')
    try:
        print('creating table')
        cursor.execute(create_table_statement) # creates table
    except Exception as e:
        print(e)
        print('Error: table was not created')
        cursor.rollback()
        sys.exit()
    else:
        print('table was created')
        cursor.commit()


insert_statement = f"""
    INSERT INTO {TABLE_NAME}
    VALUES (?, ?, ?, ?)
"""

select_statement = f"""
    SELECT TOP 10 * FROM DS_TEST.dbo.{TABLE_NAME}
    """

try:
    for record in records:
        print(record)
        cursor.execute(insert_statement, record) # inserting records in database table
except Exception as e:
    cursor.rollback()
    print(e)
    print('transaction rolled')
else:
    print('records inserted')
    cursor.commit()
    df = pd.read_sql(select_statement, conn)
    print(df)
finally:
    if drop_table == 1:
        print('removing test_table')
        cursor.execute(f'DROP TABLE DS_TEST.dbo.{TABLE_NAME}')
        conn.commit()
    print('connection closed')
    conn.close()
