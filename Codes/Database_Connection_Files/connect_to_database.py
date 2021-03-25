from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# Load environment variables (from .env file) for the database

def connect_to_db():
    load_dotenv(override=True) # load environment variables from .env file
    host = os.getenv("DB_HOST") # hostname
    database = os.getenv("DB_DATABASE") # connection name
    user = os.getenv("DB_USER") # username
    password = os.getenv("DB_PASS")
    engine_string = f"mysql+mysqldb://{user}:{password}@{host}/{database}?charset=utf8mb4"
    print(engine_string)
    engine = create_engine(engine_string) # connect to server
    return engine

