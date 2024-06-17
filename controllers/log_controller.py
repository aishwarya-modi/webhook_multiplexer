from flask import Blueprint, request, jsonify, current_app
from flasgger.utils import swag_from
from services.log_service import LogService

log_blueprint = Blueprint('log', __name__)

@log_blueprint.before_app_request
def initialize_service():
    if 'log_service' not in current_app.config:
        current_app.config['log_service'] = LogService()

def get_log_service():
    return current_app.config['log_service']

@log_blueprint.route('/logs/webhooks/<webhook_id>', methods=['GET'])
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
    result, status_code = get_log_service().get_webhook_logs(webhook_id)
    return jsonify(result), status_code



