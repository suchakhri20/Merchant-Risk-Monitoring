
import pandas as pd

# 1. Load datasets
transactions = pd.read_csv("data/transactions.csv")
merchants = pd.read_csv("data/merchants.csv")

# 2. Convert transaction time
transactions["transaction_time"] = pd.to_datetime(
    transactions["transaction_time"]
)

# 3. Group transactions by merchant
merchant_summary = transactions.groupby("merchant_id").agg(
    total_transactions=("transaction_id", "count"),
    total_amount=("amount", "sum"),
    failed_transactions=("status", lambda x: (x == "Failed").sum()),
    refund_transactions=("is_refund", "sum")
).reset_index()

# 4. Calculate risk indicators
merchant_summary["failed_rate"] = (
    merchant_summary["failed_transactions"]
    / merchant_summary["total_transactions"] * 100
)

merchant_summary["refund_rate"] = (
    merchant_summary["refund_transactions"]
    / merchant_summary["total_transactions"] * 100
)

# 5. Add merchant information
merchant_summary = merchant_summary.merge(
    merchants[["merchant_id", "merchant_name", "business_category"]],
    on="merchant_id",
    how="left"
)

# 6. Filter merchants with at least 50 transactions
qualified_merchants = merchant_summary[
    merchant_summary["total_transactions"] >= 50
].copy()

# 7. Show Top 10 merchants by failed rate
print("\n===== TOP 10 MERCHANTS: FAILED RATE =====")

print(
    qualified_merchants.sort_values(
        "failed_rate", ascending=False
    )[
        ["merchant_name", "total_transactions",
         "failed_transactions", "failed_rate"]
    ].head(10).to_string(index=False)
)

# 8. Show Top 10 merchants by refund rate
print("\n===== TOP 10 MERCHANTS: REFUND RATE =====")

print(
    qualified_merchants.sort_values(
        "refund_rate", ascending=False
    )[
        ["merchant_name", "total_transactions",
         "refund_transactions", "refund_rate"]
    ].head(10).to_string(index=False)
)

# 9. Save results
merchant_summary.to_csv(
    "reports/merchant_risk_summary.csv",
    index=False
)

print("\nAnalysis completed!")
print("Saved: reports/merchant_risk_summary.csv")
