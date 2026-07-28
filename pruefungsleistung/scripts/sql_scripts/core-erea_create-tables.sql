
CREATE TABLE core.category(
	sub_category TEXT NOT NULL PRIMARY KEY,
	category TEXT
);

CREATE TABLE core.product(
	product_id TEXT NOT NULL PRIMARY KEY,
	sub_category TEXT NOT NULL REFERENCES core.category(sub_category),
	product_name TEXT
);

CREATE TABLE core.location(
	postal_code TEXT NOT NULL PRIMARY KEY,
	city TEXT,
	"state" TEXT,
	country TEXT,
	region TEXT
);

CREATE TABLE core.customer(
	customer_id TEXT NOT NULL PRIMARY KEY,
	customer_name TEXT,
	segment TEXT
);
CREATE TABLE core.orders(
	order_id TEXT NOT NULL PRIMARY KEY,
	customer_id TEXT NOT NULL REFERENCES core.customer(customer_id),
	postal_code TEXT NOT NULL REFERENCES core.location(postal_code),
	order_date DATE,
	ship_date DATE,
	ship_mode TEXT
);

CREATE TABLE core.bruecken_tabelle (
	order_id TEXT NOT NULL REFERENCES core.orders(order_id),
	product_id TEXT NOT NULL REFERENCES core.product(product_id),
	Sales NUMERIC(10, 2),
	PRIMARY KEY (order_id, product_id)
);