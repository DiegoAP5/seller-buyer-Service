from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def add(self, entity: T):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_uuid(self, uuid: str):
        return self.session.query(self.model).filter(self.model.uuid == uuid).first()

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, entity: T):
        self.session.commit()

    def delete(self, entity: T):
        self.session.delete(entity)
        self.session.commit()
