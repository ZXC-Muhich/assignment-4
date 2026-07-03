DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mcd_admin') THEN
        CREATE ROLE mcd_admin LOGIN PASSWORD 'AdminPass123!';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE mcdonalds TO mcd_admin;
GRANT USAGE ON SCHEMA public TO mcd_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mcd_admin;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mcd_analyst') THEN
        CREATE ROLE mcd_analyst LOGIN PASSWORD 'AnalystPass123!';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE mcdonalds TO mcd_analyst;
GRANT USAGE ON SCHEMA public TO mcd_analyst;
GRANT SELECT ON v_restaurant_sales_summary TO mcd_analyst;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mcd_manager') THEN
        CREATE ROLE mcd_manager LOGIN PASSWORD 'ManagerPass123!';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE mcdonalds TO mcd_manager;
GRANT USAGE ON SCHEMA public TO mcd_manager;
GRANT SELECT, INSERT, UPDATE ON orders, order_items TO mcd_manager;