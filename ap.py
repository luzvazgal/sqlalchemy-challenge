#This file has the code to create a new databse model 
#using Station and Measurement models
#Code example taken from https://hackersandslackers.com/sqlalchemy-data-models/

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

Base = declarative_base()

class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True, nullable=False)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

    def __repr__(self):
        return '<Station model {}>'.format(self.id)


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True, nullable=False)
    station = Column(String)
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Float)

    def __repr__(self):
        return '<Measurement model {}>'.format(self.id)





# Create engine
#db_uri = environ.get('sqlite:///Resources/hawaii_new_model.sqlite')
engine = create_engine('sqlite:///Resources/hawaii_new_model.sqlite')

# Create All Tables
Base.metadata.create_all(engine)

