from infraestructure.repositories.base_repository import BaseRepository
from domain.models.offer import Offer

class OfferRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
