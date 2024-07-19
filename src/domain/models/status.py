from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Status(Base):
    __tablename__ = 'status'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    name = Column(String)
    description = Column(String)

    delivery = relationship("Delivery", back_populates="status")
    offer = relationship("Offer", back_populates="status")
