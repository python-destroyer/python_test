from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime

from settings import BASE_DIR

engine = create_engine('sqlite:///' + str(BASE_DIR) + '/ip_ping.db')
DBSession = sessionmaker()
session = DBSession()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    ip_address = Column(String(20), nullable=False)
    state = Column(Boolean, nullable=False)
    my_events = relationship('Event', backref='user')

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    my_type = Column(String(16), nullable=False)
    my_time = Column(DateTime(), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

Base.metadata.create_all(engine)
Base.metadata.bind = engine