
USE merchant_risk_db;

-- 1. M048 Overall Risk Summary
SELECT
    merchant_id,
    COUNT(*) AS total_transactions,
    SUM(status = 'Failed') AS failed_transactions,
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS failed_rate,
    SUM(is_refund = 1) AS refund_transactions,
    ROUND(
        SUM(is_refund = 1) * 100.0 / COUNT(*), 2
    ) AS refund_rate
FROM transactions
WHERE merchant_id = 'M048'
GROUP BY merchant_id;


-- 2. M048 Payment Method Analysis
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(status = 'Failed') AS failed_transactions,
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS failed_rate
FROM transactions
WHERE merchant_id = 'M048'
GROUP BY payment_method
ORDER BY failed_rate DESC;


-- 3. M048 Hourly Transaction Analysis
SELECT
    HOUR(transaction_time) AS transaction_hour,
    COUNT(*) AS total_transactions,
    SUM(status = 'Failed') AS failed_transactions,
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS failed_rate
FROM transactions
WHERE merchant_id = 'M048'
GROUP BY HOUR(transaction_time)
ORDER BY transaction_hour;


-- 4. M048 Transaction Amount by Status
SELECT
    status,
    COUNT(*) AS total_transactions,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(MIN(amount), 2) AS minimum_amount,
    ROUND(MAX(amount), 2) AS maximum_amount,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
WHERE merchant_id = 'M048'
GROUP BY status;


-- 5. M048 Failed Transactions by Payment Method
SELECT
    payment_method,
    COUNT(*) AS failed_transactions,
    ROUND(AVG(amount), 2) AS average_failed_amount,
    ROUND(SUM(amount), 2) AS total_failed_amount
FROM transactions
WHERE merchant_id = 'M048'
  AND status = 'Failed'
GROUP BY payment_method
ORDER BY failed_transactions DESC;


-- 6. M048 Failed Transaction Detail
SELECT
    transaction_id,
    merchant_id,
    transaction_time,
    payment_method,
    amount,
    status
FROM transactions
WHERE merchant_id = 'M048'
  AND status = 'Failed'
ORDER BY amount DESC;


-- 7. M048 Payment Method vs System Average
SELECT
    payment_method,
    COUNT(*) AS system_transactions,
    SUM(status = 'Failed') AS system_failed_transactions,
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS system_failed_rate
FROM transactions
GROUP BY payment_method
ORDER BY system_failed_rate DESC;
