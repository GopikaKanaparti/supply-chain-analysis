-- 1. Total Inventory Value
SELECT 
    SUM(inventory_value) AS total_inventory_value
FROM supply_chain_clean;


-- 2. Inventory Value by Category
SELECT 
    Category,
    SUM(inventory_value) AS inventory_value
FROM supply_chain_clean
GROUP BY Category
ORDER BY inventory_value DESC;


-- 3. Products below Reorder Level
SELECT 
    ProductID,
    ProductName,
    StockQuantity,
    ReorderLevel
FROM supply_chain_clean
WHERE StockQuantity < ReorderLevel
ORDER BY StockQuantity ASC;


-- 4. Products with Highest Inventory Turnover
SELECT 
    ProductID,
    ProductName,
    Category,
    inventory_turnover
FROM supply_chain_clean
ORDER BY inventory_turnover DESC
LIMIT 10;


-- 5. Average Lead Time by Supplier
SELECT 
    Supplier,
    AVG(DeliveryTimeDays) AS average_lead_time_days
FROM supply_chain_clean
GROUP BY Supplier
ORDER BY average_lead_time_days DESC;


-- 6. Monthly Sales Trend
SELECT 
    order_month,
    SUM(SalesValue) AS total_sales
FROM supply_chain_clean
GROUP BY order_month
ORDER BY order_month;


-- 7. Percentage of Overstocked Products
SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN stock_status = 'Overstock' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS percentage_overstocked_products
FROM supply_chain_clean;