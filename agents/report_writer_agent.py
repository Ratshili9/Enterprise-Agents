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

    # -----------------------------------------------------------
    # 🔧 UTIL: Convert numpy values to JSON-safe native Python
    # -----------------------------------------------------------
    def _convert_numpy_types(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)

        elif isinstance(obj, (np.floating, np.float64)):
            if np.isnan(obj):
                return None
            return float(obj)

        elif isinstance(obj, dict):
            return {k: self._convert_numpy_types(v) for k, v in obj.items()}

        elif isinstance(obj, list):
            return [self._convert_numpy_types(v) for v in obj]

        elif isinstance(obj, pd.DataFrame):
            # Convert each cell to Python type
            safe_df = obj.applymap(self._convert_numpy_types)
            return safe_df.head(10).to_markdown(index=False)

        return obj

    # -----------------------------------------------------------
    # 🔧 BUILD LLM PROMPT
    # -----------------------------------------------------------
    def _prepare_final_prompt(self, context: dict) -> str:

        # Build safe plot list
        plots_dir = "reports/plots"
        plot_files = []
        if os.path.exists(plots_dir):
            plot_files = [f for f in os.listdir(
                plots_dir) if f.endswith(".png")]

        # Base report data
        report_data = {
            "Data_Profile": self._convert_numpy_types(context.get("profile_report", "N/A")),
            "Internal_Insights": context.get("insights_report", "N/A"),
            "External_Context": context.get("external_context", "N/A"),
            "Recommendation_Report": context.get("recommendation_report", "N/A"),
            "ML_Reports_Summary": self._convert_numpy_types(context.get("ml_reports", {})),
            "Plot_Files": plot_files,
        }

        # ----------------------------------------
        # Load all ML CSV outputs (if any)
        # ----------------------------------------
        if 'ml_reports' in context:
            ml_summary = {}

            for key, item in context['ml_reports'].items():

                # Case 1: Value is a CSV file path
                if isinstance(item, str) and item.endswith(".csv") and os.path.exists(item):
                    try:
                        df = pd.read_csv(item)
                        # Ensure conversion to native types before to_markdown
                        ml_summary[key] = self._convert_numpy_types(
                            df).head(10).to_markdown(index=False)
                    except Exception as e:
                        ml_summary[key] = f"Error loading CSV: {e}"

                # Case 2: Value is a dict (model metrics or JSON)
                elif isinstance(item, dict):
                    ml_summary[key] = self._convert_numpy_types(item)

                # Case 3: Value is a string or list that needs type safety
                elif isinstance(item, (str, list)):
                    ml_summary[key] = self._convert_numpy_types(item)

            report_data["ML_Data_Summaries"] = ml_summary

        # ----------------------------------------
        # Construct Prompt
        # ----------------------------------------
        # Use simple conversion to ensure no numpy types linger in the prompt JSON
        report_data_safe = self._convert_numpy_types(report_data)
        readable_json = json.dumps(report_data_safe, indent=2)

        prompt = (
            "You are a Senior Business Analyst. Based on the following structured data, "
            "write a clear, professional, 500-700 word Markdown report.\n\n"
            "The report MUST include:\n"
            "1. **Executive Summary**\n"
            "2. **Key Findings**\n"
            "3. **Trends & Insights** (from internal + external data)\n"
            "4. **Machine Learning Analysis Summary**\n"
            "5. **Strategic Recommendations**\n\n"
            "Do NOT include the raw JSON. Use it only as reference.\n"
            "Below is the structured data:\n\n"
            "------------------------------\n"
            f"{readable_json}\n"
            "------------------------------\n"
        )

        return prompt

    # -----------------------------------------------------------
    # 🔧 RUN AGENT (UPDATED to return context)
    # -----------------------------------------------------------
    def run(self, context: dict) -> dict:  # Updated return type to dict
        print("📝 [Report] Writing report...")

        os.makedirs("reports", exist_ok=True)

        final_prompt = self._prepare_final_prompt(context)

        print("--- [TOOL:LLM] Calling Gemini to synthesize final report... ---")
        final_report = generate_report_content(final_prompt)

        # LLM failed
        if not final_report or final_report.startswith("Error:"):
            print("❌ [Report] LLM failed, saving fallback file.")

            context["final_report_status"] = "FAILURE (LLM Error)"
            context["final_report_content"] = "Report generation failed due to an LLM error."

            with open("reports/final_analysis_report.md", "w", encoding="utf-8") as f:
                f.write("# REPORT GENERATION FAILED\n\n")
                f.write("LLM error. Raw prompt was:\n\n")
                f.write(final_prompt)

            # Critical: Always return the context, even if failed.
            return context

        # Write final report
        try:
            with open("reports/final_analysis_report.md", "w", encoding="utf-8") as f:
                f.write(final_report)

            # Critical: Update context with the successful output
            context["final_report_status"] = "SUCCESS"
            context["final_report_content"] = final_report

            print("✅ [Report] Report saved successfully and context updated.")
            return context  # Critical: Return the updated context

        except Exception as e:
            print(f"❌ [Report] Could not write report: {e}")

            context["final_report_status"] = f"FAILURE (File Write Error: {e})"
            context["final_report_content"] = "Report file could not be written."

            # Critical: Always return the context, even if failed.
            return context
