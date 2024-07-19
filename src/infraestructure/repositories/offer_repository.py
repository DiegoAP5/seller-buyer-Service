from sqlalchemy.orm import Session
from domain.models.offer import Offer

class OfferRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, status: Offer):
        self.session.add(status)
        self.session.commit()
    
    def get_by_uuid(self, uuid: str) -> Offer:
        return self.session.query(Offer).filter_by(uuid=uuid).first()
    
    def get_all(self):
        return self.session.query(Offer).all()
    
    def update(self, status: Offer):
        self.session.commit()
    
    def delete(self, uuid: str):
        status = self.get_by_uuid(uuid)
        if status:
            self.session.delete(status)
            self.session.commit()
