from app.core.database import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = 'User'
    username = Column(String(50), primary_key=True)
    password = Column(String(100))
    privilege = Column(String(20))
