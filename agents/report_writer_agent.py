import json
import os
import numpy as np
import pandas as pd

from agents.llm_client import generate_report_content 

class ReportWriterAgent:
    """
    The final agent. It gathers all data, reports, plots, and recommendations
    from the context and synthesizes the final analysis report using the LLM.
    """
    def __init__(self):
        pass

    def _convert_numpy_types(self, obj):
        """Recursively converts numpy types to native Python types for JSON serialization."""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            # Convert NaN to None, which JSON handles
            if np.isnan(obj): return None
            return float(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(elem) for elem in obj]
        elif isinstance(obj, pd.DataFrame):
            # Convert DataFrame to a simple dict or string representation
            return obj.head().to_markdown(index=False)
        return obj

    def _prepare_final_prompt(self, context: dict) -> str:
        """Constructs the comprehensive prompt for the Report Writer LLM."""
        
        # Filter context data to include only serializable reports and paths
        report_data = {
            "Data_Profile": self._convert_numpy_types(context.get("profile_report", "N/A")),
            "Internal_Insights": context.get("insights_report", "N/A"),
            "External_Context": context.get("external_context", "N/A"),
            "Recommendation_Report": context.get("recommendation_report", "N/A"),
            "ML_Reports_Summary": self._convert_numpy_types(context.get("ml_reports", {})),
            "Plot_Files": [f for f in os.listdir("reports/plots") if f.endswith('.png')] if os.path.exists("reports/plots") else [],
        }
        
        # Load ML CSV content summaries to provide concrete data to the LLM
        if 'ml_reports' in context:
            ml_summary = {}
            for key, path in context['ml_reports'].items():
                if isinstance(path, str) and path.endswith('.csv') and os.path.exists(path):
                    try:
                        df = pd.read_csv(path)
                        # Ensure numeric data types are converted before markdown conversion
                        df_for_llm = df.apply(lambda x: [self._convert_numpy_types(val) for val in x] if x.dtype in ['float64', 'int64'] else x)
                        ml_summary[key] = df_for_llm.to_markdown(index=False)
                    except Exception as e:
                        ml_summary[key] = f"Could not load CSV: {e}"
            report_data['ML_Data_Summaries'] = ml_summary
        
        # Convert the structured data into a detailed, readable string for the LLM
        prompt_parts = [
            "You are a Senior Business Analyst specializing in synthesizing complex data into actionable, "
            "professional Markdown reports. Your goal is to review the provided structured data "
            "(Profile, Insights, ML Predictions, Recommendations, Context) and generate a cohesive, "
            "well-written report, approximately 500-700 words long. "
            "The report must contain an Executive Summary, Key Findings, and Strategic Recommendations. "
            "Do not include the raw JSON data in the final report.",
            json.dumps(report_data, indent=2)
        ]
        
        return "\n".join(prompt_parts)


    def run(self, context: dict) -> bool:
        print("📝 [Report] Writing report...")
        
        final_prompt = self._prepare_final_prompt(context)

        print("--- [TOOL:LLM] Calling Gemini to synthesize final report... ---")
        # NOTE: This call now uses the function imported from agents.llm_client
        final_report_content = generate_report_content(final_prompt)
        
        if not final_report_content or final_report_content.startswith("Error:"):
            print(f"❌ [Report] LLM call failed or returned error: {final_report_content}")
            # Fallback: write a failed report with the raw prompt for debugging
            with open("reports/final_analysis_report.md", "w") as f:
                f.write("# REPORT GENERATION FAILED\n\nCould not generate final report from LLM. Raw prompt used for debugging:\n\n---\n" + final_prompt)
            return False

        try:
            # Save the final content received from the LLM
            with open("reports/final_analysis_report.md", "w", encoding="utf-8") as f:
                f.write(final_report_content)
                
            print("✅ [Report] Report successfully synthesized and saved.")
            return True

        except Exception as e:
            print(f"❌ [Report] Error writing final report to disk: {e}")
            return False