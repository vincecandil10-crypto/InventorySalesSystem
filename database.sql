CREATE DATABASE IF NOT EXISTS inventory_system;

USE inventory_system;

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    status VARCHAR(20) NOT NULL
		
 );       
        
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);        

USE inventory_system;

SELECT * FROM sales;
 
 SELECT product_id, product_name, stock, status
FROM products;


SELECT COUNT(*) AS total_products
FROM products;

SELECT * FROM inventory_system.products;

USE inventory_system;

SELECT COUNT(*) AS total_products
FROM products;

SELECT *
FROM products
ORDER BY product_id;

USE inventory_system;

SELECT COUNT(*) AS total_products
FROM products;

SELECT product_id, product_name, category, price, stock, status
FROM products
ORDER BY product_id DESC
LIMIT 10;


USE inventory_system;

SELECT
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM sales) AS total_sales;