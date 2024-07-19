from marshmallow import ValidationError
from domain.models.commentaries import Commentaries
from infraestructure.repositories.commentaries_repository import CommentariesRepository
from infraestructure.db import SessionLocal
from application.schemas.commentaries_schema import CommentariesSchema
from application.schemas.base_response import BaseResponse
from http import HTTPStatus

class CommentariesController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = CommentariesRepository(self.session)
        self.schema = CommentariesSchema()

    def create_commentaries(self, data):
        try:
            validated_data = self.schema.load(data)
            new_commentaries = Commentaries(**validated_data)
            self.repo.add(new_commentaries)
            return BaseResponse(self.to_dict(new_commentaries), "Commentaries created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_commentaries(self, uuid, data):
        commentaries = self.repo.get_by_uuid(Commentaries, uuid)
        if commentaries:
            try:
                validated_data = self.schema.load(data, partial=True)
                for key, value in validated_data.items():
                    setattr(commentaries, key, value)
                self.repo.update(commentaries)
                return BaseResponse(self.to_dict(commentaries), "Commentaries updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)

    def get_commentaries(self, uuid):
        commentaries = self.repo.get_by_uuid(Commentaries, uuid)
        if commentaries:
            return BaseResponse(self.to_dict(commentaries), "Commentaries fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)

    def delete_commentaries(self, uuid):
        commentaries = self.repo.get_by_uuid(Commentaries, uuid)
        if commentaries:
            self.repo.delete(commentaries)
            return BaseResponse(None, "Commentaries deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)

    def list_commentaries(self):
        commentaries_list = self.repo.get_all(Commentaries)
        return BaseResponse([self.to_dict(commentaries) for commentaries in commentaries_list], "Commentaries fetched successfully", True, HTTPStatus.OK)

    def to_dict(self, commentaries: Commentaries):
        return {
            "id": commentaries.id,
            "uuid": commentaries.uuid,
            "clothId": commentaries.clothId,
            "offer": commentaries.offer,
            "buyerId": commentaries.buyerId,
            "sellerId": commentaries.sellerId
        }
