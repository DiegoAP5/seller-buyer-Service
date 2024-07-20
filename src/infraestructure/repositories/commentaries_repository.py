from sqlalchemy.orm import Session
from domain.models.commentaries import Commentaries

class CommentariesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, status: Commentaries):
        self.session.add(status)
        self.session.commit()
    
    def get_by_uuid(self, uuid: str) -> Commentaries:
        return self.session.query(Commentaries).filter_by(uuid=uuid).first()
    
    def get_all(self):
        return self.session.query(Commentaries).all()
    
    def get_all_by_seller_id(self, seller_id):
        return self.session.query(Commentaries).filter(Commentaries.sellerId == seller_id).all()
    
    def update(self, status: Commentaries):
        self.session.commit()
    
    def delete(self, uuid: str):
        status = self.get_by_uuid(uuid)
        if status:
            self.session.delete(status)
            self.session.commit()
