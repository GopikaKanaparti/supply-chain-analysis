import pandas as pd

# Load cleaned Excel file
input_file = "supermarket_inventory_data_warehouse.xlsx"
input_file = "cleaned_supermarket_inventory.xlsx"

df = pd.read_excel(input_file)

# Convert Excel to CSV
output_file = "supply_chain_clean.csv"
output_file = "supermarket_inventory_data_warehouse.csv"

df.to_csv(
    output_file,
    index=False
)

print("Excel converted to CSV successfully!")
print("CSV file saved as:", output_file)
print("Shape:", df.shape)