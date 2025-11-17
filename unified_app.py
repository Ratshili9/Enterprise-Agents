import streamlit as st
import json
import os
import pandas as pd
import numpy as np

# --- 1. MOCK LLM Client and Helper Function ---
# In a real setup, this would be your llm_client.py logic
def generate_report_content(prompt: str) -> str:
    """Mock LLM call to simulate report generation."""
    st.info("Simulating LLM call. This takes time in the real world...")
    
    # Simple mock output based on the provided data structure
    data_found = "Data Profile: Present. ML Models: Logistic Regression and Decision Tree were run."
    
    return f"""
# Final Business Analysis Report

## 1. Executive Summary
This project successfully analyzed internal and external data points to generate strategic recommendations. The key finding is the strong correlation between customer satisfaction and repeat purchase rate, primarily driven by product quality metrics.

## 2. Key Findings
- **Data Completeness:** The initial dataset was 98% complete.
- **ML Performance:** The Logistic Regression model achieved an accuracy of 0.88, slightly outperforming the Decision Tree (0.85).

## 3. Strategic Recommendations
1. **Focus on Quality Control:** Invest 15% more budget into QC based on the ML findings.
2. **Expand External Data:** Incorporate social media sentiment analysis for a more robust external context.

## 4. Analysis Data Reference
{data_found}
"""

# --- 2. AGENT DEFINITIONS (Conceptually placed in the same file) ---

# Mock Agent Classes (Replace these with your full agent logic)
class ProfilerAgent:
    def run(self, context: dict) -> dict:
        st.info("🏃‍♂️ Running Profiler Agent...")
        context["profile_report"] = {"rows": 1000, "cols": 12, "missing": 0.02}
        return context

class InsightsAgent:
    def run(self, context: dict) -> dict:
        st.info("🏃‍♂️ Running Insights Agent...")
        context["insights_report"] = "High seasonality found in sales data."
        context["external_context"] = "Market growth rate projected at 5%."
        return context

class MLAgent:
    def run(self, context: dict) -> dict:
        st.info("🏃‍♂️ Running ML Agent...")
        # Mock ML results: A dict for one model, a DataFrame (which needs numpy conversion) for another
        context["ml_reports"] = {
            "Logistic_Regression_Metrics": {
                "Accuracy": 0.88,
                "Precision": 0.89
            },
            "Decision_Tree_Results_Table": pd.DataFrame({
                'Feature': ['F1', 'F2', 'F3'],
                'Importance': [np.float64(0.45), np.float64(0.30), np.float64(0.25)]
            })
        }
        return context

# --- 3. ReportWriterAgent (The one we just fixed) ---

class ReportWriterAgent:
    """
    The final agent. It gathers all data and synthesizes the final report.
    (This is the corrected logic that updates and returns the context dictionary).
    """

    def _convert_numpy_types(self, obj):
        """Converts numpy types to standard Python types for JSON safety."""
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
            safe_df = obj.applymap(self._convert_numpy_types)
            return safe_df.head(10).to_markdown(index=False)
        return obj

    def _prepare_final_prompt(self, context: dict) -> str:
        """Constructs the LLM prompt using all collected data."""
        report_data = {
            "Data_Profile": self._convert_numpy_types(context.get("profile_report", "N/A")),
            "Internal_Insights": context.get("insights_report", "N/A"),
            "External_Context": context.get("external_context", "N/A"),
            "ML_Reports_Summary": self._convert_numpy_types(context.get("ml_reports", {})),
            "Plot_Files": [], # Mocking plots for this example
        }

        report_data_safe = self._convert_numpy_types(report_data)
        readable_json = json.dumps(report_data_safe, indent=2)

        prompt = (
            "You are a Senior Business Analyst. Based on the following structured data, "
            "write a clear, professional, 500-700 word Markdown report.\n\n"
            "The report MUST include:\n"
            "1. **Executive Summary**\n"
            "2. **Key Findings**\n"
            "3. **Trends & Insights**\n"
            "4. **Machine Learning Analysis Summary**\n"
            "5. **Strategic Recommendations**\n\n"
            "Do NOT include the raw JSON. Use it only as reference.\n"
            "Below is the structured data:\n\n"
            "------------------------------\n"
            f"{readable_json}\n"
            "------------------------------\n"
        )
        return prompt

    def run(self, context: dict) -> dict:
        st.info("📝 Running Report Writer Agent...")
        final_prompt = self._prepare_final_prompt(context)
        final_report = generate_report_content(final_prompt)

        if not final_report or final_report.startswith("#"): # Simple error check
            context["final_report_status"] = "FAILURE"
            context["final_report_content"] = "Report generation failed."
            return context

        context["final_report_status"] = "SUCCESS"
        context["final_report_content"] = final_report
        return context

# --- 4. THE UNIFIED PIPELINE FUNCTION ---

def run_full_pipeline(initial_context: dict) -> dict:
    """Orchestrates all agents sequentially."""
    st.subheader("Pipeline Execution Log")
    context = initial_context

    # CRITICAL: We MUST reassign the 'context' variable with the return value
    # from each agent's run method to ensure memory is updated!

    # 1. Run Profiler
    profiler = ProfilerAgent()
    context = profiler.run(context)

    # 2. Run Insights
    insights = InsightsAgent()
    context = insights.run(context)

    # 3. Run ML
    ml_agent = MLAgent()
    context = ml_agent.run(context)

    # 4. Run Report Writer
    writer = ReportWriterAgent()
    context = writer.run(context)
    
    st.success("✅ Pipeline Complete!")
    return context

# --- 5. STREAMLIT DASHBOARD (The new main entry point) ---

def main():
    st.set_page_config(
        page_title="Unified Agent Analysis Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 Data Analysis & Reporting System")

    # Initialize session state for context/memory
    if 'pipeline_context' not in st.session_state:
        st.session_state.pipeline_context = {}
        st.session_state.report_content = None

    # --- Sidebar for Inputs ---
    with st.sidebar:
        st.header("1. Configuration")
        # In a real app, you would upload a file here
        st.file_uploader("Upload Data File (Mocked)", type=['csv', 'xlsx'])
        
        # User prompt input
        user_prompt = st.text_area(
            "Analysis Goal/Prompt:",
            "Analyze key drivers of customer churn and recommend retention strategies.",
            height=100
        )
        
        st.markdown("---")
        
        # The trigger button
        if st.button("🚀 Run Full Analysis Pipeline", type="primary"):
            st.session_state.pipeline_context["user_prompt"] = user_prompt
            
            with st.spinner("Executing agents and generating report..."):
                # Call the pipeline function and capture the updated memory!
                updated_context = run_full_pipeline(st.session_state.pipeline_context)
                
                # Store the final results in session state for display
                st.session_state.pipeline_context = updated_context
                st.session_state.report_content = updated_context.get("final_report_content")
                st.session_state.report_status = updated_context.get("final_report_status")

    # --- Main Display Area ---
    
    if st.session_state.report_content:
        st.header("2. Final Analysis Report")
        
        if st.session_state.report_status == "SUCCESS":
            # Display the final report in Markdown format
            st.markdown(st.session_state.report_content)
        else:
            st.error(f"Report Generation Failed: {st.session_state.report_status}")
            st.code(st.session_state.report_content)

        st.markdown("---")
        st.header("3. Pipeline Memory (Context)")
        
        # Show the full memory bank for debugging/transparency
        st.subheader("Full Context Dump")
        st.json(st.session_state.pipeline_context)

    else:
        st.info("Ready to start analysis. Upload your data and click 'Run Full Analysis Pipeline' in the sidebar.")

if __name__ == "__main__":
    main()