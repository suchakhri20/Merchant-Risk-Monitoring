
import pandas as pd
import numpy as np
from pathlib import Path

# 1. Set random seed for reproducible data
rng = np.random.default_rng(42)

# 2. Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 3. Create 50 synthetic merchants
merchant_ids = [f"M{i:03d}" for i in range(1, 51)]

categories = [
    "Retail", "Electronics", "Fashion",
    "Food", "Digital Services"
]

merchants = pd.DataFrame({
    "merchant_id": merchant_ids,
    "merchant_name": [f"Merchant {i:03d}" for i in range(1, 51)],
    "business_category": rng.choice(categories, 50),
    "registration_date": pd.to_datetime("2024-01-01")
        + pd.to_timedelta(rng.integers(0, 900, 50), unit="D"),
    "account_status": rng.choice(
        ["Active", "Active", "Active", "Under Review"],
        50
    )
})

# 4. Create 10,000 synthetic transactions
n = 10_000

transactions = pd.DataFrame({
    "transaction_id": [f"TXN{i:06d}" for i in range(1, n + 1)],
    "merchant_id": rng.choice(merchant_ids, n),
    "customer_id": [f"C{i:05d}" for i in rng.integers(1, 3001, n)],
    "transaction_time": (
        pd.Timestamp("2026-10-10")
        + pd.to_timedelta(
            rng.integers(0, 30 * 24 * 60 * 60, n),
            unit="s"
        )
    ),
    "amount": np.round(rng.lognormal(7.2, 0.9, n), 2),
    "payment_method": rng.choice(
        ["Credit Card", "Debit Card", "QR Payment", "E-Wallet"],
        n
    ),
    "status": rng.choice(
        ["Success", "Failed"],
        n,
        p=[0.96, 0.04]
    ),
    "is_refund": rng.choice(
        [True, False],
        n,
        p=[0.02, 0.98]
    ),
    "scenario_label": "Normal"
})

# 5. Inject synthetic suspicious patterns
# These labels are for testing only, not used as scoring inputs.

groups = {
    "High_Amount": 100,
    "Unusual_Hour": 100,
    "Repeated_Failures": 100,
    "Refund_Spike": 100
}

available_indices = np.arange(n)
rng.shuffle(available_indices)

start = 0

for label, count in groups.items():
    idx = available_indices[start:start + count]
    start += count

    transactions.loc[idx, "scenario_label"] = label

    if label == "High_Amount":
        transactions.loc[idx, "amount"] = np.round(
            rng.uniform(20000, 50000, count), 2
        )

    elif label == "Unusual_Hour":
        random_hours = rng.integers(0, 5, count)
        transactions.loc[idx, "transaction_time"] = (
            transactions.loc[idx, "transaction_time"].dt.normalize()
            + pd.to_timedelta(random_hours, unit="h")
            + pd.to_timedelta(
                rng.integers(0, 3600, count), unit="s"
            )
        )

    elif label == "Repeated_Failures":
        transactions.loc[idx, "status"] = "Failed"

    elif label == "Refund_Spike":
        transactions.loc[idx, "is_refund"] = True

# 6. Save CSV files
transactions.to_csv(
    DATA_DIR / "transactions.csv",
    index=False
)

merchants.to_csv(
    DATA_DIR / "merchants.csv",
    index=False
)

# 7. Display results
print("Dataset generation completed!")
print("Transactions:", len(transactions))
print("Merchants:", len(merchants))

print("\nScenario distribution:")
print(transactions["scenario_label"].value_counts())

print("\nSaved files:")
print(DATA_DIR / "transactions.csv")
print(DATA_DIR / "merchants.csv")
