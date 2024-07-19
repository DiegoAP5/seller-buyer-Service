from flask import Blueprint, request
from application.controllers.delivery_controller import DeliveryController

delivery_bp = Blueprint('delivery', __name__)
controller = DeliveryController()

@delivery_bp.route('/delivery/create', methods=['POST'])
def create_delivery():
    data = request.json
    response = controller.create_delivery(data)
    return response.to_response()

@delivery_bp.route('/delivery/update/<uuid>', methods=['PUT'])
def update_delivery(uuid):
    data = request.json
    response = controller.update_delivery(uuid, data)
    return response.to_response()

@delivery_bp.route('/delivery/<uuid>', methods=['GET'])
def get_delivery(uuid):
    response = controller.get_delivery(uuid)
    return response.to_response()

@delivery_bp.route('/delivery/delete/<uuid>', methods=['DELETE'])
def delete_delivery(uuid):
    response = controller.delete_delivery(uuid)
    return response.to_response()

@delivery_bp.route('/delivery', methods=['GET'])
def list_deliveries():
    response = controller.list_deliveries()
    return response.to_response()
