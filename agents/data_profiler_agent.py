import pandas as pd
from tools.data_tools import load_data, get_data_profile

class DataProfilerAgent:
    """
    Loads the raw data and generates a profile report.
    Crucially, it saves the raw DataFrame and profile to the context.
    """
    def __init__(self):
        pass

    def run(self, context: dict) -> bool:
        print("🔍 [Profiler] Loading CSV...")
        try:
            csv_path = context.get("data_path")
            if not csv_path or not isinstance(csv_path, str):
                print("Profiler Error: Invalid or missing 'data_path' in context.")
                return False

            df_raw = load_data(csv_path)
            
            # --- CRITICAL FIX: Save raw data to context for cleaning agent ---
            context["raw_df"] = df_raw
            
            profile = get_data_profile(df_raw)
            # Save profile report to context for Report Writer/LLMs
            context["profile_report"] = profile
            
            print(f"📊 [Profiler] Dataset Shape: {df_raw.shape}")
            print(f"📌 [Profiler] Columns: {list(df_raw.columns)}")
            print("✅ [Profiler] Profiling complete.")
            return True

        except FileNotFoundError as e:
            print(f"Profiler Error: {e}")
            return False
        except Exception as e:
            print(f"Profiler Error: An unexpected error occurred: {e}")
            return False