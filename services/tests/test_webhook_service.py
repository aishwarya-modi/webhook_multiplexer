import pytest
from unittest.mock import MagicMock
from bson.objectid import ObjectId
from exceptions import NotFoundError
from services.webhook_service import WebhookService, DatabaseError, RESPONSE_CODE_SUCCESS

@pytest.fixture
def mock_log_service():
    return MagicMock()

@pytest.fixture
def mock_mongo():
    return MagicMock()


def test_create_webhook_success(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_result = MagicMock(acknowledged=True, inserted_id=ObjectId())  # Generate a valid ObjectId
    mock_collection.insert_one.return_value = mock_result
    mock_mongo.webhook_db.webhooks = mock_collection

    data = {"customer_id": "123", "webhook_url": "http://example.com"}
    result, status_code = service.create_webhook(data)

    assert status_code == RESPONSE_CODE_SUCCESS
    assert 'webhook_id' in result
    assert ObjectId.is_valid(result['webhook_id'])  # Check if the returned ID is a valid ObjectId
    assert result['webhook_url'] == data['webhook_url']
    assert mock_log_service.create_log.called

def test_create_webhook_database_error(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_collection.insert_one.return_value = MagicMock(acknowledged=False)
    mock_mongo.webhook_db.webhooks = mock_collection

    data = {"customer_id": "123", "webhook_url": "http://example.com"}
    with pytest.raises(DatabaseError):
        service.create_webhook(data)

    assert mock_log_service.create_log.called

def test_add_endpoints_success(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_collection.update_one.return_value = None  # Mocking successful update
    mock_mongo.webhook_db.webhooks = mock_collection

    webhook_id = ObjectId()
    data = {"endpoints": [{"url": "http://example1.com"}, {"url": "http://example2.com"}]}
    result, status_code = service.add_endpoints(str(webhook_id), data)

    assert status_code == RESPONSE_CODE_SUCCESS
    assert result['webhook_id'] == str(webhook_id)
    assert len(result['endpoints']) == len(data['endpoints'])
    assert mock_log_service.create_log.called

def test_add_endpoints_database_error(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_collection.update_one.side_effect = Exception("MongoDB connection error")
    mock_mongo.webhook_db.webhooks = mock_collection

    webhook_id = ObjectId()
    data = {"endpoints": [{"url": "http://example1.com"}, {"url": "http://example2.com"}]}
    with pytest.raises(DatabaseError):
        service.add_endpoints(str(webhook_id), data)

    assert mock_log_service.create_log.called

def test_delete_endpoint_success(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_collection.update_one.return_value = None  # Mocking successful update
    mock_mongo.webhook_db.webhooks = mock_collection

    webhook_id = ObjectId()
    endpoint_id = "abcdef1234567890"
    result, status_code = service.delete_endpoint(str(webhook_id), endpoint_id)

    assert status_code == RESPONSE_CODE_SUCCESS
    assert result == {"message": "Endpoint deleted successfully"}
    assert mock_log_service.create_log.called


def test_delete_endpoint_not_found(mock_log_service, mock_mongo):
    service = WebhookService()
    service.log_service = mock_log_service
    service.mongo = mock_mongo

    # Mocking MongoDB collection methods
    mock_collection = MagicMock()
    mock_mongo.webhook_db.webhooks = mock_collection

    webhook_id = ObjectId()
    endpoint_id = "abcdef1234567890"

    # Mocking behavior for find_one and update_one methods
    mock_collection.find_one.return_value = None  # Simulate no webhook found
    mock_collection.update_one.return_value = MagicMock(matched_count=0)  # Simulate no document updated

    # Test the delete_endpoint method with pytest.raises
    with pytest.raises(NotFoundError) as excinfo:
        service.delete_endpoint(str(webhook_id), endpoint_id)

    # Additional check to verify the exception message or type, if needed
    assert isinstance(excinfo.value, NotFoundError)
    assert str(excinfo.value) == "Webhook not found"
