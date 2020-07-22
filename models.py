from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

Base = declarative_base()


class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    good = Column(String)
    good_description = Column(String)
    measure = Column(String)
    price = Column(Float)
    quantity = Column(Float)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user = Column(Integer)
    good = Column(String)
    quantity = Column(Float)
    sum = Column(Float)
