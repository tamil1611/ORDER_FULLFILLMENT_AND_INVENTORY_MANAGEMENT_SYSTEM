# Order Fulfillment & Inventory Management Platform

## API Documentation

---

## 1. Overview

This document describes the REST APIs available in the Order Fulfillment & Inventory Management Platform.

### Technology Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT Authentication
* Pydantic
* Pytest

---

# 2. Base URL

```text
http://127.0.0.1:8000
```

The API prefixes are:

```text
/auth
/products
/warehouses
/inventory
/api/orders
/api/returns
/api/notifications
/api/dashboard
/api/audit-logs
```

---

# 3. Authentication

Protected APIs require a JWT access token.

### Header

```http
Authorization: Bearer <access_token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Roles

The application supports the following roles:

* `admin`
* `warehouse_manager`
* `customer`

---

# 4. Common HTTP Status Codes

| Status Code | Meaning                   |
| ----------- | ------------------------- |
| 200         | Successful request        |
| 201         | Resource created          |
| 400         | Business/validation error |
| 401         | Authentication failed     |
| 403         | Access denied             |
| 404         | Resource not found        |
| 422         | Request validation error  |
| 500         | Internal server error     |

---

# 5. Authentication APIs

## 5.1 Register User

### Endpoint

```http
POST /auth/register
```

### Authentication

Not required.

### Request Body

```json
{
  "name": "John",
  "email": "john@example.com",
  "password": "Password@123",
  "role": "customer"
}
```

### Success Response

**201 Created**

```json
{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "role": "customer",
  "is_active": true
}
```

### Error Response

**400 Bad Request**

```json
{
  "detail": "User already exists"
}
```

---

## 5.2 Login

### Endpoint

```http
POST /auth/login
```

### Authentication

Not required.

### Content-Type

```text
application/x-www-form-urlencoded
```

### Request

```text
username=john@example.com
password=Password@123
```

> `username` contains the user's email address.

### Success Response

**200 OK**

```json
{
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>",
  "token_type": "bearer"
}
```

### Invalid Credentials

**401 Unauthorized**

```json
{
  "detail": "Invalid email or password"
}
```

---

## 5.3 Get Current User

### Endpoint

```http
GET /auth/me
```

### Authentication

Required.

### Success Response

**200 OK**

```json
{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "role": "customer",
  "is_active": true
}
```

---

## 5.4 Refresh Access Token

### Endpoint

```http
POST /auth/refresh
```

### Authentication

Refresh token required.

### Query Parameter

```text
refresh_token=<refresh_token>
```

Example:

```http
POST /auth/refresh?refresh_token=<refresh_token>
```

### Success Response

**200 OK**

```json
{
  "access_token": "<new_access_token>",
  "refresh_token": "<new_refresh_token>",
  "token_type": "bearer"
}
```

### Error

**401 Unauthorized**

```json
{
  "detail": "Invalid refresh token"
}
```

---

## 5.5 Logout

### Endpoint

```http
POST /auth/logout
```

### Query Parameter

```text
refresh_token=<refresh_token>
```

### Success Response

**200 OK**

```json
{
  "message": "Logout successful"
}
```

### Possible Errors

**404 Not Found**

```json
{
  "detail": "Refresh token not found"
}
```

**400 Bad Request**

```json
{
  "detail": "Refresh token already revoked"
}
```

---

## 5.6 Change Password

### Endpoint

```http
POST /auth/change-password
```

### Authentication

Required.

### Request Body

```json
{
  "old_password": "OldPassword@123",
  "new_password": "NewPassword@123"
}
```

### Success Response

**200 OK**

```json
{
  "message": "Password changed successfully"
}
```

### Error

**400 Bad Request**

```json
{
  "detail": "Invalid old password"
}
```

---

# 6. Product APIs

## 6.1 Create Product

### Endpoint

```http
POST /products/
```

### Authentication

Required.

### Role

```text
admin
```

### Request Body

```json
{
  "name": "Laptop",
  "sku": "LAP-001",
  "description": "Business laptop",
  "price": 75000
}
```

### Validation

* `name`: 2–150 characters
* `sku`: 1–100 characters
* `price`: greater than 0

### Success Response

**201 Created**

```json
{
  "id": 1,
  "name": "Laptop",
  "sku": "LAP-001",
  "description": "Business laptop",
  "price": 75000,
  "is_active": true
}
```

---

## 6.2 Get Product

### Endpoint

```http
GET /products/{product_id}
```

### Authentication

Required.

### Example

```http
GET /products/1
```

### Success Response

**200 OK**

```json
{
  "id": 1,
  "name": "Laptop",
  "sku": "LAP-001",
  "description": "Business laptop",
  "price": 75000,
  "is_active": true
}
```

### Error

**404 Not Found**

```json
{
  "detail": "Product not found"
}
```

---

## 6.3 Update Product

### Endpoint

```http
PUT /products/{product_id}
```

### Authentication

Required.

### Role

```text
admin
```

### Request Body

```json
{
  "name": "Updated Laptop",
  "description": "Updated description",
  "price": 78000
}
```

All fields are optional.

### Success Response

**200 OK**

```json
{
  "id": 1,
  "name": "Updated Laptop",
  "sku": "LAP-001",
  "description": "Updated description",
  "price": 78000,
  "is_active": true
}
```

---

## 6.4 Activate Product

### Endpoint

```http
PATCH /products/{product_id}/activate
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns the updated product.

---

## 6.5 Deactivate Product

### Endpoint

```http
PATCH /products/{product_id}/deactivate
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns the updated product.

---

## 6.6 List Products

### Endpoint

```http
GET /products/
```

### Authentication

Required.

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "name": "Laptop",
    "sku": "LAP-001",
    "description": "Business laptop",
    "price": 75000,
    "is_active": true
  }
]
```

---

# 7. Warehouse APIs

## 7.1 Create Warehouse

### Endpoint

```http
POST /warehouses/
```

### Authentication

Required.

### Role

```text
admin
```

### Request Body

```json
{
  "name": "Chennai Warehouse",
  "code": "CHN-001",
  "address": "Chennai, Tamil Nadu"
}
```

### Success Response

**201 Created**

```json
{
  "id": 1,
  "name": "Chennai Warehouse",
  "code": "CHN-001",
  "address": "Chennai, Tamil Nadu",
  "is_active": true
}
```

---

## 7.2 Get Warehouse

### Endpoint

```http
GET /warehouses/{warehouse_id}
```

### Authentication

Required.

### Success Response

**200 OK**

Returns warehouse details.

### Error

**404 Not Found**

```json
{
  "detail": "Warehouse not found"
}
```

---

## 7.3 Update Warehouse

### Endpoint

```http
PUT /warehouses/{warehouse_id}
```

### Authentication

Required.

### Role

```text
admin
```

### Request Body

```json
{
  "name": "Updated Warehouse",
  "address": "Updated Address"
}
```

### Success Response

**200 OK**

Returns the updated warehouse.

---

## 7.4 Deactivate Warehouse

### Endpoint

```http
PATCH /warehouses/{warehouse_id}/deactivate
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns the updated warehouse.

---

## 7.5 Activate Warehouse

### Endpoint

```http
PATCH /warehouses/{warehouse_id}/activate
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns the updated warehouse.

---

## 7.6 List Warehouses

### Endpoint

```http
GET /warehouses/
```

### Authentication

Required.

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "name": "Chennai Warehouse",
    "code": "CHN-001",
    "address": "Chennai, Tamil Nadu",
    "is_active": true
  }
]
```

---

# 8. Inventory APIs

## 8.1 Get All Inventory

### Endpoint

```http
GET /inventory/
```

### Authentication

Required.

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "product_id": 1,
    "warehouse_id": 1,
    "available_quantity": 100,
    "reserved_quantity": 10,
    "damaged_quantity": 2,
    "reorder_level": 20,
    "updated_at": "2026-10-06T10:00:00"
  }
]
```

---

## 8.2 Get Product Inventory

### Endpoint

```http
GET /inventory/{product_id}
```

### Authentication

Required.

### Example

```http
GET /inventory/1
```

### Success Response

**200 OK**

Returns inventory records for the specified product.

---

## 8.3 Adjust Inventory

### Endpoint

```http
POST /inventory/adjust
```

### Authentication

Required.

### Role

```text
admin
warehouse_manager
```

### Required Header

```http
Idempotency-Key: <unique-key>
```

### Request Body

```json
{
  "product_id": 1,
  "warehouse_id": 1,
  "adjustment_amount": 20,
  "reason": "Stock received"
}
```

### Validation

* `product_id` > 0
* `warehouse_id` > 0
* `reason`: 3–255 characters

### Success Response

**200 OK**

```json
{
  "id": 1,
  "product_id": 1,
  "warehouse_id": 1,
  "available_quantity": 120,
  "reserved_quantity": 10,
  "damaged_quantity": 2,
  "reorder_level": 20,
  "updated_at": "2026-10-06T10:00:00"
}
```

### Error

**400 Bad Request**

```json
{
  "detail": "Inventory not found"
}
```

---

## 8.4 Transfer Inventory

### Endpoint

```http
POST /inventory/transfer
```

### Authentication

Required.

### Role

```text
admin
warehouse_manager
```

### Required Header

```http
Idempotency-Key: <unique-key>
```

### Request Body

```json
{
  "product_id": 1,
  "from_warehouse_id": 1,
  "to_warehouse_id": 2,
  "quantity": 10
}
```

### Validation

* `product_id` > 0
* `from_warehouse_id` > 0
* `to_warehouse_id` > 0
* `quantity` > 0

### Success Response

Returns the inventory transfer result.

### Error

**400 Bad Request**

```json
{
  "detail": "Insufficient inventory"
}
```

---

# 9. Order APIs

## 9.1 Create Order

### Endpoint

```http
POST /api/orders
```

### Authentication

Required.

### Required Header

```http
Idempotency-Key: <unique-key>
```

### Request Body

```json
{
  "warehouse_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

### Success Response

**201 Created**

```json
{
  "id": 1,
  "order_number": "ORD-A1B2C3D4",
  "customer_id": 10,
  "warehouse_id": 1,
  "total_amount": 150000,
  "status": "PENDING",
  "payment_status": "PENDING",
  "expected_delivery_date": null,
  "created_at": "2026-10-06T10:00:00",
  "updated_at": "2026-10-06T10:00:00",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "unit_price": 75000,
      "total_price": 150000
    }
  ]
}
```

### Error

**400 Bad Request**

```json
{
  "detail": "Quantity must be greater than zero"
}
```

---

## 9.2 List Customer Orders

### Endpoint

```http
GET /api/orders
```

### Authentication

Required.

### Query Parameters

```text
page
page_size
status
warehouse_id
payment_status
min_total_amount
max_total_amount
customer_id
```

### Example

```http
GET /api/orders?page=1&page_size=20&status=PENDING
```

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "order_number": "ORD-A1B2C3D4",
    "customer_id": 10,
    "warehouse_id": 1,
    "total_amount": 150000,
    "status": "PENDING",
    "payment_status": "PENDING",
    "expected_delivery_date": null,
    "created_at": "2026-10-06T10:00:00",
    "updated_at": "2026-10-06T10:00:00",
    "items": []
  }
]
```

---

## 9.3 Get Order

### Endpoint

```http
GET /api/orders/{order_id}
```

### Authentication

Required.

### Example

```http
GET /api/orders/1
```

### Success Response

**200 OK**

Returns the order details.

### Errors

**404 Not Found**

```json
{
  "detail": "Order not found"
}
```

**403 Forbidden**

```json
{
  "detail": "You are not allowed to view this order"
}
```

---

## 9.4 Confirm Payment

### Endpoint

```http
POST /api/orders/{order_id}/payment-confirm
```

### Authentication

Required.

### Required Header

```http
Idempotency-Key: <unique-key>
```

### Request Body

```json
{
  "payment_reference": "PAY-123456"
}
```

### Success Response

**200 OK**

Returns the updated order.

### Error

**400 Bad Request**

```json
{
  "detail": "Payment confirmation failed"
}
```

---

## 9.5 Confirm Order

### Endpoint

```http
POST /api/orders/{order_id}/confirm
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the confirmed order.

### Error

**400 Bad Request**

```json
{
  "detail": "Only pending orders can be confirmed"
}
```

---

## 9.6 Fulfill Order

### Endpoint

```http
POST /api/orders/{order_id}/fulfill
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the updated order.

### Error

**400 Bad Request**

```json
{
  "detail": "Order cannot be fulfilled"
}
```

---

## 9.7 Ship Order

### Endpoint

```http
POST /api/orders/{order_id}/ship
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the updated order.

---

## 9.8 Deliver Order

### Endpoint

```http
POST /api/orders/{order_id}/deliver
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the delivered order.

---

## 9.9 Return Order

### Endpoint

```http
POST /api/orders/{order_id}/return
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the updated order.

### Error

**400 Bad Request**

```json
{
  "detail": "Order cannot be returned"
}
```

---

## 9.10 Cancel Order

### Endpoint

```http
POST /api/orders/{order_id}/cancel
```

### Authentication

Required.

### Success Response

**200 OK**

Returns the cancelled order.

### Error

**400 Bad Request**

```json
{
  "detail": "Order cannot be cancelled"
}
```

---

## 9.11 Assign Order

### Endpoint

```http
PATCH /api/orders/{order_id}/assign
```

### Authentication

Required.

### Query Parameter

```text
warehouse_id
```

### Example

```http
PATCH /api/orders/1/assign?warehouse_id=2
```

### Success Response

**200 OK**

Returns the assignment result.

### Error

**400 Bad Request**

```json
{
  "detail": "Only confirmed orders can be assigned"
}
```

---

# 10. Return APIs

## 10.1 Create Return Request

### Endpoint

```http
POST /api/returns
```

### Authentication

Required.

### Role

```text
customer
```

### Request Body

```json
{
  "order_id": 1,
  "reason": "Product damaged"
}
```

### Success Response

**201 Created**

```json
{
  "id": 1,
  "order_id": 1,
  "customer_id": 10,
  "reason": "Product damaged",
  "status": "PENDING",
  "created_at": "2026-10-06T10:00:00",
  "updated_at": "2026-10-06T10:00:00"
}
```

### Error

**400 Bad Request**

```json
{
  "detail": "Return cannot be created"
}
```

---

## 10.2 Approve Return

### Endpoint

```http
PATCH /api/returns/{return_id}/approve
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns the approved return.

### Error

**400 Bad Request**

```json
{
  "detail": "Return cannot be approved"
}
```

---

# 11. Notification APIs

## 11.1 Get Notifications

### Endpoint

```http
GET /api/notifications
```

### Authentication

Required.

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "title": "Order Created",
    "message": "Your order has been created successfully.",
    "notification_type": "ORDER_CREATED",
    "is_read": false,
    "created_at": "2026-10-06T10:00:00"
  }
]
```

---

## 11.2 Mark Notification as Read

### Endpoint

```http
PATCH /api/notifications/{notification_id}/read
```

### Authentication

Required.

### Success Response

**200 OK**

```json
{
  "id": 1,
  "title": "Order Created",
  "message": "Your order has been created successfully.",
  "notification_type": "ORDER_CREATED",
  "is_read": true,
  "created_at": "2026-10-06T10:00:00"
}
```

### Error

**404 Not Found**

```json
{
  "detail": "Notification not found"
}
```

---

## 11.3 Mark All Notifications as Read

### Endpoint

```http
PATCH /api/notifications/read-all
```

### Authentication

Required.

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "title": "Order Created",
    "message": "Your order has been created successfully.",
    "notification_type": "ORDER_CREATED",
    "is_read": true,
    "created_at": "2026-10-06T10:00:00"
  }
]
```

---

# 12. Dashboard APIs

## 12.1 Admin Dashboard

### Endpoint

```http
GET /api/dashboard/admin
```

### Authentication

Required.

### Role

```text
admin
```

### Success Response

**200 OK**

Returns admin dashboard information.

---

## 12.2 Warehouse Dashboard

### Endpoint

```http
GET /api/dashboard/warehouse/{warehouse_id}
```

### Authentication

Required.

### Role

```text
warehouse_manager
```

### Example

```http
GET /api/dashboard/warehouse/1
```

### Success Response

**200 OK**

Returns warehouse dashboard information.

---

## 12.3 Customer Dashboard

### Endpoint

```http
GET /api/dashboard/customer/{customer_id}
```

### Authentication

Required.

### Role

```text
customer
```

### Example

```http
GET /api/dashboard/customer/10
```

### Success Response

**200 OK**

Returns customer dashboard information.

---

# 13. Audit Log APIs

## 13.1 List Audit Logs

### Endpoint

```http
GET /api/audit-logs
```

### Authentication

Required.

### Role

```text
admin
```

### Query Parameters

```text
skip
limit
```

### Example

```http
GET /api/audit-logs?skip=0&limit=100
```

### Success Response

**200 OK**

```json
[
  {
    "id": 1,
    "user_id": 1,
    "action": "CREATE",
    "entity": "Order",
    "entity_id": 10,
    "timestamp": "2026-10-06T10:00:00",
    "ip_address": "127.0.0.1",
    "log_metadata": {
      "order_number": "ORD-A1B2C3D4"
    }
  }
]
```

---

# 14. Error Response Format

The application generally returns FastAPI HTTP error responses in the following format:

```json
{
  "detail": "Error message"
}
```

Example:

```json
{
  "detail": "Order not found"
}
```

For validation errors, FastAPI returns HTTP `422`.

Example:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "warehouse_id"
      ],
      "msg": "Field required"
    }
  ]
}
```

---

# 15. Idempotency

Idempotency is implemented to prevent duplicate processing when the same request is submitted multiple times.

The following APIs require an `Idempotency-Key` header:

### Create Order

```http
POST /api/orders
Idempotency-Key: order-123
```

### Confirm Payment

```http
POST /api/orders/{order_id}/payment-confirm
Idempotency-Key: payment-123
```

### Adjust Inventory

```http
POST /inventory/adjust
Idempotency-Key: inventory-adjust-123
```

### Transfer Inventory

```http
POST /inventory/transfer
Idempotency-Key: inventory-transfer-123
```

The same key should not be reused for a different request payload.

Example:

```http
Idempotency-Key: unique-request-001
```

---

# 16. Swagger / OpenAPI Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

### OpenAPI JSON

```text
http://127.0.0.1:8000/openapi.json
```

Swagger can be used to:

* View available endpoints
* View request schemas
* View response schemas
* Authorize using JWT
* Test APIs directly
* Inspect HTTP responses

---

# 17. Postman Collection

The Postman collection should be organized into the following folders:

```text
Order Fulfillment & Inventory Management
│
├── Authentication
│   ├── Register
│   ├── Login
│   ├── Me
│   ├── Refresh Token
│   ├── Logout
│   └── Change Password
│
├── Products
│   ├── Create Product
│   ├── Get Product
│   ├── Update Product
│   ├── Activate Product
│   ├── Deactivate Product
│   └── List Products
│
├── Warehouses
│   ├── Create Warehouse
│   ├── Get Warehouse
│   ├── Update Warehouse
│   ├── Activate Warehouse
│   ├── Deactivate Warehouse
│   └── List Warehouses
│
├── Inventory
│   ├── Get Inventory
│   ├── Get Product Inventory
│   ├── Adjust Inventory
│   └── Transfer Inventory
│
├── Orders
│   ├── Create Order
│   ├── List Orders
│   ├── Get Order
│   ├── Confirm Payment
│   ├── Confirm Order
│   ├── Fulfill Order
│   ├── Ship Order
│   ├── Deliver Order
│   ├── Return Order
│   ├── Cancel Order
│   └── Assign Order
│
├── Returns
│   ├── Create Return
│   └── Approve Return
│
├── Notifications
│   ├── Get Notifications
│   ├── Mark Notification Read
│   └── Mark All Read
│
├── Dashboard
│   ├── Admin Dashboard
│   ├── Warehouse Dashboard
│   └── Customer Dashboard
│
└── Audit Logs
    └── List Audit Logs
```

---

# 18. Authorization Summary

| API Group           |         Admin | Warehouse Manager |      Customer |
| ------------------- | ------------: | ----------------: | ------------: |
| Authentication      |             ✓ |                 ✓ |             ✓ |
| Products            |             ✓ |     Authenticated | Authenticated |
| Warehouses          |             ✓ |     Authenticated | Authenticated |
| Inventory View      |             ✓ |                 ✓ | Authenticated |
| Inventory Adjust    |             ✓ |                 ✓ |             ✗ |
| Inventory Transfer  |             ✓ |                 ✓ |             ✗ |
| Orders              | Authenticated |     Authenticated | Authenticated |
| Create Return       |             ✗ |                 ✗ |             ✓ |
| Approve Return      |             ✓ |                 ✗ |             ✗ |
| Admin Dashboard     |             ✓ |                 ✗ |             ✗ |
| Warehouse Dashboard |             ✗ |                 ✓ |             ✗ |
| Customer Dashboard  |             ✗ |                 ✗ |             ✓ |
| Audit Logs          |             ✓ |                 ✗ |             ✗ |

> Actual business rules inside the service layer determine whether a specific authenticated user can perform an operation.

---

# 19. API Architecture

The application follows a layered architecture:

```text
Client
  ↓
FastAPI Router
  ↓
Dependencies / Authentication / Authorization
  ↓
Service Layer
  ↓
Repository Layer
  ↓
SQLAlchemy Models
  ↓
PostgreSQL
```

### Router

Responsible for:

* Receiving HTTP requests
* Request validation
* Authent
