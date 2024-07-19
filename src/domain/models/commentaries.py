from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from uuid import uuid4
from infraestructure.db import Base

class Commentaries(Base):
    __tablename__ = 'commentaries'
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True, index=True)
    clothId = Column(Integer, ForeignKey('cloth.id'))
    offer = Column(Float)
    buyerId = Column(Integer, ForeignKey('user.id'))
    sellerId = Column(Integer, ForeignKey('user.id'))

    cloth = relationship("Cloth", back_populates="commentaries")
    buyer = relationship("User", foreign_keys=[buyerId])
    seller = relationship("User", foreign_keys=[sellerId])
