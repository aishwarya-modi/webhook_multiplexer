from flask import Blueprint, current_app, jsonify, request
from flasgger.utils import swag_from
from services.customer_service import CustomerService

customer_blueprint = Blueprint('customer', __name__)

@customer_blueprint.before_app_request
def initialize_service():
    if 'customer_service' not in current_app.config:
        current_app.config['customer_service'] = CustomerService()

def get_customer_service():
    return current_app.config['customer_service']

@customer_blueprint.route('/customers/callback', methods=['POST'])
@swag_from({
    'summary': 'Recieve webhook callback',
    'responses': {
        201: {
            'description': 'Webhook callback recieved successfully',
        }
    },
})
def webhook_callback():
    data = request.json
    result, status_code = get_customer_service().webhook_callback(data)
    return jsonify(result), status_code


@customer_blueprint.route('/customers/event1', methods=['POST'])
@swag_from({
    'summary': 'Event 1 API',
    'responses': {
        200: {
            'description': 'Event 1 API executed successfully',
        }
    },
})
def event1():
    data = request.json
    result, status_code = get_customer_service().event1(data)
    return jsonify(result), status_code

@customer_blueprint.route('/customers/event2', methods=['POST'])
@swag_from({
    'summary': 'Event 2 API',
    'responses': {
        200: {
            'description': 'Event 2 API executed successfully',
        }
    },
})
def event2():
    data = request.json
    result, status_code = get_customer_service().event2(data)
    return jsonify(result), status_code

@customer_blueprint.route('/customers/event3', methods=['POST'])
@swag_from({
    'summary': 'Event 3 API',
    'responses': {
        200: {
            'description': 'Event 3 API executed successfully',
        }
    },
})
def event3():
    data = request.json
    result, status_code = get_customer_service().event3(data)
    print(result)
    return jsonify(result), status_code


