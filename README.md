# E-Commerce Markdown Optimization Engine

An interactive, data-driven decision tool designed to prevent profit margin erosion for fashion retailers. This project simulates a real-world enterprise analytics pipeline, converting transaction-level sales receipts into actionable product profiles using **SQL (DuckDB)** and surfacing real-time markdown recommendations via an interactive **Streamlit web dashboard**.



## Executive Summary & Business Case

In fashion retail, inventory stagnation is a multi-million dollar bottleneck. Holding products at full price for too long ties up working capital and exhausts valuable warehouse shelf space. Conversely, premature or aggressive price cuts can quickly undermine gross margins. 

This product serves as a **Merchandising Decision Support System**. It evaluates product performance based on the core retail KPI: **Sell-Through Rate (STR)**. By triggering rule-based, optimized discounts on underperforming clothing lines, this tool helps retailers maximize inventory turnover while aggressively protecting profit margins.



## Tech Stack & Architecture

- **Interface Layer:** Python & Streamlit (Interactive Web UI for Recruiters/Category Buyers)
- **Data Engineering Engine:** DuckDB SQL (High-performance relational in-memory database)
- **Data Analytics & Core Libraries:** Pandas, NumPy, Matplotlib, Seaborn
- **Data Source:** Ingests live transactional store data tracking variables like `stock_quantity`, `original_price`, `category`, and `purchase_date`.



## Core Features & Analytics Pipeline

### 1. SQL Aggregation & KPI Engineering
Raw boutique sales ledger data consists of scattered transaction rows. This engine leverages DuckDB SQL to compress rows into localized product profiles, dynamically calculating the **Sell-Through Rate (STR)**:
$$\text{STR} = \left( \frac{\text{Units Sold}}{\text{Units Sold} + \text{Remaining Stock}} \right) \times 100$$

### 2. Algorithmic Markdown Engine
A rule-based SQL logic engine (`CASE WHEN` structures) monitors inventory drift. If a product line's STR drops below user-defined risk thresholds, the system flags the product and auto-generates a calibrated promotional price index to clear stock.

### 3. Interactive Control Panel
Built specifically to demonstrate product sense, users can manipulate parameters in real time:
- **STR Slider:** Adjust the benchmark percentage defining "stagnant" inventory.
- **Markdown Slider:** Control the promotional discount intensity applied to failing lines.



## How to Run the App Locally

Ensure you have your environment dependencies installed, then run the engine locally:

```bash
# Install the required technical stack
pip install streamlit pandas numpy matplotlib seaborn duckdb

# Stream the app server locally
python3 -m streamlit run app.py
```

---
📄 **License:** This project is open-source and available under the **MIT License**.
