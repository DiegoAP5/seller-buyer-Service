from flask import Blueprint, request
from application.controllers.offer_controller import OfferController

offer_bp = Blueprint('offer', __name__)
controller = OfferController()

@offer_bp.route('/offer/create', methods=['POST'])
def create_offer():
    data = request.json
    response = controller.create_offer(data)
    return response.to_response()

@offer_bp.route('/offer/update/<uuid>', methods=['PUT'])
def update_offer(uuid):
    data = request.json
    response = controller.update_offer(uuid, data)
    return response.to_response()

@offer_bp.route('/offer/<uuid>', methods=['GET'])
def get_offer(uuid):
    response = controller.get_offer(uuid)
    return response.to_response()

@offer_bp.route('/offer/delete/<uuid>', methods=['DELETE'])
def delete_offer(uuid):
    response = controller.delete_offer(uuid)
    return response.to_response()

@offer_bp.route('/offer', methods=['GET'])
def list_offers():
    response = controller.list_offers()
    return response.to_response()
