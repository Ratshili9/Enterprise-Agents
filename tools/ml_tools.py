import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA

# Define the output directory based on the new structure
ML_REPORT_DIR = "reports/ml"

def prepare_time_series_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Attempts to prepare data for time series analysis (e.g., sales forecasting).
    Assumes the cleaned DataFrame has 'TotalSale' and a suitable date column.
    """
    df_ts = df.copy()
    
    # 1. Find Date Column (Assume cleaner has ensured a 'Date' column exists if possible)
    date_col = next((col for col in df_ts.columns if 'date' in col.lower()), None)
    
    if date_col is None:
        print("ML Tool Error: No suitable date column found for time series analysis.")
        return None
        
    df_ts[date_col] = pd.to_datetime(df_ts[date_col], errors='coerce')
    df_ts.dropna(subset=[date_col], inplace=True)
    
    # 2. Find Sales Column (Assume cleaner/viz agent added 'TotalSale' or use the largest numeric)
    sales_col = next((col for col in df_ts.columns if 'totalsale' in col.lower()), None)
    if sales_col is None:
        numeric_cols = df_ts.select_dtypes(include=[np.float64, np.int64]).columns
        if len(numeric_cols) > 0:
            sales_col = numeric_cols[0]
        else:
            print("ML Tool Error: No numeric sales data available.")
            return None

    # 3. Aggregate daily sales for forecasting
    df_ts = df_ts.set_index(date_col).resample('D').agg({sales_col: 'sum'}).fillna(0)
    df_ts.rename(columns={sales_col: 'DailySales'}, inplace=True)
    return df_ts

def predict_sales_forecast(df_ts: pd.DataFrame, steps: int = 7) -> str:
    """
    Uses ARIMA model to predict future daily sales.
    """
    if df_ts is None or df_ts.empty:
        return "N/A: Time series data preparation failed."
        
    # Simple ARIMA (p, d, q) model for demonstration
    # p=1 (lagged values), d=1 (differencing), q=0 (moving average)
    try:
        model = ARIMA(df_ts['DailySales'], order=(1, 1, 0))
        model_fit = model.fit()
        
        # Forecast 'steps' days into the future
        forecast = model_fit.forecast(steps=steps)
        
        # Create a DataFrame for the forecast report
        forecast_df = pd.DataFrame({
            'Date': pd.to_datetime(forecast.index).strftime('%Y-%m-%d'),
            'Forecasted_Sales': np.round(forecast.values, 2)
        })
        
        output_path = os.path.join(ML_REPORT_DIR, "sales_forecast.csv")
        forecast_df.to_csv(output_path, index=False)
        return output_path
        
    except Exception as e:
        print(f"ML Tool Error during ARIMA forecasting: {e}")
        return f"N/A: Forecasting failed. {e}"


def detect_anomalies(df: pd.DataFrame, contamination_rate: float = 0.1) -> str:
    """
    Uses Isolation Forest to detect outlier transactions based on sales amount.
    """
    df_anomaly = df.copy()
    
    # Use sales amount for anomaly detection
    sales_col = next((col for col in df_anomaly.columns if 'totalsale' in col.lower()), None)
    if sales_col is None:
        return "N/A: Sales column not found for anomaly detection."

    # Train the Isolation Forest model
    X = df_anomaly[[sales_col]].values
    
    # Isolation Forest is effective for detecting outliers in data
    model = IsolationForest(contamination=contamination_rate, random_state=42)
    df_anomaly['Anomaly'] = model.fit_predict(X)
    
    # Filter for anomalies (where Anomaly == -1)
    anomalies_df = df_anomaly[df_anomaly['Anomaly'] == -1].drop(columns=['Anomaly'])
    
    output_path = os.path.join(ML_REPORT_DIR, "transaction_anomalies.csv")
    anomalies_df.to_csv(output_path, index=False)
    
    return output_path


def predict_demand_by_category(df: pd.DataFrame, category_col: str = 'Category') -> str:
    """
    Predicts demand (quantity) for each product category using simple linear regression
    based on the time index (a proxy for trend).
    """
    if category_col not in df.columns:
        return f"N/A: Category column '{category_col}' not found for demand prediction."
        
    # Assume 'Quantity' or 'Units' is the demand metric
    quantity_col = next((col for col in df.columns if 'quantity' in col.lower() or 'units' in col.lower()), None)
    if quantity_col is None:
        return "N/A: Quantity/Units column not found for demand prediction."
        
    results = []
    
    # 1. Create a time index (feature for linear regression)
    df['TimeIndex'] = range(len(df))
    
    for category in df[category_col].unique():
        category_df = df[df[category_col] == category].copy()
        
        # Aggregate quantity by time index (e.g., transaction order)
        X = category_df[['TimeIndex']].values 
        y = category_df[quantity_col].values
        
        # Simple Linear Regression to model the trend in demand
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast the next period's demand (e.g., transaction N+1)
        next_time_index = df['TimeIndex'].max() + 1
        predicted_demand = model.predict([[next_time_index]])[0]
        
        results.append({
            'Category': category,
            'Trend_Coefficient': np.round(model.coef_[0], 4),
            'Predicted_Next_Demand': np.round(predicted_demand, 2)
        })

    results_df = pd.DataFrame(results)
    output_path = os.path.join(ML_REPORT_DIR, "category_demand_predictions.csv")
    results_df.to_csv(output_path, index=False)
    
    return output_path