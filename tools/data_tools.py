import pandas as pd
import numpy as np

def load_data(csv_path: str) -> pd.DataFrame:
    """Loads a CSV file from the given path."""
    print(f"--- [TOOL:Data] Loading data from {csv_path} ---")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at path: {csv_path}")
    
    # Simple check for 'charges' or 'TotalSale' to ensure it's numeric for cleaning
    if 'charges' in df.columns:
        df['charges'] = pd.to_numeric(df['charges'], errors='coerce')
    
    return df

def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Performs basic data cleaning (imputation, dropping duplicates)."""
    df = df_raw.copy()
    
    # Impute missing numeric data with the mean
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].mean())
        
    # Drop rows with remaining NaNs (usually from object/string columns)
    df.dropna(inplace=True)
    
    # Ensure charges (our target) is numeric
    if 'charges' in df.columns:
        df['charges'] = pd.to_numeric(df['charges'], errors='coerce')
        df.dropna(subset=['charges'], inplace=True)
        
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    return df

def get_data_profile(df: pd.DataFrame) -> dict:
    """Generates a basic data profile summary."""
    profile = {
        "shape": df.shape,
        "columns": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df.describe(include='all').to_dict()
    }
    return profile