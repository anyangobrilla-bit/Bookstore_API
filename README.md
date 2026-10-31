# Bookstore Management System API

A RESTful API built with **Flask**, **Python**, and **pytest** that integrates multiple micro-subsystems for a fictional bookstore, including **Inventory**, **Sales**, and **Delivery** management.

---

## Features & Architecture

- **Inventory Subsystem (`/api/v1/books/<isbn>`):** Manages book stock levels, pricing, and book details.
- **Sales Subsystem (`/api/v1/orders`):** Processes customer orders, validates stock availability, calculates total amounts, and updates inventory levels.
- **Delivery Subsystem (`/api/v1/deliveries/<order_id>`):** Tracks order fulfillment, courier assignments, and delivery schedules.
- **Security:** Header-based API key authentication across protected endpoints.
- **Testing:** Comprehensive unit test suite powered by `pytest`.

---

## Authentication

All API requests to protected endpoints require an API key passed in the request headers:

```http
X-API-Key: bookstore-secret-token-2026