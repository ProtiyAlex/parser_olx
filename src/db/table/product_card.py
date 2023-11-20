from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime as dt
from db.dbcore import Base


class ProductCard(Base):
    __tablename__ = 'product_card'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    img_link = Column(String)
    location = Column(String)
    data = Column(DateTime)
    link = Column(String)
    description = Column(String)


