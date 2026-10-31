# Bookstore Management System API

## 1. Project Overview

The Bookstore Management System API is a RESTful web service developed using Python and Flask. It demonstrates how different business subsystems can communicate and exchange data through a centralized API.

The project integrates three mock services:

- **Inventory Service:** Manages book information, prices and stock levels.
- **Sales Service:** Processes customer orders, validates stock availability and simulates payments.
- **Delivery Service:** Creates delivery records and manages courier and shipping information.

The API uses JSON for data exchange and API key authentication to protect its endpoints.

## 2. Technologies and Tools

- Python – Main programming language.
- Flask – Backend web framework.
- Flask-CORS – Enables cross-origin requests.
- Pytest – Automated testing framework.
- Swagger Editor / OpenAPI 3.0 – API documentation and testing.
- JSON – Data exchange format.
- Git and GitHub – Version control and project hosting.

## 3. Features and Architecture

### 3.1 Inventory Service

- Retrieves book details using an ISBN.
- Checks available stock.
- Updates stock levels when orders are placed.

### 3.2 Sales Service

- Accepts customer orders.
- Validates order information and stock availability.
- Calculates order totals.
- Simulates payment processing.
- Generates unique order IDs.

### 3.3 Delivery Service

- Associates delivery records with existing orders.
- Stores shipping addresses and courier information.
- Generates unique delivery IDs.
- Assigns a dispatch status.

### 3.4 Security and Validation

- API key authentication through the `X-API-Key` request header.
- Validation of required request fields.
- Positive whole-number validation for order quantities.
- Appropriate HTTP response codes for successful and unsuccessful requests.

## 4. API Endpoints

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/books/{isbn}` | Retrieves book information. |
| POST | `/api/v1/orders` | Creates a customer order. |
| PUT | `/api/v1/deliveries/{order_id}` | Creates a delivery record for an existing order. |

## 5. Authentication

All API endpoints require an API key supplied through the request header:

`X-API-Key: your-api-key`

For this demonstration, the application uses a development API key configured in `main.py`.

## 6. Installation and Setup

### 6.1 Prerequisites

- Python 3 installed.
- Visual Studio Code or another Python editor.
- Git installed for version control.

### 6.2 Clone the Repository

```bash
git clone https://github.com/anyangobrilla-bit/Bookstore_API.git
cd Bookstore_API
```

### 6.3 Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 6.4 Install Dependencies

```bash
pip install -r requirements.txt
```

### 6.5 Run the Application

```bash
python main.py
```

The API will be available at:

`http://127.0.0.1:5000`

## 7. API Testing

The API was tested using Swagger Editor and automated tests with pytest.

To execute the automated test suite, run:

```bash
python -m pytest -v
```

The test suite covers:

1. Successful retrieval of book information.
2. Unauthorized access rejection.
3. Successful customer order creation.
4. Successful delivery record creation.

**Test results: 4 tests passed.**

All three API endpoints were also tested successfully using Swagger Editor.

## 8. API Documentation

The API is documented using OpenAPI 3.0 in the `openapi.yaml` file.

The documentation can be viewed and used for interactive testing through:

[Swagger Editor](https://editor.swagger.io/)

Import the `openapi.yaml` file into Swagger Editor to explore the available endpoints, request formats and response codes.

## 9. Limitations and Future Improvements

The current implementation uses mock services and in-memory data storage. Therefore, records are not permanently retained when the application restarts.

Payment processing is simulated and does not connect to an actual payment provider.

Future improvements could include:

- Integration with a permanent database such as PostgreSQL.
- Real payment gateway integration, such as M-Pesa.
- Deployment to a production server.
- Improved authentication using secure token management.
- Integration with actual inventory and delivery systems.

## 10. Conclusion

The project demonstrates how RESTful APIs can facilitate communication and data exchange between independent business subsystems. It provides a practical example of service integration through standardized HTTP methods, JSON data exchange, authentication and API documentation.