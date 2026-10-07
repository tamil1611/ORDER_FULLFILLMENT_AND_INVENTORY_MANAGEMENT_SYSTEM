# Order Fulfillment & Inventory Management Platform

A backend system built with **FastAPI** and **PostgreSQL** to manage products, inventory, warehouses, orders, order fulfillment, returns, notifications, and audit logs.

## Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Authentication:** JWT
* **Validation:** Pydantic
* **Testing:** Pytest
* **API Testing:** Postman
* **Server:** Uvicorn

## Features

### Authentication & Authorization

* User registration and login
* JWT access and refresh tokens
* Logout and token revocation
* Role-based access control
* Active/inactive user validation

### Product Management

* Product management
* Product details and pricing
* SKU management
* Product availability status

### Warehouse & Inventory Management

* Warehouse management
* Product inventory by warehouse
* Inventory adjustment
* Inventory transfer between warehouses
* Available, reserved and damaged quantities
* Reorder-level monitoring
* Inventory transaction tracking

### Order Management

* Create orders
* View order details
* Order status management
* Order confirmation
* Order fulfillment
* Order cancellation
* Order return processing
* Order item management
* Inventory reservation during order creation

### Return Management

* Create return requests
* Approve/reject returns
* Return status tracking
* Return reason tracking

### Notifications

* Order-related notifications
* Inventory and low-stock notifications
* Notification read/unread status
* Mark notification as read
* Mark all notifications as read

### Audit Logs

* Track important system actions
* Store user, action and entity information
* Maintain system activity history

## Project Structure

```text
order_fulfillment_system/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── tests/
│
├── .env
├── .env.example
├── alembic.ini
├── requirements.txt
├── README.md
└── Postman_Collection.json
```

## Database Models

The main database entities are:

* Users
* Products
* Warehouses
* Inventory
* Inventory Transactions
* Orders
* Order Items
* Returns
* Notifications
* Audit Logs

The complete ER Diagram is available in:

```text
docs/ER_Diagram.png
```

## Architecture

The application follows a layered architecture:

```text
Client / Postman
       ↓
FastAPI Routers
       ↓
Services
       ↓
Repositories
       ↓
SQLAlchemy ORM
       ↓
PostgreSQL
```

Architecture Diagram:

```text
docs/Architecture_Diagram.png
```

## Prerequisites

Install the following before running the project:

* Python 3.11+
* PostgreSQL
* Git
* pip
* Virtual Environment

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd order_fulfillment_system
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE order_fulfillment_db;
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/order_fulfillment_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Run Alembic Migrations

Apply all database migrations:

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Then:

```bash
alembic upgrade head
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Detailed API documentation is available in:

```text
docs/API_Documentation.md
```

## Authentication

The API uses JWT-based authentication.

### Login Flow

```text
Register
   ↓
Login
   ↓
Access Token
   ↓
Authorization: Bearer <access_token>
   ↓
Protected APIs
```

For protected endpoints, send:

```http
Authorization: Bearer <access_token>
```

## Main API Modules

| Module         | Endpoint                       | Method |
| -------------- | ------------------------------ | ------ |
| Authentication | `/auth/register`               | POST   |
| Authentication | `/auth/login`                  | POST   |
| Profile        | `/profile`                     | GET    |
| Inventory      | `/api/inventory`               | GET    |
| Inventory      | `/api/inventory/{product_id}`  | GET    |
| Inventory      | `/api/inventory/adjust`        | POST   |
| Inventory      | `/api/inventory/transfer`      | POST   |
| Orders         | `/api/orders`                  | POST   |
| Orders         | `/api/orders`                  | GET    |
| Orders         | `/api/orders/{id}`             | GET    |
| Returns        | `/api/returns`                 | POST   |
| Notifications  | `/api/notifications`           | GET    |
| Notifications  | `/api/notifications/{id}/read` | PATCH  |
| Notifications  | `/api/notifications/read-all`  | PATCH  |

> Refer to the complete API documentation for all available endpoints, request schemas, responses, authentication requirements, and role permissions.

## Testing

Run the automated tests using:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

## Postman

A Postman collection is included for API testing.

```text
Postman_Collection.json
```

Import the collection into Postman and configure the required environment variables.

## Error Handling

The application provides structured error handling for:

* Validation errors
* Authentication errors
* Authorization errors
* Resource not found
* Invalid order status transitions
* Insufficient inventory
* Duplicate resources
* Invalid inventory adjustments
* Database-related errors

## Role-Based Access Control

The system supports role-based permissions.

Example roles include:

* **Admin**
* **Warehouse Manager**
* **Customer**

Protected operations are restricted based on the authenticated user's role.

## Order Flow

```text
Create Order
     ↓
Reserve Inventory
     ↓
PENDING
     ↓
CONFIRMED
     ↓
FULFILLED
     ↓
SHIPPED
     ↓
DELIVERED
```

Cancellation and return operations are handled according to the order status and business rules.

## Inventory Flow

```text
Purchase / Adjustment
        ↓
Available Inventory
        ↓
Order Created
        ↓
Inventory Reserved
        ↓
Order Fulfilled
        ↓
Inventory Updated
```

Inventory transactions are recorded for important stock movements.

## Documentation

Project documentation includes:

```text
docs/
├── ER_Diagram.png
├── Architecture_Diagram.png
├── API_Documentation.md
└── Database_Setup.md
```

## Project Deliverables

* GitHub Repository
* Complete FastAPI Source Code
* PostgreSQL Database Models
* Alembic Migrations
* `.env.example`
* Postman Collection
* Automated Tests
* ER Diagram
* Architecture Diagram
* README
* API Documentation
* Database Setup Instructions

## Concurrency & Transactions

The system uses database transactions and row-level locking to safely handle concurrent inventory operations.

### Row-Level Locking

Inventory reservation uses PostgreSQL row-level locking with SQLAlchemy `SELECT FOR UPDATE`.

When multiple users try to reserve the same inventory at the same time:

1. The first transaction locks the inventory row.
2. It checks the available quantity.
3. The quantity is moved from available stock to reserved stock.
4. The transaction is committed.
5. The next transaction waits for the lock and then checks the latest inventory quantity.
6. If sufficient stock is not available, the operation fails with an insufficient inventory error.

This prevents race conditions and negative inventory.

### Transactions

Order creation and inventory reservation are performed within a database transaction. If an error occurs during order creation, the transaction is rolled back so that partial inventory changes are not persisted.

### Database Constraints

A unique constraint on `product_id` and `warehouse_id` ensures that only one inventory record exists for each product in a warehouse.

### Idempotency

Critical APIs use idempotency keys to prevent duplicate operations:

* Create Order
* Payment Confirmation
* Inventory Adjustment
* Inventory Transfer

If the same idempotency key is submitted with the same request data, the previously stored response is returned. If the same key is used with different request data, the API returns `409 Conflict`.

## Testing

The project includes automated tests using pytest.

### Test Coverage

The automated tests cover:

- Order quantity validation
- Insufficient inventory validation
- Product existence validation
- Idempotency request hashing
- Different request data detection
- Concurrent inventory reservation

### Running Tests

Run all tests using:

```bash
python -m pytest tests -v


## License

This project is developed for learning, training, and project evaluation purposes.