
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from services import (
    inventory_db,
    sales_db,
    check_stock,
    reduce_stock,
    get_book as find_book,
    create_order,
    create_delivery
)

app = Flask(__name__)
CORS(app)

# ==========================================
# API KEY AUTHENTICATION
# ==========================================

API_KEY = "bookstore-secret-token-2026"


def verify_api_key():
    key = request.headers.get("X-API-Key")

    if key != API_KEY:
        abort(
            401,
            description="Unauthorized: Invalid or missing API Key."
        )


# ==========================================
# 1. INVENTORY ENDPOINT
# ==========================================

@app.route('/api/v1/books/<isbn>', methods=['GET'])
def get_book(isbn):
    verify_api_key()

    book = find_book(isbn)

    if not book:
        return jsonify({
            "error": "Book not found in Inventory System"
        }), 404

    return jsonify(book), 200


# ==========================================
# 2. SALES AND ORDER ENDPOINT
# ==========================================

@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    verify_api_key()

    data = request.get_json(silent=True) or {}

    required = [
        "customer_id",
        "isbn",
        "quantity",
        "payment_method"
    ]

    if not all(field in data for field in required):
        return jsonify({
            "error": "Missing required fields"
        }), 400

    isbn = data["isbn"]
    quantity = data["quantity"]

    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return jsonify({
            "error": "Quantity must be a positive whole number"
        }), 400

    book = find_book(isbn)

    if not book:
        return jsonify({
            "error": "Book not found in Inventory System"
        }), 400

    if not check_stock(isbn, quantity):
        return jsonify({
            "error": "Insufficient stock or book unavailable"
        }), 400

    # Reduce inventory after checking availability
    reduce_stock(isbn, quantity)

    # Create the customer order
    order_record = create_order(
        data["customer_id"],
        isbn,
        quantity,
        data["payment_method"],
        book
    )

    return jsonify(order_record), 201


# ==========================================
# 3. DELIVERY ENDPOINT
# ==========================================

@app.route('/api/v1/deliveries/<order_id>', methods=['PUT'])
def update_delivery(order_id):
    verify_api_key()

    if order_id not in sales_db:
        return jsonify({
            "error": "Associated order not found in Sales System"
        }), 404

    data = request.get_json(silent=True) or {}

    required = [
        "shipping_address",
        "courier_service",
        "estimated_delivery_date"
    ]

    if not all(field in data for field in required):
        return jsonify({
            "error": "Missing delivery configuration fields"
        }), 400

    delivery_record = create_delivery(
        order_id,
        data["shipping_address"],
        data["courier_service"],
        data["estimated_delivery_date"]
    )

    return jsonify(delivery_record), 200


# ==========================================
# RUN THE APPLICATION
# ==========================================

if __name__ == '__main__':
    app.run(debug=True, port=5000)
