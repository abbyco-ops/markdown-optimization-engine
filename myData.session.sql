-- Create production inventory table
CREATE TABLE IF NOT EXISTS retail_inventory (
    product_id VARCHAR PRIMARY KEY,
    category VARCHAR,
    brand VARCHAR,
    season  VARCHAR,
    color VARCHAR,
    original_price DECIMAL(10,2),
    markdown_percentage DECIMAL(10,2),
    current_price DECIMAL(10,2),
    purchase_date DATE,
    stock_quantity INT,
    customer_rating DECIMAL(3,1),
    is_returned BOOLEAN,
    return_reason VARCHAR
);

-- Copy path directly from your exported CSV file
COPY retail_inventory FROM 'fashion_boutique_dataset.csv' (HEADER true, DELIMITER ',');
