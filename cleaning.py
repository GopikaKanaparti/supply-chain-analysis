import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD DATASET
# ============================================================

file_path = "supermarket_inventory_data_with_warehouse.xlsx"

df = pd.read_excel(file_path)

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

print("\nDuplicate Complete Records:", df.duplicated().sum())
print("Duplicate ProductID:", df["ProductID"].duplicated().sum())

# Remove exact duplicate records
df = df.drop_duplicates()

print("\nShape After Removing Duplicate Records:", df.shape)


# ============================================================
# 4. CONVERT NUMERIC COLUMNS TO NUMERIC TYPE
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
    df[column] = pd.to_numeric(df[column], errors="coerce")


print("\nData Types After Numeric Conversion:")
print(df[numeric_columns].dtypes)


# ============================================================
# 5. CONVERT DATE COLUMNS TO DATETIME
# ============================================================

date_columns = [
    "Date",
    "LastSoldDate",
    "LastRestockDate",
    "NextRestockDate"
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")


print("\nDate Data Types:")
print(df[date_columns].dtypes)


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

missing_values = df.isnull().sum()

print("\nMissing Values:")
print(missing_values[missing_values > 0])


# ============================================================
# 7. HANDLE MISSING VALUES
# ============================================================

# LastSoldDate has missing values.
# We do NOT replace missing dates with fake dates because
# that would create incorrect sales information.

# Keep missing LastSoldDate as NaT.
# NaT means "Not a Time" and represents a missing datetime value.

print("\nMissing LastSoldDate after cleaning:",
      df["LastSoldDate"].isna().sum())


# ============================================================
# 8. CHECK NUMERIC CONVERSION CREATED MISSING VALUES
# ============================================================

print("\nMissing Values After Numeric Conversion:")

for column in numeric_columns:
    missing = df[column].isna().sum()

    if missing > 0:
        print(column, ":", missing)


# ============================================================
# 9. CHECK FOR NEGATIVE INVENTORY VALUES
# ============================================================

negative_inventory = (df["StockQuantity"] < 0).sum()

print("\nNegative Inventory Records:", negative_inventory)

if negative_inventory > 0:
    print("Negative inventory records found:")
    print(df[df["StockQuantity"] < 0])
else:
    print("No negative inventory values found.")


# ============================================================
# 10. CHECK FOR NEGATIVE SALES VALUES
# ============================================================

negative_sales = (df["UnitsSold"] < 0).sum()

print("\nNegative Sales Records:", negative_sales)

if negative_sales > 0:
    print("Negative sales records found:")
    print(df[df["UnitsSold"] < 0])
else:
    print("No negative sales values found.")


# ============================================================
# 11. HANDLE NEGATIVE VALUES IF THEY EXIST
# ============================================================

# Since negative inventory or sales are logically invalid
# for this dataset, remove such records if they exist.

df = df[
    (df["StockQuantity"] >= 0) &
    (df["UnitsSold"] >= 0)
].copy()


# ============================================================
# 12. FINAL DATA VALIDATION
# ============================================================

print("\n========== FINAL VALIDATION ==========")

print("Final Dataset Shape:", df.shape)

print("Duplicate Records:", df.duplicated().sum())

print("Duplicate ProductID:",
      df["ProductID"].duplicated().sum())

print("Negative Stock:",
      (df["StockQuantity"] < 0).sum())

print("Negative Sales:",
      (df["UnitsSold"] < 0).sum())

print("\nFinal Missing Values:")
print(df.isnull().sum()[df.isnull().sum() > 0])


# ============================================================
# 13. DISPLAY FINAL DATA TYPES
# ============================================================

print("\nFinal Data Types:")
print(df.dtypes)


# ============================================================
# 14. SAVE CLEANED DATASET
# ============================================================

output_file = "cleaned_supermarket_inventory.xlsx"

df.to_excel(output_file, index=False)

print("\nCleaned dataset saved as:", output_file)