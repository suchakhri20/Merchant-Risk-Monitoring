
import pandas as pd

# 1. Load transaction data
transactions = pd.read_csv("data/transactions.csv")
merchants = pd.read_csv("data/merchants.csv")

# 2. Calculate transaction amount statistics
print("\n===== TRANSACTION AMOUNT OVERVIEW =====")

print(
    transactions["amount"].describe(
        percentiles=[0.50, 0.75, 0.90, 0.95, 0.99]
    ).round(2)
)

# 3. Calculate P99 threshold
p99_threshold = transactions["amount"].quantile(0.99)

print("\nP99 Amount Threshold:", round(p99_threshold, 2))

# 4. Identify high-value transactions
transactions["is_high_amount"] = (
    transactions["amount"] > p99_threshold
)

high_amount_transactions = transactions[
    transactions["is_high_amount"]
].copy()

print("\n===== HIGH AMOUNT TRANSACTIONS =====")
print("Total high amount transactions:", len(high_amount_transactions))

print(
    high_amount_transactions[
        ["transaction_id", "merchant_id",
         "transaction_time", "amount", "status"]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
    .to_string(index=False)
)

# 5. Analyze high-value transactions by merchant
merchant_amount_summary = transactions.groupby("merchant_id").agg(
    total_transactions=("transaction_id", "count"),
    average_amount=("amount", "mean"),
    median_amount=("amount", "median"),
    max_amount=("amount", "max"),
    high_amount_count=("is_high_amount", "sum")
).reset_index()

merchant_amount_summary["high_amount_rate"] = (
    merchant_amount_summary["high_amount_count"]
    / merchant_amount_summary["total_transactions"] * 100
)

# 6. Add merchant information
merchant_amount_summary = merchant_amount_summary.merge(
    merchants[["merchant_id", "merchant_name", "business_category"]],
    on="merchant_id",
    how="left"
)

# 7. Show merchants with most high-value transactions
print("\n===== TOP MERCHANTS: HIGH AMOUNT COUNT =====")

print(
    merchant_amount_summary.sort_values(
        "high_amount_count", ascending=False
    )[
        ["merchant_name", "total_transactions",
         "average_amount", "max_amount",
         "high_amount_count", "high_amount_rate"]
    ]
    .head(10)
    .round(2)
    .to_string(index=False)
)

# 8. Save reports
high_amount_transactions.to_csv(
    "reports/high_amount_transactions.csv",
    index=False
)

merchant_amount_summary.to_csv(
    "reports/merchant_amount_summary.csv",
    index=False
)

print("\nAmount analysis completed!")
print("Saved amount analysis reports.")
