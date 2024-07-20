from marshmallow import ValidationError
from domain.models.commentaries import Commentaries
from infraestructure.repositories.commentaries_repository import CommentariesRepository
from infraestructure.db import SessionLocal
from application.schemas.commentaries_schema import CommentariesSchema
from application.schemas.base_response import BaseResponse
from application.services.commentaries_filter import CommentariesFilterService
from http import HTTPStatus

class CommentariesController:
    def __init__(self):
        self.session = SessionLocal()
        self.repo = CommentariesRepository(self.session)
        self.schema = CommentariesSchema()
        self.filter_service = CommentariesFilterService()

    def create_commentaries(self, data):
        try:
            validated_data = self.schema.load(data)
            validated_data['comments'] = self.filter_service.censor_commentary(validated_data['comments'])
            new_commentaries = Commentaries(**validated_data)
            self.repo.add(new_commentaries)
            return BaseResponse(self.to_dict(new_commentaries), "Commentary created successfully", True, HTTPStatus.CREATED)
        except ValidationError as err:
            return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)

    def update_commentaries(self, uuid, data):
        commentaries = self.repo.get_by_uuid(uuid)
        if commentaries:
            try:
                validated_data = self.schema.load(data, partial=True)
                validated_data['comments'] = self.filter_service.censor_commentary(validated_data['comments'])
                for key, value in validated_data.items():
                    setattr(commentaries, key, value)
                self.repo.update(commentaries)
                return BaseResponse(self.to_dict(commentaries), "Commentary updated successfully", True, HTTPStatus.OK)
            except ValidationError as err:
                return BaseResponse(None, err.messages, False, HTTPStatus.BAD_REQUEST)
        return BaseResponse(None, "Commentary not found", False, HTTPStatus.NOT_FOUND)

    def getl_commentaries(self, uuid):
        commentaries = self.repo.get_by_uuid(uuid)
        if commentaries:
            return BaseResponse(self.to_dict(commentaries), "Commentaries fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)
    
    def all_commentaries_by_seller(self, seller_id):
        commentaries = self.repo.get_all_by_seller_id(seller_id)
        if commentaries:
            return BaseResponse(self.to_dict(commentaries), "Commentaries fetched successfully", True, HTTPStatus.OK)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)

    def delete_commentaries(self, uuid):
        commentaries = self.repo.get_by_uuid(uuid)
        if commentaries:
            self.repo.delete(commentaries)
            return BaseResponse(None, "Commentaries deleted successfully", True, HTTPStatus.NO_CONTENT)
        return BaseResponse(None, "Commentaries not found", False, HTTPStatus.NOT_FOUND)

    def list_commentaries(self):
        commentaries_list = self.repo.get_all()
        return BaseResponse([self.to_dict(commentaries) for commentaries in commentaries_list], "Commentaries fetched successfully", True, HTTPStatus.OK)

    def to_dict(self, commentaries: Commentaries):
        return {
            "id": commentaries.id,
            "uuid": commentaries.uuid,
            "comments": commentaries.comments,
            "sellerId": commentaries.sellerId
        }
