
import pandas as pd

# 1. Load previous analysis results
merchant_risk = pd.read_csv(
    "reports/merchant_risk_summary.csv"
)

merchant_amount = pd.read_csv(
    "reports/merchant_amount_summary.csv"
)

# 2. Merge results
risk_analysis = merchant_risk.merge(
    merchant_amount[
        ["merchant_id", "high_amount_count", "high_amount_rate"]
    ],
    on="merchant_id",
    how="left"
)

# 3. Define demo screening thresholds
FAILED_RATE_THRESHOLD = 4.97
REFUND_RATE_THRESHOLD = 2.87
HIGH_AMOUNT_COUNT_THRESHOLD = 3

# 4. Create risk indicators
risk_analysis["high_failed_rate"] = (
    risk_analysis["failed_rate"] > FAILED_RATE_THRESHOLD
)

risk_analysis["high_refund_rate"] = (
    risk_analysis["refund_rate"] > REFUND_RATE_THRESHOLD
)

risk_analysis["repeated_high_amount"] = (
    risk_analysis["high_amount_count"]
    >= HIGH_AMOUNT_COUNT_THRESHOLD
)

# 5. Count risk signals
risk_columns = [
    "high_failed_rate",
    "high_refund_rate",
    "repeated_high_amount"
]

risk_analysis["risk_signal_count"] = (
    risk_analysis[risk_columns].sum(axis=1)
)

# 6. Assign screening level
def assign_screening_level(score):
    if score >= 3:
        return "High"
    elif score == 2:
        return "Medium"
    elif score == 1:
        return "Low"
    else:
        return "No Signal"

risk_analysis["screening_level"] = (
    risk_analysis["risk_signal_count"]
    .apply(assign_screening_level)
)

# 7. Sort merchants
risk_analysis = risk_analysis.sort_values(
    ["risk_signal_count", "failed_rate"],
    ascending=[False, False]
)

# 8. Display results
print("\n===== MERCHANT RISK SCREENING =====")

print(
    risk_analysis[
        [
            "merchant_name",
            "failed_rate",
            "refund_rate",
            "high_amount_count",
            "risk_signal_count",
            "screening_level"
        ]
    ].round(2).to_string(index=False)
)

# 9. Screening summary
print("\n===== SCREENING SUMMARY =====")

print(
    risk_analysis["screening_level"]
    .value_counts()
    .to_string()
)

# 10. Save result
risk_analysis.to_csv(
    "reports/merchant_risk_screening.csv",
    index=False
)

print("\nCross-risk analysis completed!")
print("Saved: reports/merchant_risk_screening.csv")
