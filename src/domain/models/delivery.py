from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Delivery(Base):
    __tablename__ = 'delivery'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    date = Column(Date)
    clothId = Column(Integer, ForeignKey('cloth.id'))
    location = Column(String)
    buyer = Column(String)
    cellphone = Column(String)
    comments = Column(String)
    statusId = Column(Integer, ForeignKey('status.id'))
    sellerId = Column(Integer, ForeignKey('user.id'))
    buyerId = Column(Integer, ForeignKey('user.id'))
    offerId = Column(Integer, ForeignKey('offer.id'))

    cloth = relationship("Cloth", back_populates="delivery")
    status = relationship("Status", back_populates="delivery")
    seller = relationship("User", foreign_keys=[sellerId])
    buyer = relationship("User", foreign_keys=[buyerId])
    offer = relationship("Offer", back_populates="delivery")
