from marshmallow import ValidationError
from domain.models.status import Status
from infraestructure.repositories.status_repository import StatusRepository
from infraestructure.db import SessionLocal
from application.schemas.status_schema import StatusSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class StatusController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = StatusRepository(self.session)
        self.schema = StatusSchema()

    def create_status(self, data):
        try:
            validated_data = self.schema.load(data)
            new_status = Status(**validated_data)
            self.repo.add(new_status)
            return BaseResponse(self.to_dict(new_status), "Status created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_status(self, uuid, data):
        status = self.repo.get_by_uuid(Status, uuid)
        if status:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(status, key, value)
                self.repo.update(status)
                return BaseResponse(self.to_dict(status), "Status updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Status not found", False, HTTPStatus.NOT_FOUND)

    def get_status(self, uuid):
        status = self.repo.get_by_uuid(Status, uuid)
        if status:
            return BaseResponse(self.to_dict(status), "Status fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Status not found", False, HTTPStatus.NOT_FOUND)

    def delete_status(self, uuid):
        status = self.repo.get_by_uuid(Status, uuid)
        if status:
            self.repo.delete(status)
            return BaseResponse(None, "Status deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Status not found", False, HTTPStatus.NOT_FOUND)

    def list_statuses(self):
        status_list = self.repo.get_all(Status)
        return BaseResponse([self.to_dict(status) for status in status_list], "Statuses fetched successfully", True, HTTPStatus.OK)

    def to_dict(self, status: Status):
        return {
            "id": status.id,
            "uuid": status.uuid,
            "name": status.name,
            "description": status.description
        }
