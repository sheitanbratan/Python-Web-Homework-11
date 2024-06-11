from sqlalchemy import Column, Table, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
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
    user_id = Column('user_id',
                     ForeignKey('users.id', ondelete='CASCADE'),
                     default=None)
    user = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)

    def __str__(self):
        return f'{self.id}, {self.username}, {self.email}'


Base.metadata.create_all(bind=engine)