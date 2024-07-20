from sqlalchemy.orm import Session
from domain.models.delivery import Delivery

class DeliveryRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, status: Delivery):
        self.session.add(status)
        self.session.commit()
    
    def get_by_uuid(self, uuid: str) -> Delivery:
        return self.session.query(Delivery).filter_by(uuid=uuid).first()
    
    def get_all(self):
        return self.session.query(Delivery).all()
    
    def get_all_delivery_by_seller(self, seller_id):
        return self.session.query(Delivery).filter(Delivery.sellerId == seller_id).all()
    
    def get_all_delivery_by_seller_and_status(self, seller_id, status_id):
        return self.session.query(Delivery).filter(Delivery.sellerId == seller_id, Delivery.statusId == status_id).all()
    
    def get_all_delivery_by_buyer(self, buyer_id):
        return self.session.query(Delivery).filter(Delivery.buyerId == buyer_id).all()
    
    def get_all_delivery_by_buyer_and_status(self, buyer_id,status_id):
        return self.session.query(Delivery).filter(Delivery.buyerId == buyer_id, Delivery.statusId == status_id).all()
    
    def update(self, status: Delivery):
        self.session.commit()
    
    def delete(self, uuid: str):
        status = self.get_by_uuid(uuid)
        if status:
            self.session.delete(status)
            self.session.commit()
