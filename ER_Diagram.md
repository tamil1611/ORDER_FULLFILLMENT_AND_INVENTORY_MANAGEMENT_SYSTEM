┌──────────────────────┐
│        USERS         │
├──────────────────────┤
│ PK id                │
│ name                 │
│ email                │
│ password             │
│ role                 │
│ is_active            │
│ created_at           │
└──────────┬───────────┘
           │
     ┌─────┼───────────────┬──────────────────┐
     │     │               │                  │
     │     │               │                  │
     ▼     ▼               ▼                  ▼
┌────────┐ ┌────────────┐ ┌────────────────┐ ┌──────────────┐
│ ORDERS │ │  RETURNS   │ │ NOTIFICATIONS  │ │ AUDIT_LOGS   │
├────────┤ ├────────────┤ ├────────────────┤ ├──────────────┤
│PK id   │ │PK id       │ │PK id           │ │PK id         │
│order_id│ │order_id FK │ │user_id FK      │ │user_id FK    │
│customer│ │customer FK │ │title           │ │action        │
│warehouse││reason      │ │message         │ │entity_type   │
│total   │ │status      │ │type            │ │entity_id     │
│status  │ │created_at  │ │is_read         │ │created_at    │
└────┬───┘ └────────────┘ │created_at      │ └──────────────┘
     │                    └────────────────┘
     │
     ▼
┌──────────────────────┐
│     ORDER_ITEMS      │
├──────────────────────┤
│ PK id                │
│ order_id FK          │
│ product_id FK        │
│ quantity             │
│ unit_price           │
│ total_price          │
└──────────┬───────────┘
           │
           │
           ▼
┌──────────────────────┐
│       PRODUCTS       │
├──────────────────────┤
│ PK id                │
│ name                 │
│ description          │
│ price                │
│ sku                  │
│ is_active            │
└──────────┬───────────┘
           │
      ┌────┴───────────────┐
      │                    │
      ▼                    ▼
┌──────────────────┐   ┌────────────────────────┐
│    INVENTORY     │   │ INVENTORY_TRANSACTIONS │
├──────────────────┤   ├────────────────────────┤
│ PK id            │   │ PK id                  │
│ product_id FK    │   │ product_id FK          │
│ warehouse_id FK  │   │ warehouse_id FK        │
│ available_qty    │   │ transaction_type       │
│ reserved_qty     │   │ quantity               │
│ damaged_qty      │   │ reference_id           │
│ reorder_level    │   │ created_at             │
│ updated_at       │   └───────────┬────────────┘
└────────┬─────────┘               │
         │                         │
         └──────────┬──────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │    WAREHOUSES    │
           ├──────────────────┤
           │ PK id            │
           │ name             │
           │ location         │
           │ is_active        │
           └──────────────────┘



##Relationship

USERS
 ├── 1 : N → ORDERS
 ├── 1 : N → RETURNS
 ├── 1 : N → NOTIFICATIONS
 └── 1 : N → AUDIT_LOGS

ORDERS
 └── 1 : N → ORDER_ITEMS

PRODUCTS
 ├── 1 : N → ORDER_ITEMS
 ├── 1 : N → INVENTORY
 └── 1 : N → INVENTORY_TRANSACTIONS

WAREHOUSES
 ├── 1 : N → INVENTORY
 ├── 1 : N → INVENTORY_TRANSACTIONS
 └── 1 : N → ORDERS

ORDERS
 └── 1 : N → RETURNS