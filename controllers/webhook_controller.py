from flask import Blueprint, request, jsonify, current_app
from flasgger.utils import swag_from
from services.webhook_service import WebhookService

webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.before_app_request
def initialize_service():
    if 'webhook_service' not in current_app.config:
        current_app.config['webhook_service'] = WebhookService()

def get_webhook_service():
    return current_app.config['webhook_service']

@webhook_blueprint.route('/webhooks', methods=['POST'])
@swag_from({
    'summary': 'Create a new webhook',
    'responses': {
        201: {
            'description': 'Webhook created successfully',
            'examples': {
                'application/json': {
                    'webhook_id': '1',
                    'webhook_url': 'http://example.com'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'customer_id': {'type': 'string'},
                    'webhook_url': {'type': 'string'}
                },
                'example': {
                    'customer_id': '123',
                    'webhook_url': 'http://example.com'
                }
            }
        }
    ]
})
def create_webhook():
    data = request.json
    result, status_code = get_webhook_service().create_webhook(data)
    return jsonify(result), status_code

@webhook_blueprint.route('/webhooks/<webhook_id>/endpoints', methods=['POST'])
@swag_from({
    'summary': 'Add endpoints to a webhook',
    'responses': {
        200: {
            'description': 'Endpoints added successfully',
            'examples': {
                'application/json': {
                    'webhook_id': '1',
                    'endpoints': [
                        {'endpoint_id': '1', 'url': 'http://example1.com'},
                        {'endpoint_id': '2', 'url': 'http://example2.com'}
                    ]
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'endpoints': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'url': {'type': 'string'}
                            }
                        }
                    }
                },
                'example': {
                    'endpoints': [
                        {'url': 'http://example1.com'},
                        {'url': 'http://example2.com'}
                    ]
                }
            }
        }
    ]
})
def add_endpoints(webhook_id):
    data = request.json
    result, status_code = get_webhook_service().add_endpoints(webhook_id, data)
    return jsonify(result), status_code

@webhook_blueprint.route('/webhooks/<webhook_id>/endpoints/<endpoint_id>', methods=['DELETE'])
@swag_from({
    'summary': 'Delete an endpoint',
    'responses': {
        200: {
            'description': 'Endpoint deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Endpoint deleted successfully'
                }
            }
        }
    }
})
def delete_endpoint(webhook_id, endpoint_id):
    result, status_code = get_webhook_service().delete_endpoint(webhook_id, endpoint_id)
    return jsonify(result), status_code

@webhook_blueprint.route('/webhooks', methods=['GET'])
@swag_from({
    'summary': 'List all webhooks',
    'responses': {
        200: {
            'description': 'List of webhooks',
            'examples': {
                'application/json': [
                    {
                        'webhook_id': '1',
                        'webhook_url': 'http://example.com',
                        'endpoints': []
                    }
                ]
            }
        }
    }
})
def list_webhooks():
    result, status_code = get_webhook_service().list_webhooks()
    return jsonify(result), status_code

@webhook_blueprint.route('/logs/webhooks/<webhook_id>', methods=['GET'])
@swag_from({
    'summary': 'Get webhook logs',
    'responses': {
        200: {
            'description': 'List of webhook logs',
            'examples': {
                'application/json': [
                    {
                        'webhook_id': '1',
                        'endpoint_id': '2',
                        'status': 'success',
                        'response_code': 200,
                        'response_body': 'Forwarded successfully',
                        'timestamp': '2023-06-01T12:00:00Z'
                    }
                ]
            }
        }
    }
})
def get_webhook_logs(webhook_id):
    result, status_code = get_webhook_service().get_webhook_logs(webhook_id)
    return jsonify(result), status_code

@webhook_blueprint.route('/webhooks/<webhook_id>', methods=['POST'])
@swag_from({
    'summary': 'Trigger webhook',
    'responses': {
        200: {
            'description': 'Webhook triggered successfully',
            'examples': {
                'application/json': {
                    'status': 'success'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {'type': 'object'}
                }
            }
        }
    ]
})
def receive_webhook(webhook_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    result, status_code = get_webhook_service().receive_webhook(webhook_id, data)
    return jsonify(result), status_code
