from sqlalchemy import Column, Integer, String
from database.connection import Base


class UserTable(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    password = Column(String, nullable=False)
    home_address = Column(String, nullable=True)
    office_address = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
