from marshmallow import ValidationError
from domain.models.offer import Offer
from domain.models.delivery import Delivery
from infraestructure.repositories.offer_repository import OfferRepository
from infraestructure.repositories.delivery_repository import DeliveryRepository
from infraestructure.db import SessionLocal
from application.schemas.offer_schema import OfferSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class OfferController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = OfferRepository(self.session)
        self.delivery_repo = DeliveryRepository(self.session)
        self.schema = OfferSchema()

    def create_offer(self, data):
        try:
            validated_data = self.schema.load(data)
            new_offer = Offer(**validated_data)
            self.repo.add(new_offer)
            return BaseResponse(self.to_dict(new_offer), "Offer created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_offer(self, uuid, data):
        offer = self.repo.get_by_uuid(Offer, uuid)
        if offer:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(offer, key, value)
                self.repo.update(offer)

                if 'statusId' in validated_data:
                    # Crear una entrada en Delivery si el estado de la oferta ha cambiado
                    delivery_data = {
                        "date": validated_data.get("date"),
                        "clothId": offer.clothId,
                        "location": validated_data.get("location"),
                        "buyer": validated_data.get("buyer"),
                        "cellphone": validated_data.get("cellphone"),
                        "comments": validated_data.get("comments"),
                        "statusId": validated_data.get("statusId"),
                        "sellerId": offer.sellerId,
                        "buyerId": offer.buyerId,
                        "offerId": offer.id
                    }
                    new_delivery = Delivery(**delivery_data)
                    self.delivery_repo.add(new_delivery)

                return BaseResponse(self.to_dict(offer), "Offer updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def get_offer(self, uuid):
        offer = self.repo.get_by_uuid(Offer, uuid)
        if offer:
            return BaseResponse(self.to_dict(offer), "Offer fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def delete_offer(self, uuid):
        offer = self.repo.get_by_uuid(Offer, uuid)
        if offer:
            self.repo.delete(offer)
            return BaseResponse(None, "Offer deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Offer not found", False, HTTPStatus.NOT_FOUND)

    def list_offers(self):
        offer_list = self.repo.get_all(Offer)
        return BaseResponse([self.to_dict(offer) for offer in offer_list], "Offers fetched successfully", True, HTTPStatus.OK)

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
