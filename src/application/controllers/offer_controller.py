from marshmallow import ValidationError
from domain.models.offer import Offer
from infraestructure.repositories.offer_repository import OfferRepository
from infraestructure.db import SessionLocal
from application.services.rabbit import RabbitClient
from application.schemas.offer_schema import OfferSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
from application.controllers.delivery_controller import DeliveryController
import pika
import json
from infraestructure.db import SessionLocalUser

def get_rabbitmq_connection():
        credentials = pika.PlainCredentials('diego', 'Diegoespro01')
        parameters = pika.ConnectionParameters(
            host='35.168.45.250', 
            port=5672, 
            virtual_host='/', 
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        return connection

def send_message_to_queue(queue_name, message):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()
    
    
def get_cloth_data(cloth_id):
    rabbit_client = RabbitClient()
    message = {"cloth_id": cloth_id}
    response = rabbit_client.call('cloth_request_queue', message)
    rabbit_client.close()
    return response

class OfferController:
    def __init__(self):
        self.session = SessionLocal()
        self.rabbit = RabbitClient()
        self.session_user = SessionLocalUser()
        self.repo = OfferRepository(self.session, self.session_user)
        self.schema = OfferSchema()
        self.delivery_controller = DeliveryController() 

    def create_offer(self, data):
        try:
            validated_data = self.schema.load(data)
            new_offer = Offer(**validated_data)
            self.repo.add(new_offer)
            return BaseResponse(self.to_dict(new_offer), "Offer created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_offer(self, uuid, data):
        offer = self.repo.get_by_uuid(uuid)
        if offer:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(offer, key, value)
                self.repo.update(offer)
                new_status_id = data.get('statusId', offer.statusId)
                if new_status_id == 2:
                    user = self.repo.get_user_by_id(offer.sellerId)
                    message = {'ropa_id': offer.clothId}
                    send_message_to_queue('status_update_queue', message)
                    delivery_data = {
                        'clothId': offer.clothId,
                        'buyerId': offer.buyerId,
                        'sellerId': offer.sellerId,
                        'offerId': offer.id,
                        'date': '2024-07-31',
                        'statusId': 1,
                        'location': 'Parque central',
                        'cellphone': user.cellphone,
                        'comments': 'Entrega a tiempo',
                    }
                    self.delivery_controller.create_delivery(delivery_data)
                return BaseResponse(self.to_dict(offer), "Offer updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def get_offer(self, uuid):
        offer = self.repo.get_by_uuid(uuid)
        if offer:
            return BaseResponse(self.to_dict(offer), "Offer fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def delete_offer(self, uuid):
        offer = self.repo.get_by_uuid(uuid)
        if offer:
            self.repo.delete(offer)
            return BaseResponse(None, "Offer deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def list_offers(self):
        offers = self.repo.get_all()
        return BaseResponse([self.to_dict(offer) for offer in offers], "Offers fetched successfully", True, HTTPStatus.OK)

    def list_offers_by_seller(self, seller_id):
        offers = self.repo.get_offer_by_seller(seller_id)
        offers_data = []
        for offer in offers:
            user_id = offer.buyerId
            user = self.repo.get_user_by_id(user_id)
            cloth_data = get_cloth_data(offer.clothId)
            offers_data.append({
                "offer": self.to_dict(offer),
                "cloth": cloth_data,
                'user': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'cellphone': user.cellphone
                        }
            })
        return BaseResponse(offers_data, "Offers fetched successfully", True, HTTPStatus.OK)
    
    def list_offers_by_buyer(self, buyer_id):
        print(buyer_id)
        offers = self.repo.get_offer_by_buyer(buyer_id)
        offers_data = []
        for offer in offers:
            user_id = offer.sellerId
            user = self.repo.get_user_by_id(user_id)
            cloth_data = get_cloth_data(offer.clothId)
            offers_data.append({
                "offer": self.to_dict(offer),
                "cloth": cloth_data,
                'user': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'cellphone': user.cellphone
                        }
            })
        return BaseResponse(offers_data, "Offers fetched successfully", True, HTTPStatus.OK)

    def list_offers_by_seller_and_status(self, seller_id, status_id):
        offers = self.repo.get_offer_by_seller_and_status(seller_id, status_id)
        offers_data = []
        for offer in offers:
            user_id = offer.buyerId
            user = self.repo.get_user_by_id(user_id)
            cloth_data = get_cloth_data(offer.clothId)
            offers_data.append({
                "offer": self.to_dict(offer),
                "cloth": cloth_data,
                'user': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'cellphone': user.cellphone
                        }
            })
        return BaseResponse(offers_data, "Offers fetched successfully", True, HTTPStatus.OK)
    
    def list_offers_by_buyer_and_status(self, buyer_id, status_id):
        offers = self.repo.get_offer_by_buyer_and_status(buyer_id, status_id)
        offers_data = []
        for offer in offers:
            user_id = offer.sellerId
            user = self.repo.get_user_by_id(user_id)
            cloth_data = get_cloth_data(offer.clothId)
            offers_data.append({
                "offer": self.to_dict(offer),
                "cloth": cloth_data,
                'user': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'cellphone': user.cellphone
                        }
            })
        return BaseResponse(offers_data, "Offers fetched successfully", True, HTTPStatus.OK)
    
    def to_dict(self, offer: Offer):
        return {
            "id": offer.id,
            "uuid": offer.uuid,
            "clothId": offer.clothId,
            "offer": offer.offer,
            "buyerId": offer.buyerId,
            "sellerId": offer.sellerId,
            "statusId": offer.statusId
        }
