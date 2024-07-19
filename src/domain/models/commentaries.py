from sqlalchemy import Column, Integer, String, Float
from uuid import uuid4
from infraestructure.db import Base

class Commentaries(Base):
    __tablename__ = 'commentaries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, nullable=False)
    sellerId = Column(Integer, nullable=False)
    comments = Column(String(255))
