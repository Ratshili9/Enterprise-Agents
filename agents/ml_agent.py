import os
import pandas as pd
from tools.ml_tools import (
    prepare_time_series_data, 
    predict_sales_forecast, 
    detect_anomalies, 
    predict_demand_by_category
)

class MLAgent:
    """
    The Machine Learning Agent executes various predictive models and anomaly detection.
    
    It relies on context['cleaned_df'] and stores results in context['ml_reports'].
    """
    def __init__(self):
        # Placeholder for dynamic configuration
        pass

    def run(self, context: dict) -> bool:
        """
        Runs the full suite of ML analysis.
        
        Args:
            context: The shared dictionary containing 'cleaned_df'.
            
        Returns:
            True if ML analysis was successful, False otherwise.
        """
        print("--- [AGENT:ML] Starting Machine Learning Analysis ---")
        
        if 'cleaned_df' not in context:
            print("ML Agent Error: Cleaned DataFrame not found in context.")
            return False

        df_clean = context['cleaned_df']
        ml_reports = {}

        # 1. Prepare Time Series Data
        df_ts = prepare_time_series_data(df_clean)
        if df_ts is None:
            print("ML Agent Warning: Time series data could not be prepared.")
        
        # 2. Sales Forecasting (Time Series)
        print("--- [TOOL:ML] Predicting sales forecast...")
        forecast_path = predict_sales_forecast(df_ts, steps=14)
        ml_reports['sales_forecast_path'] = forecast_path

        # 3. Anomaly Detection
        print("--- [TOOL:ML] Detecting transaction anomalies...")
        anomalies_path = detect_anomalies(df_clean)
        ml_reports['anomalies_path'] = anomalies_path

        # 4. Category Demand Prediction
        # NOTE: We assume a 'Category' column exists in the data.
        print("--- [TOOL:ML] Predicting category demand trend...")
        demand_path = predict_demand_by_category(df_clean, category_col='Category') 
        ml_reports['demand_predictions_path'] = demand_path

        # Store all paths in context for the Recommendation Agent and Report Writer
        context['ml_reports'] = ml_reports
        
        print(f"--- [AGENT:ML] Analysis complete. {len(ml_reports)} reports generated. ---")
        return True