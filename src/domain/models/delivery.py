from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Delivery(Base):
    __tablename__ = 'delivery'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    date = Column(Date)
    clothId = Column(Integer)
    location = Column(String(255))
    cellphone = Column(String(255))
    comments = Column(String(255))
    statusId = Column(Integer, ForeignKey('status.id'))
    sellerId = Column(Integer)
    buyerId = Column(Integer)
    offerId = Column(Integer, ForeignKey('offer.id'))

    status = relationship("Status", back_populates="delivery")
    offer = relationship("Offer", back_populates="delivery")
