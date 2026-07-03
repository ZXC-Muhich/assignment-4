# assignment-4

**Database schema for my business**
```
    RESTAURANTS {
        UUID id PK
        VARCHAR location_name
        VARCHAR address
        BOOLEAN is_drive_thru
    }

    CUSTOMERS {
        UUID id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR phone
    }

    LOYALTY_CARDS {
        UUID id PK
        UUID customer_id FK
        INT points
        DATE issue_date
    }

    MENU_ITEMS {
        UUID id PK
        VARCHAR name
        VARCHAR category
        DECIMAL price
        INT calories
    }

    ORDERS {
        UUID id PK
        UUID restaurant_id FK
        UUID customer_id FK
        TIMESTAMP order_date
        DECIMAL total_amount
        VARCHAR status
    }

    ORDER_ITEMS {
        UUID order_id FK
        UUID menu_item_id FK
        INT quantity
        DECIMAL item_price
    }

    CUSTOMERS ||--|| LOYALTY_CARDS: "owns (1:1)"
    RESTAURANTS ||--o{ ORDERS: "receives (1:M)"
    CUSTOMERS ||--o{ ORDERS: "places (1:M)"
    ORDERS ||--o{ ORDER_ITEMS: "contains"
    MENU_ITEMS ||--o{ ORDER_ITEMS: "included in"
```

**Index optimization demonstration**

```
EXPLAIN ANALYZE 
SELECT * FROM orders 
WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31';
```

**Before Indexes**
<img width="1166" height="411" alt="image" src="https://github.com/user-attachments/assets/7d82d4ee-652c-4843-b2a2-26a7df9eec0c" />

**After Indexes**
<img width="1253" height="365" alt="image" src="https://github.com/user-attachments/assets/7b2ebb05-ae6b-4fd1-bfa9-56760d3eb00a" />


**Indexes**

```
CREATE INDEX idx_orders_order_date ON orders(order_date);
```
