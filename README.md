# assignment-4

**Database schema for my business**

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
