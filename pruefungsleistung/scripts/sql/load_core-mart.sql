--UPDATE mart.product_dim---
INSERT INTO mart.product_dim (product_id, product_name, sub_category, category)

SELECT
	p.product_id, p.product_name, p.sub_category, 
	pd.category
	
FROM core.product AS p

JOIN core.category AS pd ON p.sub_category = pd.sub_category

ON CONFLICT (product_id)

DO UPDATE SET
	product_name = EXCLUDED.product_name,
	sub_category = EXCLUDED.sub_category,
	category = EXCLUDED.category;

--UPDATE mart.shipping_dim---
INSERT INTO mart.shipping_dim (order_id, order_date, ship_date, ship_mode, delivery_days)

SELECT
	o.order_id, o.order_date, o.ship_date, o.ship_mode,
	o.ship_date - o.order_date AS delivery_days

FROM core.orders AS o

ON CONFLICT (order_id)

DO UPDATE SET
	order_date = EXCLUDED.order_date,
	ship_date = EXCLUDED.ship_date,
	ship_mode = EXCLUDED.ship_mode,
	delivery_days = EXCLUDED.delivery_days;
	

--UPDATE mart.location---
INSERT INTO mart.location_dim(postal_code, city, "state", region)

SELECT
	l.postal_code, l.city, l.state, l.region
	
FROM core.location AS l

ON CONFLICT (postal_code)

DO UPDATE SET
	postal_code = EXCLUDED.postal_code,
	city = EXCLUDED.city,
	"state" = EXCLUDED.state,
	region = EXCLUDED.region;

--UPDATE mart.location---
INSERT INTO mart.customer_dim(customer_id, customer_name, segment)

SELECT
	cu.customer_id, cu.customer_name, cu.segment
	
FROM core.customer AS cu

ON CONFLICT (customer_id)

DO UPDATE SET
	customer_name = EXCLUDED.customer_name,
	segment = EXCLUDED.segment;

--UPDATE mart.main_table---
INSERT INTO mart.main_table(order_id, product_id, sales, postal_code, customer_id)
SELECT
    bt.order_id, bt.product_id, bt.sales,
    lo.postal_code,
    cus.customer_id

FROM core.bruecken_tabelle AS bt



JOIN core.orders AS ors ON bt.order_id = ors.order_id
JOIN core.customer AS cus ON ors.customer_id = cus.customer_id
JOIN core.location AS lo ON ors.postal_code = lo.postal_code


ON CONFLICT (order_id, product_id)
DO UPDATE SET
    sales = EXCLUDED.sales,
    postal_code = EXCLUDED.postal_code,
    customer_id = EXCLUDED.customer_id;
    