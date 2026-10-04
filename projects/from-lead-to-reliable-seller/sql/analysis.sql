DROP VIEW IF EXISTS source_funnel;
DROP VIEW IF EXISTS mature_closed_sellers;
DROP VIEW IF EXISTS activated_sellers_90d;
DROP VIEW IF EXISTS early_fulfillment_orders_90d;

-- Preserve the qualified-lead grain and keep unattributed leads visible.
CREATE TEMP VIEW source_funnel AS
SELECT
    COALESCE(NULLIF(TRIM(m.origin), ''), 'unknown') AS origin,
    COUNT(DISTINCT m.mql_id) AS qualified_leads,
    COUNT(DISTINCT d.mql_id) AS closed_deals
FROM marketing_qualified_leads AS m
LEFT JOIN closed_deals AS d
    ON d.mql_id = m.mql_id
GROUP BY COALESCE(NULLIF(TRIM(m.origin), ''), 'unknown');

-- Exclude deals whose sellers do not have a complete 90-day observation window.
-- The cutoff is derived from the latest observed customer-delivery timestamp.
CREATE TEMP VIEW mature_closed_sellers AS
SELECT
    d.mql_id,
    d.seller_id,
    COALESCE(NULLIF(TRIM(m.origin), ''), 'unknown') AS origin,
    datetime(d.won_date) AS won_at,
    datetime(d.won_date, '+90 days') AS activation_deadline
FROM closed_deals AS d
JOIN marketing_qualified_leads AS m
    ON m.mql_id = d.mql_id
WHERE d.seller_id IS NOT NULL
  AND d.won_date IS NOT NULL
  AND datetime(d.won_date) <= datetime(
      (SELECT MAX(order_delivered_customer_date) FROM orders),
      '-90 days'
  );

-- Activation means at least one order purchased after the deal was won,
-- delivered, and delivered within 90 days of the win date.
CREATE TEMP VIEW activated_sellers_90d AS
SELECT
    c.mql_id,
    c.seller_id,
    c.origin,
    MIN(
        julianday(o.order_delivered_customer_date) - julianday(c.won_at)
    ) AS days_to_first_delivered_order,
    COUNT(DISTINCT o.order_id) AS delivered_orders_90d,
    SUM(i.price) AS delivered_item_value_90d
FROM mature_closed_sellers AS c
JOIN order_items AS i
    ON i.seller_id = c.seller_id
JOIN orders AS o
    ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
  AND datetime(o.order_purchase_timestamp) >= c.won_at
  AND datetime(o.order_delivered_customer_date) <= c.activation_deadline
GROUP BY c.mql_id, c.seller_id, c.origin;

-- Order-level delivery and review measures are attributed only when one seller
-- supplied the order. This avoids assigning a shared order outcome to several
-- sellers when an order contains items from multiple sellers.
CREATE TEMP VIEW early_fulfillment_orders_90d AS
WITH one_seller_orders AS (
    SELECT
        order_id,
        MIN(seller_id) AS seller_id
    FROM order_items
    GROUP BY order_id
    HAVING COUNT(DISTINCT seller_id) = 1
),
reviews_by_order AS (
    SELECT
        order_id,
        AVG(CAST(review_score AS REAL)) AS mean_review_score
    FROM order_reviews
    WHERE review_score BETWEEN 1 AND 5
    GROUP BY order_id
)
SELECT
    c.mql_id,
    c.seller_id,
    c.origin,
    o.order_id,
    CASE
        WHEN date(o.order_delivered_customer_date)
             <= date(o.order_estimated_delivery_date) THEN 1
        ELSE 0
    END AS on_time,
    r.mean_review_score
FROM mature_closed_sellers AS c
JOIN one_seller_orders AS s
    ON s.seller_id = c.seller_id
JOIN orders AS o
    ON o.order_id = s.order_id
LEFT JOIN reviews_by_order AS r
    ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= c.won_at
  AND o.order_delivered_customer_date <= c.activation_deadline
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL;