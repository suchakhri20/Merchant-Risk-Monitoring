
import pandas as pd

# 1. Load transaction data
transactions = pd.read_csv("data/transactions.csv")

# 2. Convert transaction time
transactions["transaction_time"] = pd.to_datetime(
    transactions["transaction_time"]
)

# 3. Extract hour and date
transactions["hour"] = transactions["transaction_time"].dt.hour
transactions["date"] = transactions["transaction_time"].dt.date

# 4. Analyze by hour
hourly_summary = transactions.groupby("hour").agg(
    total_transactions=("transaction_id", "count"),
    failed_transactions=("status", lambda x: (x == "Failed").sum()),
    refund_transactions=("is_refund", "sum")
).reset_index()

hourly_summary["failed_rate"] = (
    hourly_summary["failed_transactions"]
    / hourly_summary["total_transactions"] * 100
)

hourly_summary["refund_rate"] = (
    hourly_summary["refund_transactions"]
    / hourly_summary["total_transactions"] * 100
)

print("\n===== HOURLY TRANSACTION ANALYSIS =====")

print(
    hourly_summary.sort_values(
        "failed_rate", ascending=False
    ).round(2).to_string(index=False)
)

# 5. Analyze by date
daily_summary = transactions.groupby("date").agg(
    total_transactions=("transaction_id", "count"),
    failed_transactions=("status", lambda x: (x == "Failed").sum()),
    refund_transactions=("is_refund", "sum")
).reset_index()

daily_summary["failed_rate"] = (
    daily_summary["failed_transactions"]
    / daily_summary["total_transactions"] * 100
)

daily_summary["refund_rate"] = (
    daily_summary["refund_transactions"]
    / daily_summary["total_transactions"] * 100
)

print("\n===== TOP 10 DAYS: FAILED RATE =====")

print(
    daily_summary.sort_values(
        "failed_rate", ascending=False
    )[
        ["date", "total_transactions",
         "failed_transactions", "failed_rate"]
    ].head(10).round(2).to_string(index=False)
)

# 6. Save results
hourly_summary.to_csv(
    "reports/hourly_risk_summary.csv", index=False
)

daily_summary.to_csv(
    "reports/daily_risk_summary.csv", index=False
)

print("\nTime analysis completed!")
print("Saved hourly and daily reports.")
