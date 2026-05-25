-- ============================================================
-- DataPulse Star Schema - Superstore Edition
-- ============================================================

CREATE TABLE IF NOT EXISTS date_dim (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE NOT NULL UNIQUE,
    day         INT,
    month       INT,
    month_name  VARCHAR(20),
    quarter     INT,
    year        INT,
    weekday     VARCHAR(15),
    is_weekend  BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS customer_dim (
    customer_id   VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    segment       VARCHAR(50),
    city          VARCHAR(100),
    state         VARCHAR(100),
    region        VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS product_dim (
    product_id   VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(300),
    category     VARCHAR(100),
    sub_category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS sales_fact (
    id            SERIAL PRIMARY KEY,
    order_id      VARCHAR(50),
    date_id       INT REFERENCES date_dim(date_id),
    customer_id   VARCHAR(20) REFERENCES customer_dim(customer_id),
    product_id    VARCHAR(50) REFERENCES product_dim(product_id),
    quantity      INT,
    total_amount  NUMERIC(12,2),
    discount      NUMERIC(5,2),
    profit        NUMERIC(12,2),
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS etl_logs (
    id          SERIAL PRIMARY KEY,
    pipeline    VARCHAR(100),
    status      VARCHAR(20),
    records_in  INT,
    records_out INT,
    message     TEXT,
    run_at      TIMESTAMP DEFAULT NOW()
);

-- Useful views for Power BI
CREATE OR REPLACE VIEW v_sales_summary AS
SELECT
    d.year,
    d.month_name,
    d.quarter,
    c.segment,
    c.region,
    p.category,
    p.sub_category,
    SUM(f.total_amount) AS total_sales,
    SUM(f.profit)       AS total_profit,
    SUM(f.quantity)     AS total_quantity,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM sales_fact f
JOIN date_dim     d ON f.date_id     = d.date_id
JOIN customer_dim c ON f.customer_id = c.customer_id
JOIN product_dim  p ON f.product_id  = p.product_id
GROUP BY d.year, d.month_name, d.quarter, c.segment, c.region, p.category, p.sub_category;
