from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Offer(Base):
    __tablename__ = 'offer'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    clothId = Column(Integer)
    offer = Column(Float)
    buyerId = Column(Integer)
    sellerId = Column(Integer)
    statusId = Column(Integer, ForeignKey('status.id'))
    
    status = relationship("Status", back_populates="offer")
    delivery = relationship("Delivery", back_populates="offer")
