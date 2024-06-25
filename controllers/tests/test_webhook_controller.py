import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_webhook(client):
    data = {"customer_id": "123", "webhook_url": "http://example.com"}
    response = client.post("/api/webhooks", json=data)
    print(response.json)
    assert response.status_code == 200
    assert response.json['webhook_id'] != ''

def test_add_endpoints(client):
    webhook_id = "667af9d742482dbaf49bcd62"
    data = {"endpoints": [{"url": "http://example1.com"}, {"url": "http://example2.com"}]}
    response = client.post(f"/api/webhooks/{webhook_id}/endpoints", json=data)
    assert response.status_code == 200
    assert response.json['webhook_id'] != ''

def test_delete_endpoint(client):
    webhook_id = "667af9d742482dbaf49bcd62"
    endpoint_id = "667af9d742482dbaf49bcd62"
    response = client.delete(f"/api/webhooks/{webhook_id}/endpoints/{endpoint_id}")
    assert response.status_code == 200
    assert response.json == {"message": "Endpoint deleted successfully"}

def test_list_webhooks(client):
    response = client.get("/api/webhooks")
    assert response.status_code == 200
    assert len(response.json) != 0 

def test_get_webhook_logs(client):
    webhook_id = "667af9d742482dbaf49bcd62"
    response = client.get(f"/api/logs/webhooks/{webhook_id}")
    assert response.status_code == 200
    assert len(response.json) != 0

def test_trigger_webhook(client):
    webhook_id = "667af9d742482dbaf49bcd62"
    data = {"data": {"key": "value"}}
    response = client.post(f"/api/webhooks/{webhook_id}", json=data)
    assert response.status_code == 200
    assert response.json['data'] != None