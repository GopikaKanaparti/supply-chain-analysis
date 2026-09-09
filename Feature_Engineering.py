import pandas as pd
import numpy as np

# Load dataset
df = pd.read_excel("supermarket_inventory_data_with_warehouse.xlsx")

# -----------------------------
# Feature Engineering
# -----------------------------

# 1. Inventory Value
df["inventory_value"] = (
    df["Inventory_Level"] * df["Unit_Cost"]
)

# 2. Inventory Turnover
# Avoid division by zero
df["inventory_turnover"] = np.where(
    df["Inventory_Level"] > 0,
    df["Units_Sold"] / df["Inventory_Level"],
    0
)

# 3. Stock Status
def get_stock_status(row):
    if row["Inventory_Level"] < row["Reorder_Level"]:
        return "Understock"
    elif row["Inventory_Level"] == row["Reorder_Level"]:
        return "Optimal"
    else:
        return "Overstock"

df["stock_status"] = df.apply(get_stock_status, axis=1)

# 4. Order Month
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["order_month"] = df["Order_Date"].dt.month

# -----------------------------
# Export cleaned dataset
# -----------------------------

df.to_csv(
    "../data/processed/supply_chain_clean.csv",
    index=False
)

print("Feature engineering completed.")
print(df.head())
print("Final shape:", df.shape)