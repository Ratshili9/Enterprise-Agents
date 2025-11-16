import json
from agents.llm_client import generate_text


class ExternalContextAgent:
    """
    Uses the Google Search Grounding tool via the LLM to fetch real-time 
    external context (market trends, news) relevant to the data analysis.
    The LLM synthesizes the search results and provides citations.
    """

    def __init__(self):
        # System instructions to guide the LLM's role for external search
        self.system_prompt = (
            "You are a specialized Market Research Analyst. Your task is to use Google Search "
            "to find current, high-level market trends, news, and external factors that could "
            "impact the business sector associated with the user's data (e.g., insurance, "
            "healthcare, etc.). Synthesize these findings into a concise, 2-3 paragraph "
            "report. Do not mention the search terms used. Rely entirely on the information "
            "found by the search tool."
        )

    def _prepare_prompt(self, data_columns: list) -> str:
        """Dynamically generates the prompt based on the dataset's columns."""

        # We look for keywords that suggest the industry (e.g., 'insurance', 'charges', 'hospital')

        # In this example, the data is related to "insurance"
        if 'charges' in data_columns and 'smoker' in data_columns:
            industry_keyword = "health insurance and healthcare"
        elif 'sales' in data_columns or 'revenue' in data_columns:
            industry_keyword = "global consumer market"
        else:
            industry_keyword = "general economic"

        prompt = (
            f"Please conduct a grounded search for the most recent, high-impact external market trends "
            f"and economic factors currently affecting the **{industry_keyword}** industry as of today. "
            f"The final summary must be ready to include in an analytical report."
        )
        return prompt

    def run(self, context: dict) -> bool:
        print(
            "--- [AGENT:External Context] Starting grounded search for external context ---")

        if 'columns' not in context:
            print("External Context Agent Error: Data columns not found in context.")
            return False

        data_columns = context.get('columns', [])

        # 1. Prepare the LLM prompt
        llm_prompt = self._prepare_prompt(data_columns)

        # 2. Call LLM with Google Search tool enabled
        print("--- [TOOL:LLM] Calling Gemini with Google Search grounding ---")

        # The LLM Client will return a JSON string with {"text": ..., "sources": [...]}
        response_json_string = generate_text(
            prompt=llm_prompt,
            system_prompt=self.system_prompt,
            tools=[{"google_search": {}}]  # Enable grounding tool
        )

        if response_json_string.startswith("Error:"):
            print(
                f"External Context Agent Error: LLM call failed: {response_json_string}")
            context['external_context_report'] = "External context search failed."
            return False

        try:
            response_data = json.loads(response_json_string)
            report_text = response_data['text']
            sources = response_data['sources']

            # 3. Store the synthesized report and sources in context
            context['external_context_report'] = report_text
            context['external_context_sources'] = sources

            print(
                f"--- [AGENT:External Context] Found and synthesized {len(sources)} source(s). ---")

        except json.JSONDecodeError:
            print("External Context Agent Error: Failed to parse LLM response JSON.")
            context['external_context_report'] = "External context search failed due to JSON error."
            return False

        print("External Context Agent Finished.")
        return True
