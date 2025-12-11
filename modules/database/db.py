import os
from dotenv import load_dotenv
from sqlalchemy import URL, Table, Column, String, MetaData
from sqlalchemy import create_engine, insert

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
    Column('email', String),  
    Column('name', String, primary_key=True),                    
    Column('passwordhash', String),                
)
metadata_obj.create_all(engine)

def insert_user(email_user: str, name_user: str, passwordhash_user: str):
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