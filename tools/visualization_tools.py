# tools/visualization_tools.py (The Corrected, Robust Version)
import matplotlib
matplotlib.use("Agg")

import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_sales_over_time(df, save_path):
    """
    Generates a sales trend plot, making the function robust against 
    inconsistent column names and ensuring the output directory exists.
    """
    print(f"--- [TOOL:Viz] Plotting sales over time to {save_path} ---")

    # 1. CRITICAL FIX: Ensure output directory exists before saving
    # os.path.dirname(save_path) extracts 'reports/plots'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 2. CRITICAL FIX: Clean up ALL column names to prevent KeyErrors
    df.columns = df.columns.str.strip()

    # 3. Convert all numeric-looking columns from strings to numbers
    # We must operate on a copy of the dataframe slice to avoid SettingWithCopyWarning
    df_plot = df.copy()
    for col in df_plot.columns:
        # Note: Using errors='coerce' is generally safer than 'ignore' for cleaning
        df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')

    # --- Sales Calculation Logic (More robust than picking the first numeric column) ---

    # Identify price-like and quantity-like columns
    price_col = next((col for col in df_plot.columns if 'price' in col.lower(
    ) or 'cost' in col.lower() and df_plot[col].dtype in [np.float64, np.int64]), None)
    quantity_col = next((col for col in df_plot.columns if 'quantity' in col.lower(
    ) or 'units' in col.lower() and df_plot[col].dtype in [np.float64, np.int64]), None)

    if price_col and quantity_col:
        df_plot['TotalSale'] = df_plot[price_col] * df_plot[quantity_col]
        sales_col = 'TotalSale'
        print(f"Calculated TotalSale using {price_col} * {quantity_col}.")
    else:
        # Fallback: Use the largest available numeric column if TotalSale cannot be calculated
        numeric_cols = df_plot.select_dtypes(
            include=['int64', 'float64']).columns.tolist()
        if not numeric_cols:
            raise ValueError("No numeric columns found. Cannot plot sales.")

        # Pick the column with the largest max value, assuming it's the sales column
        sales_col = df_plot[numeric_cols].max().idxmax()
        print(f"Warning: Using single column '{sales_col}' as sales amount.")

    # --- Date Detection Logic ---

    date_col = None
    for col in df_plot.columns:
        if "date" in col.lower():
            date_col = col
            # Ensure the date column is in datetime format
            df_plot[date_col] = pd.to_datetime(
                df_plot[date_col], errors='coerce')
            break

    if date_col is None:
        # Create artificial index if no date column
        df_plot["__index"] = range(len(df_plot))
        date_col = "__index"

    # --- Plotting ---

    # Aggregate sales by date for a clearer trend line
    if date_col != "__index":
        daily_sales = df_plot.groupby(date_col)[sales_col].sum().reset_index()
        daily_sales.plot(x=date_col, y=sales_col, figsize=(10, 6))
    else:
        df_plot.plot(x=date_col, y=sales_col, figsize=(10, 6))

    plt.title(f"Sales Trend: {sales_col}")
    plt.xlabel(date_col.replace('_', ' ').title())
    plt.ylabel(sales_col.replace('_', ' ').title())
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

    return save_path


def plot_top_products(df: pd.DataFrame, output_path: str) -> str:
    """Plots the top 5 products by revenue using a smart fallback for sales calculation."""
    print(f"--- [TOOL:Viz] Plotting top products to {output_path} ---")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    numeric_cols = df.select_dtypes(
        include=['int64', 'float64']).columns.tolist()

    if len(numeric_cols) < 2:
        if len(numeric_cols) == 1:
            sales_col = numeric_cols[0]
            df['TotalSale'] = df[sales_col]
        else:
            raise ValueError(
                "No suitable numeric columns found for plotting product revenue.")
    else:
        col1, col2 = numeric_cols[0], numeric_cols[1]
        df['TotalSale'] = df[col1] * df[col2]

    top_products = df.groupby(
        'Product')['TotalSale'].sum().nlargest(5).reset_index()

    # --- The rest of the function remains the same ---
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_products, x='TotalSale', y='Product', orient='h')
    plt.title('Top 5 Products by Revenue (Calculated)')
    plt.xlabel('Total Revenue')
    plt.ylabel('Product')
    plt.savefig(output_path)
    plt.close()
    return output_path
