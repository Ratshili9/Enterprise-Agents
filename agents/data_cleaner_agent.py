import pandas as pd
from tools.data_tools import clean_data


class DataCleanerAgent:
    """
    Takes the raw DataFrame from context, cleans it, and saves the cleaned DataFrame
    back into the context for use by parallel and ML agents.
    """

    def __init__(self):
        pass

    def run(self, context: dict) -> bool:
        print("🧹 [Cleaner] Cleaning data...")

        # Ensure raw data is available from the Profiler
        if 'raw_df' not in context:
            print(
                "Cleaner Error: Raw DataFrame not found in context. Run Profiler first.")
            return False

        try:
            df_raw = context['raw_df']
            df_clean = clean_data(df_raw)

            # --- CRITICAL FIX: Save cleaned data to context for ML, Viz, and Insights agents ---
            context["cleaned_df"] = df_clean

            print("✅ [Cleaner] Cleaning complete.")
            return True

        except Exception as e:
            print(f"Cleaner Error: An unexpected error occurred: {e}")
            return False
