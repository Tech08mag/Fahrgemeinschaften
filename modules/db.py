import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, URL, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

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
    startpoint: Column[str] = Column(String)
    destination: Column[str] = Column(String)
    osmlink: Column[str] = Column(String)

    def __repr__(self):
        return f"<User(id_drive='{self.id_drive}', organizer='{self.organizer}', date='{self.date}', time='{self.time}', price='{self.price}', seat_number='{self.seat_amount}', startpoint='{self.startpoint}', destination='{self.destination}', orm_link='{self.osmlink}'>"

class Passenger(Base):
    __tablename__ = 'passenger'
    drive_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    passenger_name: Mapped[str] = mapped_column(String, primary_key=True)

    def __repr__(self):
        return f"<User(drive_id='{self.drive_id}', passenger_name='{self.passenger_name}'>"

engine = create_engine(url_object, echo=True)
Base.metadata.create_all(engine)
Session: sessionmaker[engine] = sessionmaker(bind=engine)