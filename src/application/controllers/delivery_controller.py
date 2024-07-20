from marshmallow import ValidationError
from domain.models.delivery import Delivery
from infraestructure.repositories.delivery_repository import DeliveryRepository
from infraestructure.db import SessionLocal
from application.schemas.delivery_schema import DeliverySchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class DeliveryController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = DeliveryRepository(self.session)
        self.schema = DeliverySchema()

    def create_delivery(self, data):
        try:
            validated_data = self.schema.load(data)
            new_delivery = Delivery(**validated_data)
            self.repo.add(new_delivery)
            return BaseResponse(self.to_dict(new_delivery), "Delivery created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_delivery(self, uuid, data):
        delivery = self.repo.get_by_uuid(uuid)
        if delivery:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(delivery, key, value)
                self.repo.update(delivery)
                return BaseResponse(self.to_dict(delivery), "Delivery updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Delivery not found", False, HTTPStatus.NOT_FOUND)

    def get_delivery(self, uuid):
        delivery = self.repo.get_by_uuid(uuid)
        if delivery:
            return BaseResponse(self.to_dict(delivery), "Delivery fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Delivery not found", False, HTTPStatus.NOT_FOUND)

    def delete_delivery(self, uuid):
        delivery = self.repo.get_by_uuid(uuid)
        if delivery:
            self.repo.delete(delivery)
            return BaseResponse(None, "Delivery deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Delivery not found", False, HTTPStatus.NOT_FOUND)

    def list_deliveries(self):
        deliveries = self.repo.get_all()
        return BaseResponse([self.to_dict(delivery) for delivery in deliveries], "Deliveries fetched successfully", True, HTTPStatus.OK)
    
    def list_deliveries_seller(self, seller_id):
        deliveries = self.repo.get_all_delivery_by_seller(seller_id)
        return BaseResponse([self.to_dict(delivery) for delivery in deliveries], "Deliveries fetched successfully", True, HTTPStatus.OK)
    
    def list_deliveries_seller_status(self, seller_id, status_id):
        deliveries = self.repo.get_all_delivery_by_seller_and_status(seller_id,status_id)
        return BaseResponse([self.to_dict(delivery) for delivery in deliveries], "Deliveries fetched successfully", True, HTTPStatus.OK)
    
    def list_deliveries_buyer(self, buyer_id):
        deliveries = self.repo.get_all_delivery_by_buyer(buyer_id)
        return BaseResponse([self.to_dict(delivery) for delivery in deliveries], "Deliveries fetched successfully", True, HTTPStatus.OK)
    
    def list_deliveries_buyer_status(self, buyer_id, status_id):
        deliveries = self.repo.get_all_delivery_by_buyer_and_status(buyer_id,status_id)
        return BaseResponse([self.to_dict(delivery) for delivery in deliveries], "Deliveries fetched successfully", True, HTTPStatus.OK)

    def to_dict(self, delivery: Delivery):
        return {
            "id": delivery.id,
            "uuid": delivery.uuid,
            "date": delivery.date,
            "clothId": delivery.clothId,
            "location": delivery.location,
            "cellphone": delivery.cellphone,
            "comments": delivery.comments,
            "statusId": delivery.statusId,
            "sellerId": delivery.sellerId,
            "buyerId": delivery.buyerId,
            "offerId": delivery.offerId
        }
