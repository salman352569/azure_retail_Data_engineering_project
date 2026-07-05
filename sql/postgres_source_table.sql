CREATE SCHEMA IF NOT EXISTS retail;

CREATE TABLE retail.customer (
    customer_id VARCHAR PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE retail.products (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE retail.order (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR(100),
    order_date VARCHAR(50),
    channel VARCHAR(50),
    status VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);



CREATE TABLE retail.order_items (
    order_item_id VARCHAR PRIMARY KEY,
    order_id VARCHAR(100),
    product_id VARCHAR(50),
    quantity VARCHAR(50),
    sales_amount VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

create table retail.watermark(
table_name varchar(100) PRIMARY KEY 
last_load_timestamp TIMESTAMP
);

INSERT TNTO retail.watermark VALUES(
('customers','1900-01-01'),
('products','1900-01-01'),
('orders','1900-01-01'),
('order_items','1900-01-01');

update retail.watermark
SET last_load_time = (
SELECT MAX(updated_at)
FROM reatil.cutomers
)
WHERE table_name ='customers';
