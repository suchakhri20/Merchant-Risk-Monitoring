
import pandas as pd
from pathlib import Path

# Locate project data
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Load datasets
transactions = pd.read_csv(DATA_DIR / "transactions.csv")
merchants = pd.read_csv(DATA_DIR / "merchants.csv")

print("===== DATA QUALITY REPORT =====")

# 1. Check row counts
print("\n1. Record Counts")
print("Transactions:", len(transactions))
print("Merchants:", len(merchants))

# 2. Check missing values
print("\n2. Missing Values")
print("Transactions:\n", transactions.isnull().sum())
print("Merchants:\n", merchants.isnull().sum())

# 3. Check duplicate IDs
print("\n3. Duplicate IDs")
print("Duplicate Transaction IDs:",
      transactions["transaction_id"].duplicated().sum())
print("Duplicate Merchant IDs:",
      merchants["merchant_id"].duplicated().sum())

# 4. Check negative amounts
print("\n4. Invalid Amounts")
print("Negative amounts:",
      (transactions["amount"] < 0).sum())
print("Zero amounts:",
      (transactions["amount"] == 0).sum())

# 5. Check merchant references
print("\n5. Merchant References")
invalid_merchants = ~transactions["merchant_id"].isin(
    merchants["merchant_id"]
)
print("Transactions with unknown merchants:",
      invalid_merchants.sum())

# 6. Check transaction status
print("\n6. Transaction Status")
print(transactions["status"].value_counts())

# 7. Check scenario labels
print("\n7. Scenario Labels")
print(transactions["scenario_label"].value_counts())

print("\n===== VALIDATION COMPLETED =====")
