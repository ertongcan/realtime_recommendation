DROP TABLE IF EXISTS user_views;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS recommended_user_products;

CREATE TABLE products(
   product_id   INT NOT NULL,
   category_id INT NOT NULL,
   PRIMARY KEY(product_id)
);

CREATE TABLE orders(
   order_id INT GENERATED ALWAYS AS IDENTITY,
   user_id INT NOT NULL,
   PRIMARY KEY(order_id)
);

CREATE TABLE order_items(
   id INT GENERATED ALWAYS AS IDENTITY,
   order_id INT NOT NULL,
   product_id   INT NOT NULL,
   quantity INT NOT NULL,
   PRIMARY KEY(id),
   CONSTRAINT fk_order
      FOREIGN KEY(order_id)
	  REFERENCES orders(order_id),
    CONSTRAINT fk_product
      FOREIGN KEY(product_id)select count(1) from products;

	  REFERENCES products(product_id)
);

CREATE TABLE user_views(
   id INT GENERATED ALWAYS AS IDENTITY,
   user_id INT NOT NULL,
   user_event VARCHAR(255) NOT NULL,
   user_event_source VARCHAR(255) NOT NULL,
   user_event_date VARCHAR(255) NOT NULL,
   product_id   INT NOT NULL
);

CREATE TABLE recommended_user_products(
   id INT GENERATED ALWAYS AS IDENTITY,
   user_id INT NOT NULL,
   product_id   INT NOT NULL
);

