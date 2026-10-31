from flask import Flask, jsonify, request, abort
import uuid
from datetime import datetime

app = Flask(__name__)

# Security configuration (API Key authentication)
API_KEY = "bookstore-secret-token-2026"

def verify_api_key():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        abort(401, description="Unauthorized: Invalid or missing API Key.")

# --- Mock Subsystem Data Stores ---
inventory_db = {
    "978-0132350884": {
        "isbn": "978-0132350884",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 2500.00,
        "currency": "KES",
        "stock_level": 42
    }
}

sales_db = {}
delivery_db = {}

# --- 1. Inventory Endpoint ---
@app.route('/api/v1/books/<isbn>', methods=['GET'])
def get_book(isbn):
    verify_api_key()
    book = inventory_db.get(isbn)
    if not book:
        return jsonify({"error": "Book not found in Inventory System"}), 404
    return jsonify(book), 200

# --- 2. Sales Endpoint ---
@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    verify_api_key()
    data = request.get_json()
    
    required = ["customer_id", "isbn", "quantity", "payment_method"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
        
    isbn = data["isbn"]
    qty = data["quantity"]
    
    book = inventory_db.get(isbn)
    if not book or book["stock_level"] < qty:
        return jsonify({"error": "Insufficient stock or book unavailable"}), 400
        
    total_amount = book["price"] * qty
    order_id = str(uuid.uuid4())
    
    # Deduct stock from inventory
    book["stock_level"] -= qty
    
    order_record = {
        "order_id": order_id,
        "customer_id": data["customer_id"],
        "isbn": isbn,
        "quantity": qty,
        "status": "PAID",
        "total_amount": total_amount,
        "currency": book["currency"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    sales_db[order_id] = order_record
    
    return jsonify(order_record), 201

# --- 3. Delivery Endpoint ---
@app.route('/api/v1/deliveries/<order_id>', methods=['PUT'])
def update_delivery(order_id):
    verify_api_key()
    if order_id not in sales_db:
        return jsonify({"error": "Associated order not found in Sales System"}), 404
        
    data = request.get_json()
    required = ["shipping_address", "courier_service", "estimated_delivery_date"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing delivery configuration fields"}), 400
        
    delivery_id = str(uuid.uuid4())
    delivery_record = {
        "delivery_id": delivery_id,
        "order_id": order_id,
        "status": "DISPATCHED",
        "courier_service": data["courier_service"],
        "shipping_address": data["shipping_address"],
        "estimated_delivery_date": data["estimated_delivery_date"]
    }
    delivery_db[order_id] = delivery_record
    
    return jsonify(delivery_record), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)