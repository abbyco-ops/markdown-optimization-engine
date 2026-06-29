-- Create production inventory table
CREATE TABLE IF NOT EXISTS retail_inventory (
    product_id VARCHAR PRIMARY KEY,
    category VARCHAR,
    original_price DECIMAL(10,2),
    weeks_on_shelf INT,
    initial_stock INT,
    inventory_level INT
);

-- Copy path directly from your exported CSV file
COPY retail_inventory FROM 'fashion_boutique_dataset.csv' (HEADER true, DELIMITER ',');
