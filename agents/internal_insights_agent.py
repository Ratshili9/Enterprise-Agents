from agents.llm_client import generate_text
from tools.memory_tools import read_memory_bank, write_memory_bank

class InternalInsightsAgent:
    def run(self, context: dict) -> bool:
        """Generates internal business insights using LLM and long-term memory."""
        print("\n=== 3A. PARALLEL: Internal Insights Agent Running ===")
        if 'cleaned_df' not in context or 'profile_report' not in context: return False
            
        profile = context['profile_report']
        data_snapshot = context['cleaned_df'].head().to_string()
        
        # --- Long-Term Memory Integration ---
        memory_data = read_memory_bank()
        past_insights = "\n".join([f"- {i['date']}: {i['insight']}" for i in memory_data['past_insights'][-3:]]) # last 3 runs
        if not past_insights: past_insights = "No past analysis found."

        prompt = f"""
        You are an expert internal data analyst. Generate 3 key insights.
        
        **PAST INSIGHTS (for context/comparison):**
        {past_insights}
        
        **CURRENT DATA:**
        {profile}
        {data_snapshot}
        
        Based on the CURRENT DATA (and considering the past trends), provide three professional, actionable internal insights.
        """
        
        insights = generate_text(prompt)
        
        # Save the new insight to Long-Term Memory
        write_memory_bank(insights)
        
        # Save result to session context
        context['internal_insights'] = insights
        print("Internal Insights Agent Finished.")
        return True