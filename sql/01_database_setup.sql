CREATE DATABASE merchant_risk_db; 
SHOW DATABASES;
SHOW DATABASES LIKE 'merchant_risk_db';
USE merchant_risk_db;
CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    merchant_id VARCHAR(10),
    customer_id VARCHAR(20),
    transaction_time DATETIME,
    amount DECIMAL(12,2),
    payment_method VARCHAR(30),
    status VARCHAR(20),
    is_refund BOOLEAN,
    scenario_label VARCHAR(30)
);
DESCRIBE transactions;
CREATE TABLE merchants (
    merchant_id VARCHAR(10) PRIMARY KEY,
    merchant_name VARCHAR(100),
    business_category VARCHAR(50),
    registration_date DATE,
    account_status VARCHAR(20)
);
DESCRIBE merchants;
SELECT COUNT(*) AS total_transactions
FROM transactions;
SELECT * FROM transactions LIMIT 5;
SHOW VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'local_infile';