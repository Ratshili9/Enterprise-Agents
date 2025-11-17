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
    The Machine Learning Agent executes time-series forecasting,
    anomaly detection, and category-level demand prediction.

    It relies on context['cleaned_df'] and stores its outputs in
    context['ml_reports'] for the Recommendation Agent.
    """

    def __init__(self):
        pass

    def run(self, context: dict) -> bool:
        print("\n--- [AGENT:ML] Starting Machine Learning Analysis ---")

        if "cleaned_df" not in context:
            print("ML Agent Error: cleaned_df missing in context")
            return False

        df_clean = context["cleaned_df"]
        ml_reports = {}

        # -----------------------------------------
        # 1. Prepare Time Series Data
        # -----------------------------------------
        print("--- [TOOL:ML] Preparing time series data...")
        df_ts = prepare_time_series_data(df_clean)

        if df_ts is None or df_ts.empty:
            print("ML Agent Warning: Could not prepare time-series data.")
        else:
            print("ML Agent: Time-series data prepared.")

        # -----------------------------------------
        # 2. Sales Forecasting
        # -----------------------------------------
        print("--- [TOOL:ML] Running sales forecast...")
        try:
            forecast_path = predict_sales_forecast(df_ts, steps=14)
        except Exception as e:
            print(f"Forecasting failed: {e}")
            forecast_path = None

        ml_reports["sales_forecast_path"] = forecast_path

        # -----------------------------------------
        # 3. Anomaly Detection
        # -----------------------------------------
        print("--- [TOOL:ML] Running anomaly detection...")
        try:
            anomalies_path = detect_anomalies(df_clean)
        except Exception as e:
            print(f"Anomaly detection failed: {e}")
            anomalies_path = None

        ml_reports["anomalies_path"] = anomalies_path

        # -----------------------------------------
        # 4. Category Demand Predictions
        # -----------------------------------------
        print("--- [TOOL:ML] Predicting demand by category...")
        try:
            demand_path = predict_demand_by_category(
                df_clean, category_col="Category")
        except Exception as e:
            print(f"Demand prediction failed: {e}")
            demand_path = None

        ml_reports["demand_predictions_path"] = demand_path

        # -----------------------------------------
        # SAVE REPORTS INTO CONTEXT
        # -----------------------------------------
        context["ml_reports"] = ml_reports

        print(
            f"--- [AGENT:ML] Completed. Generated {len(ml_reports)} ML reports. ---\n")
        return True
