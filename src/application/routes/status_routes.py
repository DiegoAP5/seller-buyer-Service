from flask import Blueprint, request
from application.controllers.status_controller import StatusController

status_bp = Blueprint('status', __name__)
controller = StatusController()

@status_bp.route('/status/create', methods=['POST'])
def create_status():
    data = request.json
    response = controller.create_status(data)
    return response.to_response()

@status_bp.route('/status/update/<uuid>', methods=['PUT'])
def update_status(uuid):
    data = request.json
    response = controller.update_status(uuid, data)
    return response.to_response()

@status_bp.route('/status/<uuid>', methods=['GET'])
def get_status(uuid):
    response = controller.get_status(uuid)
    return response.to_response()

@status_bp.route('/status/delete/<uuid>', methods=['DELETE'])
def delete_status(uuid):
    response = controller.delete_status(uuid)
    return response.to_response()

@status_bp.route('/status', methods=['GET'])
def list_statuses():
    response = controller.list_statuses()
    return response.to_response()
