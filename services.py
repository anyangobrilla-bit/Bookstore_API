
import uuid
from datetime import datetime, timezone

# ==========================================
# MOCK INVENTORY SERVICE
# ==========================================

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


def get_book(isbn):
    """Retrieve a book using its ISBN."""
    normalized_isbn = isbn.replace("-", "")

    for stored_isbn, book in inventory_db.items():
        if stored_isbn.replace("-", "") == normalized_isbn:
            return book

    return None


def check_stock(isbn, quantity):
    """Check whether the requested quantity is available."""
    book = get_book(isbn)

    return (
        book is not None
        and isinstance(quantity, int)
        and not isinstance(quantity, bool)
        and quantity > 0
        and book["stock_level"] >= quantity
    )


def reduce_stock(isbn, quantity):
    """Reduce inventory after a successful order."""
    if not check_stock(isbn, quantity):
        return False

    book = get_book(isbn)
    book["stock_level"] -= quantity

    return True


# ==========================================
# MOCK SALES SERVICE
# ==========================================

sales_db = {}


def create_order(customer_id, isbn, quantity, payment_method, book):
    """Create and store a customer order."""

    order_id = str(uuid.uuid4())
    total_amount = book["price"] * quantity

    order_record = {
        "order_id": order_id,
        "customer_id": customer_id,
        "isbn": book["isbn"],
        "quantity": quantity,
        "payment_method": payment_method,
        "status": "PAID",
        "total_amount": total_amount,
        "currency": book["currency"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    sales_db[order_id] = order_record

    return order_record


# ==========================================
# MOCK DELIVERY SERVICE
# ==========================================

delivery_db = {}


def create_delivery(
    order_id,
    shipping_address,
    courier_service,
    estimated_delivery_date
):
    """Create a delivery record for an order."""

    delivery_record = {
        "delivery_id": str(uuid.uuid4()),
        "order_id": order_id,
        "status": "DISPATCHED",
        "courier_service": courier_service,
        "shipping_address": shipping_address,
        "estimated_delivery_date": estimated_delivery_date
    }

    delivery_db[order_id] = delivery_record

    return delivery_record
