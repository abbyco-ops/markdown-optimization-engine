import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb

# Set page layout configuration at the very top
st.set_page_config(page_title="SQL Markdown Engine", layout="wide")

# ==========================================
# 1. DATABASE CONNECTIVITY & FEATURE ENGINEERING PIPELINE
# ==========================================
@st.cache_data
def load_and_aggregate_data():
    """
    Connects to the local database, ingests the custom CSV, and uses 
    relational SQL to aggregate transaction-level rows into product profiles.
    """
    conn = duckdb.connect('database.db')
    
    # Ingest the real CSV file directly into our database table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fashion_sales AS 
        SELECT * FROM read_csv_auto('fashion_boutique_dataset.csv');
    """)
    
    # Run an advanced SQL query to aggregate transactions into product profiles
    # This automatically computes units sold, current stock, and lifetime STR metrics
    aggregation_query = """
        SELECT 
            product_id,
            ANY_VALUE(category) AS category,
            ANY_VALUE(brand) AS brand,
            ANY_VALUE(season) AS season,
            MAX(original_price) AS original_price,
            
            -- Summarize performance metrics from rows
            COUNT(product_id) AS transactional_units_sold,
            MAX(stock_quantity) AS remaining_inventory_level,
            
            -- Estimate initial stock: sold units + current remaining units
            (COUNT(product_id) + MAX(stock_quantity)) AS calculated_initial_stock,
            
            -- Compute the Sell-Through Rate (STR) KPI
            ROUND((CAST(COUNT(product_id) AS FLOAT) / (COUNT(product_id) + MAX(stock_quantity))) * 100, 2) AS str_percentage
            
        FROM fashion_sales
        WHERE product_id IS NOT NULL
        GROUP BY product_id;
    """
    
    df = conn.execute(aggregation_query).fetchdf()
    conn.close()
    return df

# ==========================================
# 2. THE LOGIC ENGINE (DYNAMIC SQL RULES)
# ==========================================
def run_optimization_engine_sql(df, str_threshold, markdown_pct):
    """
    Applies strategic markdown logic across inventory profiles using 
    in-memory SQL execution via DuckDB.
    """
    discount_multiplier = 1 - (markdown_pct / 100)
    
    sql_query = f"""
        SELECT 
            product_id,
            category,
            brand,
            season,
            original_price,
            remaining_inventory_level,
            calculated_initial_stock,
            str_percentage,
            
            -- Algorithmic Tranching conditional parameters
            CASE 
                WHEN str_percentage < {str_threshold} THEN 'TRIGGER MARKDOWN'
                ELSE 'HOLD PRICE'
            END AS action_required,
            
            CASE 
                WHEN str_percentage < {str_threshold} THEN '{markdown_pct}%'
                ELSE '0%'
            END AS markdown_applied,
            
            CASE 
                WHEN str_percentage < {str_threshold} THEN ROUND(original_price * {discount_multiplier}, 2)
                ELSE original_price
            END AS current_retail_price
            
        FROM df
    """
    
    return duckdb.query(sql_query).to_df()

# ==========================================
# 3. INTERACTIVE RECRUITER DASHBOARD (UI)
# ==========================================
def main():
    st.title("💻 Enterprise Markdown Optimization Engine")
    st.markdown("This portfolio tool ingests transaction files, converts profiles via SQL, and surfaces markdown recommendations targeting underperforming lines.")
    
    # Execute Pipeline
    try:
        df_products = load_and_aggregate_data()
    except Exception as e:
        st.error(f"Pipeline Initialization Failed: {str(e)}")
        return

    # Sidebar Component Controls
    st.sidebar.header("🎯 Optimization Parameters")
    
    str_slider = st.sidebar.slider(
        "Critical STR Target (%)", 
        min_value=5, max_value=95, value=40, step=5,
        help="SKUs operating below this sell-through percentage will trigger markdown rules."
    )
    
    discount_slider = st.sidebar.slider(
        "Recommended Markdown (%)", 
        min_value=5, max_value=50, value=20, step=5,
        help="Discount rate applied to lagging lines to accelerate product turn rates."
    )
    
    # Process Model Strategies
    processed_df = run_optimization_engine_sql(df_products, str_slider, discount_slider)
    
    # Calculate Top Level High-Utility Metrics
    total_skus = len(processed_df)
    flagged_skus = len(processed_df[processed_df['action_required'] == "TRIGGER MARKDOWN"])
    avg_catalog_str = processed_df['str_percentage'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Catalog SKUs", total_skus)
    col2.metric("SKUs Flagged for Discounts", flagged_skus, f"{round((flagged_skus/total_skus)*100, 1)}% of Catalog", delta_color="inverse")
    col3.metric("Average System STR", f"{round(avg_catalog_str, 2)}%")
    
    st.divider()
    
    # Visual Analytics Layout Sections
    st.subheader("📊 Category Stagnation Dashboard Analytics")
    eda_col1, eda_col2 = st.columns(2)
    
    with eda_col1:
        st.markdown("**Average STR Performance by Merchandise Category**")
        fig, ax = plt.subplots(figsize=(6, 3.5))
        cat_data = processed_df.groupby('category')['str_percentage'].mean().sort_values()
        sns.barplot(x=cat_data.values, y=cat_data.index, ax=ax, palette="Blues_r")
        ax.set_xlabel("Average STR %")
        ax.set_ylabel("")
        st.pyplot(fig)
        
    with eda_col2:
        st.markdown("**Inventory Distribution Profiles (Initial Stock vs STR %)**")
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.scatterplot(
            data=processed_df, 
            x="calculated_initial_stock", 
            y="str_percentage", 
            hue="action_required", 
            ax=ax, 
            palette={"HOLD PRICE": "darkgray", "TRIGGER MARKDOWN": "#E24A33"}
        )
        ax.set_xlabel("Total Initial Volume (Units)")
        ax.set_ylabel("Sell-Through Rate %")
        st.pyplot(fig)
        
    st.divider()
    
    # Interactive Data Filtering Engine Component Matrix
    st.subheader("📋 Pricing Optimization Actions Matrix")
    
    cat_filter = st.selectbox("Filter Matrix View by Category", ["All Catalog Categories"] + list(processed_df['category'].unique()))
    display_df = processed_df.copy()
    if cat_filter != "All-Catalog Categories" and "All Catalog Categories" not in cat_filter:
        display_df = display_df[display_df['category'] == cat_filter]
        
    st.dataframe(
        display_df[['product_id', 'category', 'brand', 'season', 'original_price', 'current_retail_price', 'markdown_applied', 'remaining_inventory_level', 'str_percentage', 'action_required']],
        use_container_width=True
    )

if __name__ == '__main__':
    main()
