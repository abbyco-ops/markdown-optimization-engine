# E-Commerce Markdown Optimization Engine

An interactive, data-driven decision tool designed to prevent profit margin erosion for fashion retailers. This project simulates a real-world enterprise analytics pipeline, converting transaction-level sales receipts into actionable product profiles using **SQL (DuckDB)** and surfacing real-time markdown recommendations via an interactive **Tableau Dashboard**.

[View Tableau Dashboard Here!](https://public.tableau.com/views/Book1_17888969222580/FashionRetailMarkdownOptimizationModel?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)


## Executive Summary & Business Case

In fashion retail, inventory stagnation is a multi-million dollar bottleneck. Holding products at full price for too long ties up working capital and exhausts valuable warehouse shelf space. Conversely, premature or aggressive price cuts can quickly undermine gross margins. 

This product serves as a **Merchandising Decision Support System**. It evaluates product performance based on the core retail KPI: **Sell-Through Rate (STR)**. By flagging underperforming category-brand-season groups against an adjustable markdown threshold, this tool helps retailers maximize inventory turnover while protecting profit margins.



## Tech Stack & Architecture

- **Data Engineering Engine:** DuckDB SQL (High-performance relational in-memory database)
- **Visualization & Interface Layer:** Tableau (interactive dashboard with parameter-driven filtering)
- **Data Analytics & Core Libraries:** Pandas, Pandas
- **Data Source:** Ingests live transactional store data tracking variables like `stock_quantity`, `original_price`, `category`, and `purchase_date`.



## Core Features & Analytics Pipeline

### 1. SQL Aggregation & KPI Engineering
Raw boutique sales ledger data consists of scattered transaction-level rows, with each `product_id` unique per transaction rather than per style. This engine uses DuckDB SQL to aggregate transactions into category-brand-season product profiles, calculating the **Sell-Through Rate (STR)**:
$$\text{STR} = \left( \frac{\text{Units Sold}}{\text{Units Sold} + \text{Remaining Stock}} \right) \times 100$$

### 2. Markdown Recommendation Logic
A rule-based logic layer flags product groupings as "Markdown Now", "Watch", or "Healthy" based on an adjustable STR threshold, mirroring how retail merchandising teams triage markdown decisions at the style-color level. 

### 3. Interactive Control Panel
Built in Tableau to demonstrate business-facing analytics:
- **Markdown Threshold Parameter:** Adjust the STR benchmark live and watch flagged inventory update in real time.
- **Drill-down Priority List:** Filter down to only at-risk category-brand-season groups, with dollar-value estimate of at-risk inventory.
- **Seasonal Trend View:** Explore how sell-through rate shifts by season across categories.

## Running the SQL Pipeline Locally
The data aggregation logic (DuckDB SQL export) can be run locally to regenerate `product_profiles.csv`:

```bash
# Install dependencies
pip install duckdb pandas

# Run the export script
python3 export_data.py
```

---

## Data
Kaggle: https://www.kaggle.com/datasets/pratyushpuri/retail-fashion-boutique-data-sales-analytics-2025


📄 **License:** This project is open-source and available under the **MIT License**.
