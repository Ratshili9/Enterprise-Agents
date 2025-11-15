from tools.data_tools import clean_data

class DataCleanerAgent:
    def run(self, context: dict) -> bool:
        """Cleans 'raw_df' and saves 'cleaned_df'."""
        print("\n=== 2. SEQUENTIAL: Data Cleaner Agent Running ===")
        if 'raw_df' not in context: return False
            
        raw_df = context['raw_df']
        cleaned_df = clean_data(raw_df)
        
        context['cleaned_df'] = cleaned_df
        print("Cleaner Agent Finished.")
        return True