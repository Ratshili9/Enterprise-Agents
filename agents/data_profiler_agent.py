from tools.data_tools import load_data, get_data_profile

class DataProfilerAgent:
    def run(self, context: dict, file_path: str) -> bool:
        """Loads data and generates a profile."""
        print("\n=== 1. SEQUENTIAL: Data Profiler Agent Running ===")
        df = load_data(csv_path=file_path)
        if df is None: return False
        
        profile_report = get_data_profile(df)
        
        # Save state to the shared context (Session Memory)
        context['raw_df'] = df
        context['profile_report'] = profile_report
        
        print("Profiler Agent Finished.")
        return True