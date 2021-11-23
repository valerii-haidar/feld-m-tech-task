'''Describes a DB structure'''
from sqlalchemy import (
    Column, Integer, Text,
    ForeignKey, DateTime, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    '''Describes Transaction db table'''
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    visitor_id = Column(Integer)
    device_type = Column(Integer, ForeignKey('devices.id'))
    revenue = Column(Float)
    tax = Column(Float)


class Device(Base):
    '''Describes Device db table'''
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    device_name = Column(Text)
    transactions = relationship(
        'Transaction', backref='device'
    )
