
USE merchant_risk_db;

-- 1. Overall Transaction Performance
SELECT
    COUNT(*) AS total_transactions,
    SUM(status = 'Failed') AS failed_transactions,
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS failed_rate,
    SUM(is_refund = 1) AS refund_transactions,
    ROUND(
        SUM(is_refund = 1) * 100.0 / COUNT(*), 2
    ) AS refund_rate
FROM transactions;


-- 2. Merchant-level Risk Analysis
SELECT
    m.merchant_id,
    m.merchant_name,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.status = 'Failed') AS failed_transactions,
    ROUND(
        SUM(t.status = 'Failed') * 100.0 /
        COUNT(t.transaction_id), 2
    ) AS failed_rate,
    SUM(t.is_refund = 1) AS refund_transactions,
    ROUND(
        SUM(t.is_refund = 1) * 100.0 /
        COUNT(t.transaction_id), 2
    ) AS refund_rate
FROM merchants m
JOIN transactions t
    ON m.merchant_id = t.merchant_id
GROUP BY m.merchant_id, m.merchant_name
ORDER BY failed_rate DESC;


-- 3. System Average by Transaction
SELECT
    ROUND(
        SUM(status = 'Failed') * 100.0 / COUNT(*), 2
    ) AS system_failed_rate,
    ROUND(
        SUM(is_refund = 1) * 100.0 / COUNT(*), 2
    ) AS system_refund_rate
FROM transactions;


-- 4. Merchant Risk Classification
WITH system_avg AS (
    SELECT
        SUM(status = 'Failed') * 100.0 / COUNT(*) AS avg_failed_rate,
        SUM(is_refund = 1) * 100.0 / COUNT(*) AS avg_refund_rate
    FROM transactions
),
merchant_metrics AS (
    SELECT
        merchant_id,
        COUNT(*) AS total_transactions,
        SUM(status = 'Failed') AS failed_transactions,
        SUM(is_refund = 1) AS refund_transactions,
        SUM(status = 'Failed') * 100.0 / COUNT(*) AS failed_rate,
        SUM(is_refund = 1) * 100.0 / COUNT(*) AS refund_rate
    FROM transactions
    GROUP BY merchant_id
)
SELECT
    mm.merchant_id,
    mm.total_transactions,
    mm.failed_transactions,
    ROUND(mm.failed_rate, 2) AS failed_rate,
    ROUND(mm.refund_rate, 2) AS refund_rate,
    CASE
        WHEN mm.failed_rate > sa.avg_failed_rate
         AND mm.refund_rate > sa.avg_refund_rate
            THEN 'Both Above Average'
        WHEN mm.failed_rate > sa.avg_failed_rate
            THEN 'Failed Only'
        WHEN mm.refund_rate > sa.avg_refund_rate
            THEN 'Refund Only'
        ELSE 'Within Average'
    END AS risk_category
FROM merchant_metrics mm
CROSS JOIN system_avg sa
ORDER BY mm.failed_rate DESC;
