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

    def get_offer_by_seller(self, seller_id):
        return self.session.query(Offer).filter(Offer.sellerId==seller_id).all()
    
    def get_offer_by_buyer(self, buyer_id):
        return self.session.query(Offer).filter(Offer.buyerId==buyer_id).all()
    
    def get_offer_by_seller_and_status(self, seller_id, status_id):
        return self.session.query(Offer).filter(Offer.sellerId==seller_id, Offer.statusId == status_id).all()
    
    def get_offer_by_buyer_and_status(self, buyer_id, status_id):
        return self.session.query(Offer).filter(Offer.buyerId==buyer_id, Offer.statusId == status_id).all()