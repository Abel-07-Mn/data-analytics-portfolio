PRAGMA foreign_keys = OFF;

CREATE TABLE IF NOT EXISTS marketing_qualified_leads (
    mql_id TEXT PRIMARY KEY,
    first_contact_date TEXT,
    origin TEXT
);

CREATE TABLE IF NOT EXISTS closed_deals (
    mql_id TEXT PRIMARY KEY,
    seller_id TEXT,
    won_date TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    price REAL
);

CREATE TABLE IF NOT EXISTS order_reviews (
    order_id TEXT NOT NULL,
    review_score INTEGER
);

CREATE INDEX IF NOT EXISTS idx_closed_deals_seller ON closed_deals(seller_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_seller ON order_items(seller_id);
CREATE INDEX IF NOT EXISTS idx_orders_purchase ON orders(order_purchase_timestamp);
CREATE INDEX IF NOT EXISTS idx_reviews_order ON order_reviews(order_id);