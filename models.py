
from sqlalchemy import Column, Integer, String 
from database import Base 



class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, unique=True, nullable=True)
    token = Column(String(32), nullable=False, unique=True)
