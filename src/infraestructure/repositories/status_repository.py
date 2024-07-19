from infraestructure.repositories.base_repository import BaseRepository
from domain.models.status import Status

class StatusRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
