import pandas as pd
import numpy as np

# ============================================================
# 1. LOAD CLEANED DATASET
# ============================================================

file_path = "supply_chain_clean.csv"

df = pd.read_csv(file_path)

print("Cleaned Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# 2. CONVERT DATE COLUMN
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)


# ============================================================
# 3. FEATURE ENGINEERING
# ============================================================

# ------------------------------------------------------------
# 3.1 Inventory Value
# Inventory Value = Stock Quantity × Unit Price
# ------------------------------------------------------------

df["inventory_value"] = (
    df["StockQuantity"] * df["UnitPrice"]
)


# ------------------------------------------------------------
# 3.2 Inventory Turnover
# Inventory Turnover = Units Sold / Stock Quantity
# Avoid division by zero
# ------------------------------------------------------------

df["inventory_turnover"] = np.where(
    df["StockQuantity"] > 0,
    df["UnitsSold"] / df["StockQuantity"],
    0
)


# ------------------------------------------------------------
# 3.3 Stock Status
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 3.4 Order Month
# ------------------------------------------------------------

df["order_month"] = df["Date"].dt.month


# ============================================================
# 4. DISPLAY FEATURE-ENGINEERED DATA
# ============================================================

print("\nFeature Engineering Completed!")

print("\nNew Features:")

print(
    df[
        [
            "ProductID",
            "StockQuantity",
            "UnitPrice",
            "UnitsSold",
            "ReorderLevel",
            "inventory_value",
            "inventory_turnover",
            "stock_status",
            "order_month"
        ]
    ].head()
)


# ============================================================
# 5. CHECK STOCK STATUS COUNTS
# ============================================================

print("\nStock Status Distribution:")

print(
    df["stock_status"].value_counts()
)


# ============================================================
# 6. FINAL DATASET SHAPE
# ============================================================

print("\nFinal Dataset Shape:",
      df.shape)


# ============================================================
# 7. SAVE FEATURE-ENGINEERED DATASET
# ============================================================

output_file = "supply_chain_feature_engineered.csv"

df.to_csv(
    output_file,
    index=False
)

print(
    "\nFeature-engineered dataset saved as:",
    output_file
)