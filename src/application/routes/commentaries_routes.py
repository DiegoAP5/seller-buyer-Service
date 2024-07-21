from flask import Blueprint, request
from application.controllers.commentaries_controller import CommentariesController

commentaries_bp = Blueprint('commentaries', __name__)
controller = CommentariesController()

@commentaries_bp.route('/commentaries/create', methods=['POST'])
def create_commentaries():
    data = request.json
    response = controller.create_commentaries(data)
    return response.to_response()

@commentaries_bp.route('/commentaries/update/<uuid>', methods=['PUT'])
def update_commentaries(uuid):
    data = request.json
    response = controller.update_commentaries(uuid, data)
    return response.to_response()

@commentaries_bp.route('/commentaries/<uuid>', methods=['GET'])
def get_commentaries(uuid):
    response = controller.getl_commentaries(uuid)
    return response.to_response()

@commentaries_bp.route('/commentaries/seller/<seller_id>', methods=['GET'])
def get_commentaries_by_seller(seller_id):
    response = controller.get_commentaries_by_seller(seller_id)
    return response.to_response()

@commentaries_bp.route('/commentaries/delete/<uuid>', methods=['DELETE'])
def delete_commentaries(uuid):
    response = controller.delete_commentaries(uuid)
    return response.to_response()

@commentaries_bp.route('/commentaries', methods=['GET'])
def list_commentaries():
    response = controller.list_commentaries()
    return response.to_response()
