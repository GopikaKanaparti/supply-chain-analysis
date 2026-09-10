import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD CLEANED DATASET
# ============================================================

file_path = "supply_chain_clean.csv"

df = pd.read_csv(file_path)

print("Original Shape:", df.shape)


# ============================================================
# 2. CONVERT DATE COLUMN
# ============================================================

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# ============================================================
# 3. INVENTORY VALUE
# Inventory Value = Stock Quantity × Unit Price
# ============================================================

df["inventory_value"] = (
    df["StockQuantity"] * df["UnitPrice"]
)


# ============================================================
# 4. INVENTORY TURNOVER
# Inventory Turnover = Units Sold / Stock Quantity
# ============================================================

df["inventory_turnover"] = np.where(
    df["StockQuantity"] > 0,
    df["UnitsSold"] / df["StockQuantity"],
    0
)


# ============================================================
# 5. STOCK STATUS
# ============================================================

def get_stock_status(row):

    if row["StockQuantity"] < row["ReorderLevel"]:
        return "Understock"

    elif row["StockQuantity"] == row["ReorderLevel"]:
        return "Optimal"

    else:
        return "Overstock"


df["stock_status"] = df.apply(
    get_stock_status,
    axis=1
)


# ============================================================
# 6. ORDER MONTH
# ============================================================

df["order_month"] = df["Date"].dt.month


# ============================================================
# 7. DISPLAY NEW COLUMNS
# ============================================================

print("\nFeature Engineering Completed!")

print("\nNew Columns:")
print(df[
    [
        "inventory_value",
        "inventory_turnover",
        "stock_status",
        "order_month"
    ]
].head())


# ============================================================
# 8. UPDATE SAME CLEANED DATASET
# ============================================================

df.to_csv(
    "supply_chain_clean.csv",
    index=False
)

print("\nUpdated Dataset Saved Successfully!")
print("Final Shape:", df.shape)