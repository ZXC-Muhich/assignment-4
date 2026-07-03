# Assignment 4

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
<img width="881" height="746" alt="image" src="https://github.com/user-attachments/assets/2ef8120d-5b13-4917-b774-b0e9ed2adb24" />


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

**Trigger**
```
CREATE TRIGGER trg_after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_order_total();
```
**Function that will be called by trigger**
```
CREATE OR REPLACE FUNCTION update_order_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders
    SET total_amount = total_amount + (NEW.quantity * NEW.item_price)
    WHERE id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Procedure**
```
CREATE OR REPLACE PROCEDURE add_loyalty_points(
    p_customer_id UUID, 
    p_points_to_add INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_points_to_add <= 0 THEN
        RAISE EXCEPTION 'Points to add must be greater than zero';
    END IF;

    UPDATE loyalty_cards
    SET points = points + p_points_to_add
    WHERE customer_id = p_customer_id;
    
    COMMIT;
END;
$$;
```
