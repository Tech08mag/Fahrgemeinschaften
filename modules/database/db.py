import os
import time
from dotenv import load_dotenv
from sqlalchemy import URL, Table, Column, String, MetaData, UUID
from sqlalchemy import create_engine, insert
from sqlalchemy.exc import OperationalError

load_dotenv()

url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST", "postgres"),  # Default to 'postgres' for Docker
    database=os.getenv("PG_DATABASE"),
)

engine = create_engine(url_object, echo=False)

metadata_obj = MetaData()
Users = Table(
    'Users',                                        
    metadata_obj,                                    
    Column('email', String, primary_key=True),  
    Column('name', String),                    
    Column('passwordhash', String),
    Column("Settings", UUID)             
)

def wait_for_db(retries: int = 30, delay: int = 2):
    """Wait for database to be ready before proceeding."""
    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                print("✓ Database connection successful")
                return True
        except OperationalError:
            if attempt < retries - 1:
                print(f"⏳ Waiting for database... (attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                print("✗ Failed to connect to database after retries")
                raise

def init_db():
    """Initialize database tables after connection is established."""
    metadata_obj.create_all(engine)

def insert_user_data(email_user: str, name_user: str, passwordhash_user: str):
    statement1 = insert(Users).values(email = email_user,
                                       name=name_user,
                                       passwordhash = passwordhash_user)
    with engine.connect() as connection:
        connection.execute(statement1)
        connection.commit()

def get_hashed_password_by_email(email_input: str):
     with engine.connect() as connection:
        query = Users.select().where(Users.columns.email == email_input)
        output = connection.execute(query)
        return output.fetchone()