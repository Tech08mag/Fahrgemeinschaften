import os
from dotenv import load_dotenv
from sqlalchemy import URL, Table, Column, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine import result

load_dotenv()

url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_DATABASE"),
)

engine = create_engine(url_object, echo=True)

metadata_obj = MetaData()
Users = Table(
    'Users',                                        
    metadata_obj,                                    
    Column('email', String, primary_key=True),  
    Column('name', String, primary_key=True),                    
    Column('passwordhash', String),                
)
metadata_obj.create_all(engine)

def insert_user(email_user: str, name_user: str, passwordhash_user: str):
    statement1 = Users.insert().values(email = email_user,
                                       name=name_user,
                                       passwordhash = passwordhash_user)
    engine.execute(statement1) # pyright: ignore[reportAttributeAccessIssue]