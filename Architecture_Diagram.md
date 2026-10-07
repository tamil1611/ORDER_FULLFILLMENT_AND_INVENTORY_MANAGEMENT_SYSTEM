                    ┌──────────────────────┐
                    │       CLIENT         │
                    │  Postman / Frontend  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FASTAPI        │
                    │    Application       │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌──────────────┐
       │   AUTH     │   │   ORDERS   │   │  INVENTORY   │
       │   ROUTER   │   │   ROUTER   │   │    ROUTER    │
       └─────┬──────┘   └─────┬──────┘   └──────┬───────┘
             │                │                 │
             └────────────────┼─────────────────┘
                              ▼
                    ┌──────────────────────┐
                    │      SERVICES        │
                    ├──────────────────────┤
                    │ Auth Service         │
                    │ Order Service        │
                    │ Inventory Service    │
                    │ Return Service       │
                    │ Notification Service │
                    │ Audit Service        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     REPOSITORIES      │
                    ├──────────────────────┤
                    │ User Repository       │
                    │ Product Repository    │
                    │ Order Repository      │
                    │ Inventory Repository │
                    │ Return Repository     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     SQLALCHEMY       │
                    │         ORM          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      POSTGRESQL      │
                    ├──────────────────────┤
                    │ Users                │
                    │ Products             │
                    │ Warehouses           │
                    │ Inventory            │
                    │ Orders               │
                    │ Order Items          │
                    │ Returns              │
                    │ Notifications        │
                    │ Audit Logs           │
                    └──────────────────────┘


## Supporting Components

┌──────────────────┐
│    SECURITY      │
├──────────────────┤
│ JWT              │
│ RBAC             │
│ Password Hashing │
│ Validation       │
└──────────────────┘

        │

┌──────────────────┐
│     ALEMBIC      │
├──────────────────┤
│ Database         │
│ Migrations       │
└──────────────────┘

        │

┌──────────────────┐
│      TESTS       │
├──────────────────┤
│ Pytest           │
│ API Testing      │
└──────────────────┘

## Main flow:

Client
  ↓
FastAPI
  ↓
Routers
  ↓
Services
  ↓
Repositories
  ↓
SQLAlchemy
  ↓
PostgreSQL