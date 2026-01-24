import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, URL, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD"),
    host=os.getenv("PG_HOST", "postgres"),
    database=os.getenv("PG_DATABASE"),
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Column[str] = Column(String, unique=True)
    email: Column[str] = Column(String, unique=True)
    password_hash: Column[str] = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', password_hash='{self.password_hash}'>"

class Drive(Base):
    __tablename__ = 'drive'
    id_drive: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    organizer: Column[str] = Column(String)
    date: Column[str] = Column(String)
    time: Column[str] = Column(String)
    price: Column[float] = Column(DECIMAL)
    seat_amount: Column[int] = Column(Integer)

    start_street: Column[str] = Column(String)
    start_house_number: Column[int] = Column(Integer)
    start_postal_code: Column[int] = Column(Integer)
    start_place: Column[str] = Column(String)

    end_street: Column[str] = Column(String)
    end_house_number: Column[int] = Column(Integer)
    end_postal_code: Column[int] = Column(Integer)
    end_place: Column[str] = Column(String)

    def __repr__(self):
        return f"<Drive(id_drive='{self.id_drive}', organizer='{self.organizer}', date='{self.date}', time='{self.time}', price='{self.price}', seat_amount='{self.seat_amount}', start_street='{self.start_street}', start_house_number='{self.start_house_number}', start_postal_code='{self.start_postal_code}', start_place='{self.start_place}', end_street='{self.end_street}', end_house_number='{self.end_house_number}', end_postal_code='{self.end_postal_code}', end_place='{self.end_place}''>"

class Passenger(Base):
    __tablename__ = 'passenger'
    drive_id: Column[int] = Column(Integer, primary_key=True)
    passenger_name: Column[str] = Column(String, primary_key=True)

    def __repr__(self):
        return f"<User(drive_id='{self.drive_id}', passenger_name='{self.passenger_name}'>"

engine = create_engine(url_object, echo=True)
Base.metadata.create_all(engine)
Session: sessionmaker[engine] = sessionmaker(bind=engine)