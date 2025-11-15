from tools.search_tools import adk_built_in_search

class ExternalContextAgent:
    def run(self, context: dict) -> bool:
        """
        Uses the built-in search tool to enrich the report with external market context.
        """
        print("\n=== 3B. PARALLEL: External Context Agent Running ===")
        if 'profile_report' not in context: return False
            
        # Analyze the data profile to determine the search query
        profile = context['profile_report']
        
        # Simple logic: extract main categories from the profile
        # Since our mock data is Electronics and Food, we search for that.
        query = "Current market trends for electronics and food industries 2025" 
        
        # --- Built-in Tool Call (Simulated) ---
        search_results = adk_built_in_search(query)
        
        # Save external context to session context
        context['external_context'] = search_results
        print("External Context Agent Finished.")
        return True