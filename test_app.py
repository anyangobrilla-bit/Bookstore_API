import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_inventory_success(client):
    response = client.get(
        "/api/v1/books/978-0132350884",
        headers={"X-API-Key": "bookstore-secret-token-2026"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["isbn"] == "978-0132350884"
    assert data["title"] == "Clean Code"

def test_unauthorized_access(client):
    response = client.get("/api/v1/books/978-0132350884")
    assert response.status_code == 401

def test_place_order_success(client):
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": "cust-123",
            "isbn": "978-0132350884",
            "quantity": 2,
            "payment_method": "credit_card"
        },
        headers={"X-API-Key": "bookstore-secret-token-2026"}
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.get_json()
    assert "order_id" in data
    assert data["quantity"] == 2

def test_update_delivery_success(client):
    # First, place an order so we have a valid order_id to update
    order_response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": "cust-123",
            "isbn": "978-0132350884",
            "quantity": 1,
            "payment_method": "credit_card"
        },
        headers={"X-API-Key": "bookstore-secret-token-2026"}
    )
    order_data = order_response.get_json()
    order_id = order_data["order_id"]

    # Now, update/create delivery details for that order
    response = client.put(
        f"/api/v1/deliveries/{order_id}",
        json={
            "shipping_address": "123 Main Street, Nairobi",
            "courier_service": "SpeedyCourier",
            "estimated_delivery_date": "2026-11-05"
        },
        headers={"X-API-Key": "bookstore-secret-token-2026"}
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.get_json()
    assert data["order_id"] == order_id
    assert data["courier_service"] == "SpeedyCourier"