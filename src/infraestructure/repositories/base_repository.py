from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, entity_class, entity_id):
        return self.session.query(entity_class).filter(entity_class.id == entity_id).first()

    def get_by_uuid(self, entity_class, entity_uuid):
        return self.session.query(entity_class).filter(entity_class.uuid == entity_uuid).first()

    def get_all(self, entity_class):
        return self.session.query(entity_class).all()

    def update(self, entity):
        self.session.commit()

    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()
