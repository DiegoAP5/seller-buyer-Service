from infraestructure.repositories.base_repository import BaseRepository
from domain.models.commentaries import Commentaries

class CommentariesRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
