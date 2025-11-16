import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the output directory
PLOT_DIR = "reports/plots"

def find_best_columns(df: pd.DataFrame):
    """Identifies the best numeric column (target) and best categorical column (group) dynamically."""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Prioritize 'charges' or the column with the highest variance if 'charges' is not found
    target_col = None
    if 'charges' in numeric_cols:
        target_col = 'charges'
    elif numeric_cols:
        # Pick the numeric column with the highest number of unique values (most descriptive)
        numeric_uniques = {col: df[col].nunique() for col in numeric_cols}
        target_col = max(numeric_uniques, key=numeric_uniques.get)
        
    # Find the best categorical column (high cardinality, but not too high)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    group_col = None
    
    if categorical_cols:
        # Filter columns that have between 2 and 10 unique values (good for group-by analysis)
        suitable_categories = [
            col for col in categorical_cols if 2 <= df[col].nunique() <= 10
        ]
        
        # Prioritize 'region' or 'smoker' if present, otherwise take the first suitable one
        if 'region' in suitable_categories:
            group_col = 'region'
        elif 'smoker' in suitable_categories:
            group_col = 'smoker'
        elif suitable_categories:
            group_col = suitable_categories[0]
            
    if not target_col:
        print("Visualization Error: No suitable numeric column found.")
        return None, None
        
    return target_col, group_col

def create_time_series_plot(df: pd.DataFrame, target_col: str) -> str:
    """
    Generates a simple time series plot of the target column if a date column exists.
    For this generic pipeline, we'll skip if no obvious date column exists.
    """
    print(f"--- [TOOL:Viz] Creating Time Series Plot for {target_col} (Skipping for insurance.csv)---")
    
    # Since insurance.csv has no date column, we'll skip time series analysis.
    # In a real pipeline, we would look for a date column and aggregate daily data.
    return "N/A: Data is cross-sectional (no date/time column)."


def create_categorical_comparison_plot(df: pd.DataFrame, target_col: str, group_col: str) -> str:
    """
    Generates a bar plot comparing the mean of the target_col across categories in group_col.
    """
    if not target_col or not group_col:
        return "N/A: Missing suitable target or group column for categorical plot."
        
    print(f"--- [TOOL:Viz] Creating Categorical Comparison Plot: {target_col} by {group_col} ---")
    
    try:
        # Calculate mean target (charges) per group (e.g., region)
        plot_data = df.groupby(group_col)[target_col].mean().sort_values(ascending=False).reset_index()

        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=group_col, 
            y=target_col, 
            data=plot_data, 
            palette="viridis"
        )
        
        # Formatting
        plt.title(f'Average {target_col.title()} by {group_col.title()}')
        plt.xlabel(group_col.title())
        plt.ylabel(f'Average {target_col.title()}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save the plot
        file_name = f"avg_{target_col}_by_{group_col}.png"
        output_path = os.path.join(PLOT_DIR, file_name)
        plt.savefig(output_path)
        plt.close()

        return output_path
        
    except Exception as e:
        return f"N/A: Error creating categorical plot: {e}"


def create_correlation_heatmap(df: pd.DataFrame) -> str:
    """
    Generates a heatmap of numeric column correlations.
    """
    print("--- [TOOL:Viz] Creating Correlation Heatmap ---")
    
    try:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return "N/A: Not enough numeric columns (less than 2) for correlation analysis."
            
        corr_matrix = numeric_df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix, 
            annot=True, 
            cmap='coolwarm', 
            fmt=".2f", 
            linewidths=.5, 
            linecolor='black'
        )
        
        plt.title('Numeric Feature Correlation Heatmap')
        plt.tight_layout()

        # Save the plot
        output_path = os.path.join(PLOT_DIR, "correlation_heatmap.png")
        plt.savefig(output_path)
        plt.close()

        return output_path
        
    except Exception as e:
        return f"N/A: Error creating heatmap: {e}"