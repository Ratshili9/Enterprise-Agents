import pandas as pd
from io import StringIO
import os


def load_data(csv_path: str) -> pd.DataFrame:
    """Loads a CSV file into a pandas DataFrame."""
    print(f"--- [TOOL:Data] Loading data from {csv_path} ---")

    try:
        with open(csv_path, 'r', encoding='latin-1') as f:
            # Added: header=0 to guarantee the first row is the header
            # Added: skipinitialspace=True to handle spaces after delimiters
            df = pd.read_csv(f, header=0, skipinitialspace=True)

        # Guarantee header names are clean by stripping whitespace
        df.columns = df.columns.str.strip()

        # Ensure OrderDate is correctly converted
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def get_data_profile(df: pd.DataFrame) -> str:
    """Generates a high-level text profile of the DataFrame."""
    print("--- [TOOL:Data] Generating data profile ---")
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    profile = "### Data Profile Report ###\n\n"
    profile += info_str
    profile += "\n\n2. Descriptive Statistics (Numerical):\n"
    # Include non-numeric summary
    profile += df.describe(include='all').to_string()
    return profile


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Performs basic data cleaning: dropping nulls, duplicates, and ensuring types/names."""
    print("--- [TOOL:Data] Cleaning data (handling nulls and duplicates) ---")
    original_rows = len(df)
    
    # 1. CRITICAL FIX: Standardize column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # 2. FORCE TYPE CONVERSION
    # Convert Price and Quantity to numeric, forcing errors to NaN
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    
    # 3. Fill and Drop (Original logic)
    df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median())
    df['Price'] = df['Price'].fillna(df['Price'].mean())
    df_cleaned = df.dropna().drop_duplicates()
    
    print(f"Original rows: {original_rows}, Cleaned rows: {len(df_cleaned)}")
    return df_cleaned