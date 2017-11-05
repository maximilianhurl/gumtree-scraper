from sqlalchemy import DateTime, Column, Numeric, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Listing(Base):

    __tablename__ = 'users'
    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric)
    location = Column(String)
    posted_date = Column(DateTime)
    contact_name = Column(String)
    contact_number = Column(String)
    contact_email = Column(String)

    def __repr__(self):
        return f"<User(title='{self.title}', price='{self.price}')>"
