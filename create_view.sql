CREATE OR REPLACE VIEW v_restaurant_sales_summary AS
WITH sales_data AS (
    SELECT
        restaurant_id,
        COUNT(id) AS total_orders,
        SUM(total_amount) AS total_revenue
    FROM orders
    WHERE status = 'Completed'
    GROUP BY restaurant_id
)
SELECT
    r.location_name,
    sd.total_orders,
    sd.total_revenue
FROM restaurants r
JOIN sales_data sd ON r.id = sd.restaurant_id;