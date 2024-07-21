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

@delivery_bp.route('/delivery/buyer/<buyer_id>', methods=['GET'])
def list_deliveries_buyer_id(buyer_id):
    response = controller.list_deliveries_buyer(buyer_id)
    return response.to_response()

@delivery_bp.route('/delivery/buyer/status', methods=['GET'])
def list_deliveries_buyer_status():
    status_id = request.args.get('status_id')
    buyer_id = request.args.get('buyer_id')
    response = controller.list_deliveries_buyer_status(buyer_id,status_id)
    return response.to_response()

@delivery_bp.route('/delivery/seller/<seller_id>', methods=['GET'])
def list_deliveries_seller_id(seller_id):
    response = controller.list_deliveries_seller(seller_id)
    return response.to_response()

@delivery_bp.route('/delivery/seller/status', methods=['GET'])
def list_deliveries_by_seller_status():
    seller_id = request.args.get('seller_id')
    buyer_id = request.args.get('buyer_id')
    response = controller.list_deliveries_seller_status(buyer_id,seller_id)
    return response.to_response()