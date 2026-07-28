
CREATE TABLE mart.product_dim(
    product_id TEXT NOT NULL PRIMARY KEY,
    product_name TEXT,
	sub_category TEXT,
	category TEXT
);

CREATE TABLE mart.standort_dim(
	postal_code INT NOT NULL PRIMARY KEY,
	city TEXT,
	"state" TEXT,
	region TEXT
);

CREATE TABLE mart.customer_dim(
	customer_id TEXT NOT NULL PRIMARY KEY,
	customer_name TEXT,
	segment TEXT,
    avrg_purchase_value NUMERIC(10, 2),
    purchase_frequency NUMERIC(10, 2),
    clv NUMERIC(10, 2),
    customer_lifespan NUMERIC(10, 2)

);
CREATE TABLE mart.shipping_dim(
	order_id TEXT NOT NULL PRIMARY KEY,
	order_date DATE,
	ship_date DATE,
	ship_mode TEXT,
    delivery_days INT
);

CREATE TABLE mart.main_table (
	order_id TEXT NOT NULL REFERENCES mart.shipping_dim(order_id),
	product_id TEXT NOT NULL REFERENCES mart.product_dim(product_id),
	sales NUMERIC(10, 2),
    postal_code TEXT NOT NULL REFERENCES mart.standort_dim(postal_code),
    customer_id TEXT NOT NULL REFERENCES mart.customer_dim(customer_id),
    country TEXT,
	PRIMARY KEY (order_id, product_id)
);