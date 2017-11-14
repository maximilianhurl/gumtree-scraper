from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Advert(Base):

    __tablename__ = 'advert'

    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric)
    location = Column(String)
    posted_date = Column(DateTime)
    url = Column(String)
    processed = Column(Boolean)

    def __repr__(self):
        return f"<Advert(title='{self.title}', price='{self.price}')>"
