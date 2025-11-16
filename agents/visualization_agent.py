import os
from tools.visualization_tools import (
    find_best_columns,
    create_time_series_plot,
    create_categorical_comparison_plot,
    create_correlation_heatmap
)

class VisualizationAgent:
    """
    The Visualization Agent generates and saves key diagnostic and summary plots.
    It now uses a column-agnostic approach based on data type and count.
    """
    def __init__(self):
        # Clear old plots before starting
        if os.path.exists("reports/plots"):
            for f in os.listdir("reports/plots"):
                os.remove(os.path.join("reports/plots", f))
        
    def run(self, context: dict) -> bool:
        print("🎨 [Viz] Starting Visualization Agent...")
        
        if 'cleaned_df' not in context:
            print("Visualization Agent Error: Cleaned DataFrame not found in context.")
            return False

        df_clean = context['cleaned_df']
        
        # 1. Dynamically find the best columns
        target_col, group_col = find_best_columns(df_clean)
        
        if not target_col:
            print("Visualization Agent Warning: Could not find a suitable numeric column to plot.")
            context['plot_paths'] = {"status": "Failed due to missing numeric data."}
            return False

        plot_paths = {}

        # 2. Time Series Plot (will skip for insurance.csv, but remains for flexibility)
        plot_paths['time_series'] = create_time_series_plot(df_clean, target_col)
        
        # 3. Categorical Comparison Plot (e.g., Average charges by region)
        if group_col:
            plot_paths['categorical_comparison'] = create_categorical_comparison_plot(df_clean, target_col, group_col)
        else:
            plot_paths['categorical_comparison'] = "N/A: No suitable categorical column found."

        # 4. Correlation Heatmap
        plot_paths['correlation_heatmap'] = create_correlation_heatmap(df_clean)
        
        context['plot_paths'] = plot_paths
        
        print("✅ [Viz] Visualization complete.")
        return True