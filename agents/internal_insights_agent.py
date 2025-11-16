import pandas as pd
import json
from agents.llm_client import generate_text
from tools.memory_tools import read_memory_bank, write_insight_to_memory  # <-- NEW IMPORT


class InternalInsightsAgent:
    """
    Analyzes the cleaned DataFrame to generate key internal insights.
    It now incorporates past insights from the memory bank to provide historical context.
    """

    def __init__(self):
        # We want this agent to be the one that uses the memory bank for context
        pass

    def _prepare_prompt(self, df_clean: pd.DataFrame, past_insights: list[dict]) -> str:
        """Constructs the LLM prompt including data summary and past insights."""

        # 1. Summarize the current dataset (top 5 rows and statistics)
        data_summary = f"Data Head:\n{df_clean.head().to_markdown(index=False)}\n\n"
        data_summary += f"Descriptive Statistics:\n{df_clean.describe().to_markdown()}\n\n"
        data_summary += f"Data Types:\n{df_clean.dtypes.to_markdown()}"

        # 2. Integrate past insights from memory
        memory_summary = "No past insights available."
        if past_insights:
            memory_list = "\n".join([
                f"- [From {i['date']} by {i['source']}]: {i['insight']}"
                for i in past_insights
            ])
            memory_summary = f"Past key findings from previous runs:\n{memory_list}"

        # 3. Final Prompt
        prompt = f"""
        # Internal Data Analysis Task

        **Objective:** Analyze the current clean dataset and historical context to extract 3-5 critical, non-obvious business insights.
        
        **Instructions:**
        1. Focus on correlations, trends in the descriptive statistics, and group-by anomalies (e.g., how 'smoker' status impacts 'charges').
        2. Specifically comment on whether the current data aligns with or deviates from the **Past Insights** provided.
        3. Output only the key insights in a clean Markdown format.
        
        ---
        
        **CURRENT CLEAN DATA SUMMARY:**
        {data_summary}
        
        ---
        
        **PAST INSIGHTS (Historical Context):**
        {memory_summary}
        
        ---
        
        **OUTPUT FORMAT EXAMPLE:**
        
        ## Key Internal Insights
        
        * **Insight 1:** [Detail of first finding...]
        * **Insight 2:** [Detail of second finding...]
        * ...
        """
        return prompt

    def run(self, context: dict) -> bool:
        print("--- [AGENT:Internal Insights] Starting internal data analysis ---")

        if 'cleaned_df' not in context:
            print(
                "Internal Insights Agent Error: Cleaned DataFrame not found in context.")
            return False

        df_clean = context['cleaned_df']

        # 1. Read past insights from memory
        past_insights = read_memory_bank()

        # 2. Generate LLM prompt
        prompt = self._prepare_prompt(df_clean, past_insights)

        # 3. Call LLM
        print("--- [TOOL:LLM] Generating internal insights ---")
        insights_content = generate_text(prompt)

        if insights_content.startswith("Error:"):
            print(
                f"Internal Insights Agent Error: LLM call failed: {insights_content}")
            context['insights_report'] = "Internal insight generation failed."
            return False

        # 4. Save the generated report content to context
        context['insights_report'] = insights_content

        # 5. Extract a single key finding and write it back to the memory bank
        # We'll take the first bullet point as the key finding for simplicity
        try:
            key_insight_match = next((
                line.strip()
                for line in insights_content.split('\n')
                if line.strip().startswith('*') or line.strip().startswith('-')
            ), "No single key insight extracted.")

            # Clean up the bullet point marker
            key_insight = key_insight_match.lstrip('*- ').strip()

            write_insight_to_memory(
                insight=key_insight,
                source="InternalInsightsAgent"
            )
        except Exception as e:
            print(
                f"Internal Insights Agent Warning: Failed to write to memory bank: {e}")

        print("--- [AGENT:Internal Insights] Analysis complete. ---")
        return True
