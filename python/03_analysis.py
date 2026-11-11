
import pandas as pd
from pathlib import Path

# 1. Set project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# 2. Load datasets
df = pd.read_csv(DATA_DIR / "transactions.csv")
merchants = pd.read_csv(DATA_DIR / "merchants.csv")

# 3. Convert transaction time to datetime
df["transaction_time"] = pd.to_datetime(df["transaction_time"])

# 4. Calculate key business metrics
total_transactions = len(df)
total_amount = df["amount"].sum()
average_amount = df["amount"].mean()

success_count = (df["status"] == "Success").sum()
failed_count = (df["status"] == "Failed").sum()
refund_count = df["is_refund"].sum()

success_rate = success_count / total_transactions * 100
failed_rate = failed_count / total_transactions * 100
refund_rate = refund_count / total_transactions * 100

# 5. Display results
print("=" * 45)
print("MERCHANT RISK MONITORING")
print("TRANSACTION OVERVIEW")
print("=" * 45)

print(f"Total Transactions : {total_transactions:,}")
print(f"Total Amount       : {total_amount:,.2f}")
print(f"Average Amount     : {average_amount:,.2f}")

print("-" * 45)
print(f"Successful         : {success_count:,}")
print(f"Failed             : {failed_count:,}")
print(f"Refunds            : {refund_count:,}")

print("-" * 45)
print(f"Success Rate       : {success_rate:.2f}%")
print(f"Failed Rate        : {failed_rate:.2f}%")
print(f"Refund Rate        : {refund_rate:.2f}%")

print("=" * 45)
