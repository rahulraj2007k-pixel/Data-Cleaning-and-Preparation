import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# DATA CLEANING & PREPARATION PROJECT
# ============================================================

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw_dataset.csv"
CLEANED_FILE = BASE_DIR / "data" / "cleaned_dataset.csv"
LOG_FILE = BASE_DIR / "cleaning_log.txt"


# ------------------------------------------------------------
# 2. Cleaning log
# ------------------------------------------------------------

log_messages = []


def log(message):
    """Print message and store it in cleaning log."""
    print(message)
    log_messages.append(str(message))


# ------------------------------------------------------------
# 3. Load dataset
# ------------------------------------------------------------

log("=" * 60)
log("DATA CLEANING & PREPARATION")
log("=" * 60)

try:
    df = pd.read_csv(RAW_FILE)
except FileNotFoundError:
    print(f"\nERROR: Dataset not found at:\n{RAW_FILE}")
    print("Please make sure raw_dataset.csv is inside the data folder.")
    raise SystemExit(1)


original_rows = len(df)
original_columns = len(df.columns)

log(f"Loaded dataset: {original_rows} rows, {original_columns} columns")


# ------------------------------------------------------------
# 4. Initial inspection
# ------------------------------------------------------------

log("\n--- INITIAL DATA INSPECTION ---")

log(f"Shape: {df.shape}")
log(f"Columns: {list(df.columns)}")

log("\nData types before cleaning:")
log(df.dtypes.to_string())

log("\nMissing values before cleaning:")
log(df.isna().sum().to_string())

log(f"\nExact duplicate rows before cleaning: {df.duplicated().sum()}")


# ------------------------------------------------------------
# 5. Standardize column names
# ------------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

log("\nColumn names standardized.")


# ------------------------------------------------------------
# 6. Clean text columns
# ------------------------------------------------------------

text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

log("Removed leading/trailing spaces from text fields.")


# ------------------------------------------------------------
# 7. Standardize city names
# ------------------------------------------------------------

if "city" in df.columns:
    df["city"] = df["city"].str.title()

log("Standardized city names.")


# ------------------------------------------------------------
# 8. Standardize product names
# ------------------------------------------------------------

if "product" in df.columns:
    df["product"] = df["product"].str.title()

log("Standardized product names.")


# ------------------------------------------------------------
# 9. Standardize email addresses
# ------------------------------------------------------------

if "email" in df.columns:

    df["email"] = (
        df["email"]
        .str.strip()
        .str.lower()
    )

log("Standardized email addresses to lowercase.")


# ------------------------------------------------------------
# 10. Validate email addresses
# ------------------------------------------------------------

if "email" in df.columns:

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_email = (
        df["email"].notna()
        & ~df["email"].str.match(
            email_pattern,
            na=False
        )
    )

    invalid_email_count = int(invalid_email.sum())

    # Convert invalid email addresses to missing
    df.loc[invalid_email, "email"] = pd.NA

    log(
        f"Invalid email addresses converted to "
        f"missing values: {invalid_email_count}"
    )


# ------------------------------------------------------------
# 11. Convert order dates
# ------------------------------------------------------------

if "order_date" in df.columns:

    # Remove unnecessary spaces
    df["order_date"] = (
        df["order_date"]
        .astype("string")
        .str.strip()
    )

    # Handle different formats such as:
    # 2026-01-05
    # 05/01/2026
    # 2026/01/07
    # 08-01-2026

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    log(
        "Converted multiple date formats "
        "to standard datetime format."
    )


# ------------------------------------------------------------
# 12. Convert numeric columns
# ------------------------------------------------------------

numeric_columns = [
    "quantity",
    "unit_price"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        log(
            f"Converted {column} "
            f"to numeric format."
        )


# ------------------------------------------------------------
# 13. Detect invalid negative quantity
# ------------------------------------------------------------

if "quantity" in df.columns:

    invalid_quantity = df["quantity"] < 0

    invalid_quantity_count = int(
        invalid_quantity.sum()
    )

    df.loc[
        invalid_quantity,
        "quantity"
    ] = np.nan

    log(
        "Invalid negative quantities converted "
        f"to missing values: {invalid_quantity_count}"
    )


# ------------------------------------------------------------
# 14. Detect invalid negative prices
# ------------------------------------------------------------

if "unit_price" in df.columns:

    invalid_price = df["unit_price"] < 0

    invalid_price_count = int(
        invalid_price.sum()
    )

    df.loc[
        invalid_price,
        "unit_price"
    ] = np.nan

    log(
        "Invalid negative prices converted "
        f"to missing values: {invalid_price_count}"
    )


# ------------------------------------------------------------
# 15. Remove duplicate records
# ------------------------------------------------------------

exact_duplicates = int(
    df.duplicated().sum()
)

# Business-key duplicate detection.
#
# Two records are treated as duplicates when their
# customer, email, date, product, quantity and price
# are identical, even if their order_id is different.

duplicate_columns = [
    "customer_name",
    "email",
    "order_date",
    "product",
    "quantity",
    "unit_price"
]

available_duplicate_columns = [
    column
    for column in duplicate_columns
    if column in df.columns
]

business_duplicates = int(
    df.duplicated(
        subset=available_duplicate_columns,
        keep="first"
    ).sum()
)

df = df.drop_duplicates(
    subset=available_duplicate_columns,
    keep="first"
)

log(
    f"Exact duplicate rows detected: "
    f"{exact_duplicates}"
)

log(
    f"Business-key duplicate rows removed: "
    f"{business_duplicates}"
)


# ------------------------------------------------------------
# 16. Handle missing quantity
# ------------------------------------------------------------

if "quantity" in df.columns:

    missing_quantity = int(
        df["quantity"].isna().sum()
    )

    if missing_quantity > 0:

        median_quantity = df["quantity"].median()

        df["quantity"] = (
            df["quantity"]
            .fillna(median_quantity)
        )

    log(
        "Missing quantity values filled "
        f"using median: {missing_quantity}"
    )


# ------------------------------------------------------------
# 17. Handle missing unit price
# ------------------------------------------------------------

if "unit_price" in df.columns:

    missing_price = int(
        df["unit_price"].isna().sum()
    )

    if missing_price > 0:

        median_price = df["unit_price"].median()

        df["unit_price"] = (
            df["unit_price"]
            .fillna(median_price)
        )

    log(
        "Missing unit_price values filled "
        f"using median: {missing_price}"
    )


# ------------------------------------------------------------
# 18. Handle missing email
# ------------------------------------------------------------

if "email" in df.columns:

    missing_email = int(
        df["email"].isna().sum()
    )

    df["email"] = (
        df["email"]
        .fillna("unknown@example.com")
    )

    log(
        "Missing email values filled with "
        f"placeholder: {missing_email}"
    )


# ------------------------------------------------------------
# 19. Handle missing order dates
# ------------------------------------------------------------

if "order_date" in df.columns:

    missing_dates = int(
        df["order_date"].isna().sum()
    )

    if missing_dates > 0:

        median_date = df["order_date"].median()

        df["order_date"] = (
            df["order_date"]
            .fillna(median_date)
        )

    log(
        "Missing order dates filled using "
        f"median date: {missing_dates}"
    )


# ------------------------------------------------------------
# 20. Set appropriate data types
# ------------------------------------------------------------

if "order_id" in df.columns:

    df["order_id"] = pd.to_numeric(
        df["order_id"],
        errors="coerce"
    ).astype("Int64")


if "quantity" in df.columns:

    df["quantity"] = (
        df["quantity"]
        .round()
        .astype("Int64")
    )


if "unit_price" in df.columns:

    df["unit_price"] = (
        df["unit_price"]
        .round(2)
    )


# ------------------------------------------------------------
# 21. Create total amount
# ------------------------------------------------------------

if (
    "quantity" in df.columns
    and "unit_price" in df.columns
):

    df["total_amount"] = (
        df["quantity"]
        * df["unit_price"]
    )

    log("Created total_amount column.")


# ------------------------------------------------------------
# 22. Standardize final date format
# ------------------------------------------------------------

if "order_date" in df.columns:

    df["order_date"] = (
        df["order_date"]
        .dt.strftime("%Y-%m-%d")
    )

    log(
        "Standardized final order_date "
        "format to YYYY-MM-DD."
    )


# ------------------------------------------------------------
# 23. Final validation
# ------------------------------------------------------------

log("\n--- FINAL VALIDATION ---")

remaining_missing = int(
    df.isna().sum().sum()
)

remaining_duplicates = int(
    df.duplicated().sum()
)

final_rows = len(df)
final_columns = len(df.columns)

log(
    f"Remaining missing values: "
    f"{remaining_missing}"
)

log(
    f"Remaining duplicate rows: "
    f"{remaining_duplicates}"
)

log(
    f"Final dataset shape: "
    f"{df.shape}"
)


# ------------------------------------------------------------
# 24. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(
    CLEANED_FILE,
    index=False
)

log(
    f"\nCleaned dataset saved to: "
    f"{CLEANED_FILE}"
)


# ------------------------------------------------------------
# 25. Save cleaning log
# ------------------------------------------------------------

with open(
    LOG_FILE,
    "w",
    encoding="utf-8"
) as file:

    for message in log_messages:
        file.write(message + "\n")


log(
    f"Cleaning log saved to: "
    f"{LOG_FILE}"
)


# ------------------------------------------------------------
# 26. Final summary
# ------------------------------------------------------------

log("\n" + "=" * 60)
log("CLEANING SUMMARY")
log("=" * 60)

log(
    f"Original rows: {original_rows}"
)

log(
    f"Final rows: {final_rows}"
)

log(
    f"Rows removed: "
    f"{original_rows - final_rows}"
)

log(
    f"Original columns: "
    f"{original_columns}"
)

log(
    f"Final columns: "
    f"{final_columns}"
)

log(
    f"Missing values remaining: "
    f"{remaining_missing}"
)

log(
    f"Duplicate rows remaining: "
    f"{remaining_duplicates}"
)

log("=" * 60)
log("DATA CLEANING COMPLETED SUCCESSFULLY")
log("=" * 60)