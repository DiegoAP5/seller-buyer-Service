from infraestructure.repositories.offer_repository import OfferRepository
from infraestructure.repositories.delivery_repository import DeliveryRepository
from domain.models.offer import Offer
from domain.models.delivery import Delivery
import uuid
from datetime import datetime

class OfferController:
    def __init__(self, offer_repo: OfferRepository, delivery_repo: DeliveryRepository):
        self.offer_repo = offer_repo
        self.delivery_repo = delivery_repo

    def create_offer(self, offer_data):
        new_offer = Offer(**offer_data, uuid=str(uuid.uuid4()))
        return self.offer_repo.create(new_offer)

    def get_offers(self):
        return self.offer_repo.get_all()

    def get_offer_by_id(self, offer_id):
        return self.offer_repo.get_by_id(offer_id)

    def update_offer(self, offer_id, offer_data):
        offer = self.offer_repo.get_by_id(offer_id)
        if offer:
            for key, value in offer_data.items():
                setattr(offer, key, value)
            self.offer_repo.update(offer)
            if offer_data.get('statusId') == 2:  # Assuming 2 is the status that triggers delivery creation
                delivery_data = {
                    'uuid': str(uuid.uuid4()),
                    'date': datetime.now(),
                    'clothId': offer.clothId,
                    'location': 'Default Location',
                    'buyer': 'Default Buyer',
                    'cellphone': '0000000000',
                    'comments': '',
                    'statusId': offer_data.get('statusId'),
                    'sellerId': offer.sellerId,
                    'buyerId': offer.buyerId,
                    'offerId': offer.id
                }
                new_delivery = Delivery(**delivery_data)
                self.delivery_repo.create(new_delivery)
            return offer
        return None

    def delete_offer(self, offer_id):
        offer = self.offer_repo.get_by_id(offer_id)
        if offer:
            self.offer_repo.delete(offer)
            return offer
        return None
