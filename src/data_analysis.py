import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# DATA QUALITY ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw_dataset.csv"
CLEANED_FILE = BASE_DIR / "data" / "cleaned_dataset.csv"
SCREENSHOT_DIR = BASE_DIR / "screenshots"


# Create screenshots directory if it doesn't exist
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. Load datasets
# ============================================================

raw_df = pd.read_csv(RAW_FILE)
cleaned_df = pd.read_csv(CLEANED_FILE)


print("=" * 60)
print("DATA QUALITY ANALYSIS")
print("=" * 60)


# ============================================================
# 2. Dataset comparison
# ============================================================

print("\n--- DATASET COMPARISON ---")

print(f"Raw dataset rows: {len(raw_df)}")
print(f"Cleaned dataset rows: {len(cleaned_df)}")

print(f"Raw dataset columns: {len(raw_df.columns)}")
print(f"Cleaned dataset columns: {len(cleaned_df.columns)}")


# ============================================================
# 3. Missing value comparison
# ============================================================

raw_missing = raw_df.isna().sum()
cleaned_missing = cleaned_df.isna().sum()

print("\n--- MISSING VALUES COMPARISON ---")

print("\nRaw dataset:")
print(raw_missing)

print("\nCleaned dataset:")
print(cleaned_missing)


# ============================================================
# 4. Duplicate comparison
# ============================================================

raw_duplicates = raw_df.duplicated().sum()
cleaned_duplicates = cleaned_df.duplicated().sum()

print("\n--- DUPLICATE COMPARISON ---")

print(f"Raw exact duplicates: {raw_duplicates}")
print(f"Cleaned exact duplicates: {cleaned_duplicates}")


# ============================================================
# 5. Data types
# ============================================================

print("\n--- CLEANED DATA TYPES ---")

print(cleaned_df.dtypes)


# ============================================================
# 6. Basic statistics
# ============================================================

print("\n--- BASIC STATISTICS ---")

print(
    cleaned_df[
        ["quantity", "unit_price", "total_amount"]
    ].describe()
)


# ============================================================
# 7. Product analysis
# ============================================================

print("\n--- PRODUCT ANALYSIS ---")

product_sales = (
    cleaned_df
    .groupby("product")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)


# ============================================================
# 8. City analysis
# ============================================================

print("\n--- CITY ANALYSIS ---")

city_sales = (
    cleaned_df
    .groupby("city")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(city_sales)


# ============================================================
# 9. Create product sales chart
# ============================================================

plt.figure(figsize=(9, 5))

product_sales.plot(
    kind="bar"
)

plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")

plt.xticks(rotation=30)
plt.tight_layout()

product_chart = (
    SCREENSHOT_DIR / "product_sales.png"
)

plt.savefig(
    product_chart,
    dpi=150
)

plt.close()

print(
    f"\nProduct sales chart saved to:\n"
    f"{product_chart}"
)


# ============================================================
# 10. Create city sales chart
# ============================================================

plt.figure(figsize=(9, 5))

city_sales.plot(
    kind="bar"
)

plt.title("Total Sales by City")
plt.xlabel("City")
plt.ylabel("Total Sales")

plt.xticks(rotation=30)
plt.tight_layout()

city_chart = (
    SCREENSHOT_DIR / "city_sales.png"
)

plt.savefig(
    city_chart,
    dpi=150
)

plt.close()

print(
    f"City sales chart saved to:\n"
    f"{city_chart}"
)


# ============================================================
# 11. Missing values comparison chart
# ============================================================

comparison = pd.DataFrame({
    "Raw Dataset": raw_missing,
    "Cleaned Dataset": cleaned_missing
})

comparison = comparison.fillna(0)

plt.figure(figsize=(10, 6))

comparison.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Missing Values: Before vs After Cleaning")
plt.xlabel("Columns")
plt.ylabel("Number of Missing Values")

plt.xticks(rotation=45)
plt.tight_layout()

missing_chart = (
    SCREENSHOT_DIR / "missing_values_comparison.png"
)

plt.savefig(
    missing_chart,
    dpi=150
)

plt.close()

print(
    f"Missing values chart saved to:\n"
    f"{missing_chart}"
)


# ============================================================
# 12. Save analysis summary
# ============================================================

summary_file = BASE_DIR / "analysis_summary.txt"

with open(
    summary_file,
    "w",
    encoding="utf-8"
) as file:

    file.write("DATA QUALITY ANALYSIS SUMMARY\n")
    file.write("=" * 50 + "\n\n")

    file.write(
        f"Raw dataset rows: {len(raw_df)}\n"
    )

    file.write(
        f"Cleaned dataset rows: {len(cleaned_df)}\n"
    )

    file.write(
        f"Rows removed: "
        f"{len(raw_df) - len(cleaned_df)}\n"
    )

    file.write(
        f"Raw exact duplicates: "
        f"{raw_duplicates}\n"
    )

    file.write(
        f"Cleaned exact duplicates: "
        f"{cleaned_duplicates}\n"
    )

    file.write(
        f"Raw missing values: "
        f"{raw_missing.sum()}\n"
    )

    file.write(
        f"Cleaned missing values: "
        f"{cleaned_missing.sum()}\n"
    )

    file.write("\nProduct Sales:\n")
    file.write(product_sales.to_string())

    file.write("\n\nCity Sales:\n")
    file.write(city_sales.to_string())


print(
    f"\nAnalysis summary saved to:\n"
    f"{summary_file}"
)


# ============================================================
# 13. Completion message
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)