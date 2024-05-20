from sqlalchemy import Column, Table, String, Integer, Text
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.database.db import engine

Base = declarative_base()


contacts = Table(
    'contacts',
    Base.metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('surname', String),
    Column('email', String),
    Column('phone', String),
    Column('birthday', DateTime),
    Column('additional_info', Text, nullable=True),
)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False, unique=False)
    surname = Column(String(15), nullable=False, unique=False)
    email = Column(String(30), nullable=False)
    phone = Column(String(15), nullable=False)
    birthday = Column(DateTime, nullable=False, unique=False)
    additional_info = Column(Text, nullable=True, unique=False)


Base.metadata.create_all(bind=engine)