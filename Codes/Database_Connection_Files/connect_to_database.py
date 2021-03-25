from dotenv import load_dotenv
from sqlalchemy import create_engine
import os


def connect_to_db():
    """
    This method creates the engine that allows a connection to the 
    database using the credentials stored in the .env file located 
    in the Database_Connection_Files folder.
    Returns
    ----------
    engine:
        Engine is the lowest level object used by SQLAlchemy. It maintains a 
        pool of connections available for use whenever the application needs 
        to talk to the database. .execute() is a convenience method that first 
        calls conn = engine.connect(close_with_result=True) and the then 
        conn.execute(). The close_with_result parameter means the connection 
        is closed automatically.
    References
    ----------
    Ref -> https://stackoverflow.com/a/42772654
    Ref -> https://docs.sqlalchemy.org/en/13/core/connections.html
    """
    load_dotenv(override=True) # load environment variables from .env file
    host = os.getenv("DB_HOST") # hostname
    database = os.getenv("DB_DATABASE") # connection name
    user = os.getenv("DB_USER") # username
    password = os.getenv("DB_PASS")
    engine_string = f"mysql+mysqldb://{user}:{password}@{host}/{database}?charset=utf8mb4"
    # print(engine_string) # check the .env is loaded and working.
    engine = create_engine(engine_string) # connect to server
    return engine
