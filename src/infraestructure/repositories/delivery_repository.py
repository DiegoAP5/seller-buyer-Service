from infraestructure.repositories.base_repository import BaseRepository
from domain.models.delivery import Delivery

class DeliveryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
