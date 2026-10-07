# Database Setup Instructions

This document explains how to configure PostgreSQL and connect it with the **Order Fulfillment & Inventory Management Platform**.

## 1. Prerequisites

Install the following:

* PostgreSQL
* Python 3.11+
* pip
* Virtual Environment
* Alembic

Verify PostgreSQL installation:

```bash
psql --version
```

Verify Python:

```bash
python --version
```

---

## 2. Create PostgreSQL Database

Open PostgreSQL using `psql` or **pgAdmin**.

Create the database:

```sql
CREATE DATABASE order_fulfillment_db;
```

Verify the database:

```sql
\l
```

Connect to the database:

```sql
\c order_fulfillment_db
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/order_fulfillment_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Database URL Format

```text
postgresql://<username>:<password>@<host>:<port>/<database_name>
```

Example:

```text
postgresql://postgres:password@localhost:5432/order_fulfillment_db
```

> Do not commit the `.env` file to GitHub. Use `.env.example` for sharing configuration structure.

---

## 4. Install Database Dependencies

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

The project uses:

* SQLAlchemy
* psycopg2-binary
* Alembic
* Pydantic Settings

---

## 5. Configure SQLAlchemy

The application uses SQLAlchemy to connect FastAPI with PostgreSQL.

The database configuration is located inside the application database module.

The connection uses the `DATABASE_URL` value from `.env`.

General flow:

```text
.env
  ↓
DATABASE_URL
  ↓
SQLAlchemy Engine
  ↓
SessionLocal
  ↓
FastAPI Dependencies
  ↓
PostgreSQL
```

---

## 6. Configure Alembic

Alembic is used for database schema migrations.

The project contains:

```text
alembic/
├── versions/
├── env.py
└── ...
```

The database URL is configured through the application's environment settings.

---

## 7. Run Database Migrations

After configuring the database, run:

```bash
alembic upgrade head
```

This creates all required database tables.

Check the current migration:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

---

## 8. Create a New Migration

Whenever a database model is changed:

```bash
alembic revision --autogenerate -m "update database model"
```

Review the generated migration file before applying it.

Then run:

```bash
alembic upgrade head
```

---

## 9. Rollback Migration

To rollback the latest migration:

```bash
alembic downgrade -1
```

To downgrade to a specific revision:

```bash
alembic downgrade <revision_id>
```

---

## 10. Main Database Tables

The application contains the following major tables:

```text
users
products
warehouses
inventory
inventory_transactions
orders
order_items
returns
notifications
audit_logs
```

### Users

Stores user authentication and authorization information.

Important fields:

* id
* name
* email
* password
* role
* is_active
* created_at

### Products

Stores product information.

Important fields:

* id
* name
* description
* price
* sku
* is_active

### Warehouses

Stores warehouse information.

Important fields:

* id
* name
* location
* is_active

### Inventory

Stores product stock information for each warehouse.

Important fields:

* id
* product_id
* warehouse_id
* available_quantity
* reserved_quantity
* damaged_quantity
* reorder_level
* updated_at

### Inventory Transactions

Stores inventory movement history.

Examples:

* PURCHASE
* SALE
* RESERVATION
* RELEASE
* ADJUSTMENT
* TRANSFER_IN
* TRANSFER_OUT
* RETURN
* DAMAGE

### Orders

Stores customer order information.

Important fields:

* id
* order_number
* customer_id
* warehouse_id
* total_amount
* status
* payment_status
* expected_delivery_date
* created_at

### Order Items

Stores products included in an order.

Important fields:

* id
* order_id
* product_id
* quantity
* unit_price
* total_price

### Returns

Stores order return requests.

Important fields:

* id
* order_id
* customer_id
* reason
* status
* created_at
* updated_at

### Notifications

Stores system notifications.

Important fields:

* id
* user_id
* title
* message
* notification_type
* is_read
* created_at

### Audit Logs

Stores important system activity.

Important fields:

* id
* user_id
* action
* entity_type
* entity_id
* created_at

---

## 11. Database Relationships

The major relationships are:

```text
USERS
  │
  ├──< ORDERS
  │      │
  │      └──< ORDER_ITEMS >── PRODUCTS
  │
  ├──< RETURNS >── ORDERS
  │
  ├──< NOTIFICATIONS
  │
  └──< AUDIT_LOGS

PRODUCTS
  │
  ├──< INVENTORY >── WAREHOUSES
  │
  ├──< INVENTORY_TRANSACTIONS
  │
  └──< ORDER_ITEMS
```

The complete ER Diagram is available at:

```text
docs/ER_Diagram.png
```

---

## 12. Verify Database Tables

Connect to PostgreSQL:

```bash
psql -U postgres -d order_fulfillment_db
```

List all tables:

```sql
\dt
```

View table structure:

```sql
\d users
```

For example:

```sql
\d orders
```

---

## 13. Run the Application

After completing the database setup:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 14. Database Setup Flow

```text
Install PostgreSQL
        ↓
Create Database
        ↓
Configure .env
        ↓
Install Python Dependencies
        ↓
Configure Alembic
        ↓
Run alembic upgrade head
        ↓
Verify Tables
        ↓
Start FastAPI Application
```

## 15. Troubleshooting

### Database Connection Error

Check:

* PostgreSQL service is running
* Database name is correct
* Username is correct
* Password is correct
* Port is correct
* `DATABASE_URL` is correctly configured

Default PostgreSQL port:

```text
5432
```

### Migration Error

Check the current migration:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

Then run:

```bash
alembic upgrade head
```

### Table Does Not Exist

Run:

```bash
alembic upgrade head
```

Then verify:

```sql
\dt
```

## 16. Security Notes

* Never commit `.env` to GitHub.
* Never expose the PostgreSQL password in source code.
* Use a strong `SECRET_KEY`.
* Use different credentials for development and production.
* Restrict database access in production environments.
