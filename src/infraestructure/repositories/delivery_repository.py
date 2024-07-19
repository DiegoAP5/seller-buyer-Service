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
    
    def update(self, status: Delivery):
        self.session.commit()
    
    def delete(self, uuid: str):
        status = self.get_by_uuid(uuid)
        if status:
            self.session.delete(status)
            self.session.commit()
