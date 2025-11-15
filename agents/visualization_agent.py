from tools.visualization_tools import plot_sales_over_time, plot_top_products
from config import PLOTS_DIR
import os


class VisualizationAgent:
    def run(self, context: dict) -> bool:
        """Generates plots from 'cleaned_df' and saves 'plot_paths'."""
        print("\n=== 3C. PARALLEL: Visualization Agent Running ===")
        if 'cleaned_df' not in context:
            return False

        df = context['cleaned_df']
        plot_paths = []

        # Generate plots and collect their file paths
        sales_path = plot_sales_over_time(
            df, os.path.join(PLOTS_DIR, 'sales_trend.png'))
        if sales_path:
            plot_paths.append(sales_path)

        products_path = plot_top_products(
            df, os.path.join(PLOTS_DIR, 'top_products.png'))
        if products_path:
            plot_paths.append(products_path)

        context['plot_paths'] = plot_paths
        print("Visualization Agent Finished.")
        return True
