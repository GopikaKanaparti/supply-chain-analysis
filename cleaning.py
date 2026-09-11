import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD DATASET
# ============================================================

file_path = "supermarket.csv"

df = pd.read_csv(file_path)

print("Original Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# 2. CHECK DATA TYPES
# ============================================================

print("\nData Types Before Cleaning:")
print(df.dtypes)


# ============================================================
# 3. CHECK DUPLICATE RECORDS
# ============================================================

print("\nDuplicate Complete Records:",
      df.duplicated().sum())

print(
    "Duplicate ProductID + WarehouseID:",
    df.duplicated(
        subset=["ProductID", "WarehouseID"]
    ).sum()
)

# Remove exact duplicate records
df = df.drop_duplicates()

print(
    "\nShape After Removing Duplicates:",
    df.shape
)


# ============================================================
# 4. CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "UnitPrice",
    "StockQuantity",
    "StockValue",
    "ReorderLevel",
    "ReorderQuantity",
    "UnitsSold",
    "SalesValue",
    "DeliveryTimeDays",
    "WarehouseCapacityUnits"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\nData Types After Numeric Conversion:")
print(df[numeric_columns].dtypes)


# ============================================================
# 5. CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "Date",
    "LastSoldDate",
    "LastRestockDate",
    "NextRestockDate"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )

print("\nDate Data Types:")
print(df[date_columns].dtypes)


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\nMissing Values:")

missing_values = df.isnull().sum()

print(
    missing_values[missing_values > 0]
)


# ============================================================
# 7. HANDLE MISSING LAST SOLD DATE
# ============================================================

# Do NOT insert random dates.
# Missing dates are kept as NaT because the actual
# last sold date is not available.

print(
    "\nMissing LastSoldDate:",
    df["LastSoldDate"].isna().sum()
)


# ============================================================
# 8. CHECK NUMERIC MISSING VALUES
# ============================================================

print("\nMissing Numeric Values:")

for column in numeric_columns:

    missing = df[column].isna().sum()

    if missing > 0:
        print(column, ":", missing)


# ============================================================
# 9. CHECK NEGATIVE INVENTORY
# ============================================================

negative_inventory = (
    df["StockQuantity"] < 0
).sum()

print(
    "\nNegative Inventory Records:",
    negative_inventory
)


# ============================================================
# 10. CHECK NEGATIVE SALES
# ============================================================

negative_sales = (
    df["UnitsSold"] < 0
).sum()

print(
    "Negative Sales Records:",
    negative_sales
)


# ============================================================
# 11. REMOVE NEGATIVE VALUES
# ============================================================

if negative_inventory > 0 or negative_sales > 0:

    df = df[
        (df["StockQuantity"] >= 0) &
        (df["UnitsSold"] >= 0)
    ].copy()

    print("\nNegative inventory/sales records removed.")

else:

    print("\nNo negative inventory or sales records found.")


# ============================================================
# 12. FINAL VALIDATION
# ============================================================

print("\n========== FINAL VALIDATION ==========")

print(
    "Final Dataset Shape:",
    df.shape
)

print(
    "Duplicate Complete Records:",
    df.duplicated().sum()
)

print(
    "Duplicate ProductID + WarehouseID:",
    df.duplicated(
        subset=["ProductID", "WarehouseID"]
    ).sum()
)

print(
    "Negative Stock:",
    (df["StockQuantity"] < 0).sum()
)

print(
    "Negative Sales:",
    (df["UnitsSold"] < 0).sum()
)


# ============================================================
# 13. FINAL MISSING VALUES
# ============================================================

print("\nFinal Missing Values:")

final_missing = df.isnull().sum()

print(
    final_missing[final_missing > 0]
)


# ============================================================
# 14. FINAL DATA TYPES
# ============================================================

print("\nFinal Data Types:")
print(df.dtypes)


# ============================================================
# 15. SAVE CLEANED DATASET AS CSV
# ============================================================

output_file = "supply_chain_clean.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    "\nCleaned dataset saved as:",
    output_file
)