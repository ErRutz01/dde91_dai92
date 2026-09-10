--customer_lifespan berechnen--

UPDATE mart.customer_dim as mc

SET customer_lifespan = agg.customer_lifespan
FROM(
	SELECT
	customer_id,
	COUNT(DISTINCT EXTRACT(year FROM co.order_date)) AS customer_lifespan
	FROM core.orders AS co
	GROUP BY customer_id
) AS agg
WHERE mc.customer_id = agg.customer_id;

--puchase_frequency berechnen--
UPDATE mart.customer_dim as mc

SET purchase_frequency = agg.purchase_frequency
	
FROM (
	SELECT
		customer_id,
		COUNT(DISTINCT co.order_id)::NUMERIC(10, 2) / COUNT(DISTINCT EXTRACT(year FROM co.order_date)) AS purchase_frequency
	FROM core.orders AS co
	GROUP BY customer_id
	) AS agg

WHERE mc.customer_id = agg.customer_id;


--avrg_purchase_value berechnen--
UPDATE mart.customer_dim as mc

SET avrg_purchase_value = agg.avrg_purchase_value
FROM(
	SELECT
		co.customer_id,
		SUM(bt.sales)::NUMERIC(10, 2)/COUNT(DISTINCT co.order_id) AS avrg_purchase_value
	FROM core.orders AS co
	JOIN core.bruecken_tabelle AS bt ON co.order_id = bt.order_id
	GROUP BY customer_id
	) AS agg
WHERE mc.customer_id = agg.customer_id;


--clv berechnen--
UPDATE mart.customer_dim as mc

SET clv = agg.clv
FROM(
	SELECT
		co.customer_id,
		LN(SUM(bt.sales)+1) AS clv
		FROM core.orders AS co
		JOIN core.bruecken_tabelle AS bt ON co.order_id = bt.order_id
		GROUP BY customer_id
) AS agg
WHERE mc.customer_id = agg.customer_id;


--delivery_days berechnen--

