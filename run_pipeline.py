import argparse
import os
from concurrent.futures import ThreadPoolExecutor

# === Agents ===
from agents.data_profiler_agent import DataProfilerAgent
from agents.data_cleaner_agent import DataCleanerAgent
# Corrected Agent Imports for Parallel Execution
from agents.internal_insights_agent import InternalInsightsAgent
from agents.external_context_agent import ExternalContextAgent
from agents.visualization_agent import VisualizationAgent
from agents.ml_agent import MLAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_writer_agent import ReportWriterAgent


# ======================================================
# 1. CLI ARGUMENT PARSER
# ======================================================
def parse_args():
    parser = argparse.ArgumentParser(description="Enterprise AI Pipeline")
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to input CSV file"
    )
    return parser.parse_args()


# ======================================================
# 2. ENVIRONMENT SETUP
# ======================================================
def setup_environment():
    # Ensure all new and old report folders exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/plots", exist_ok=True)
    os.makedirs("reports/ml", exist_ok=True)  # New ML output folder

    memory_path = "reports/memory_bank.json"

    if not os.path.exists(memory_path):
        # Initialize memory bank if missing
        with open(memory_path, "w") as f:
            f.write('{"past_insights": []}')

    # Clear old report files before a new run
    if os.path.exists("reports/final_analysis_report.md"):
        os.remove("reports/final_analysis_report.md")

    print("--- Environment Setup Complete: reports prepared. ---")


# ======================================================
# 3. RUN WRAPPER FOR PARALLEL AGENTS
# ======================================================
def run_agent_wrapper(agent_class, context):
    try:
        # Run agent instance and return success status
        return agent_class().run(context)
    except Exception as e:
        print(f"Error in {agent_class.__name__}: {str(e)}")
        # Return False or None to indicate failure
        return False


# ======================================================
# 4. MAIN PIPELINE
# ======================================================
def main():
    # Placeholder for LLM Client Configuration (assuming it's here in the full file)
    # print("--- LLM Client configured successfully ---")

    args = parse_args()
    csv_path = args.file

    setup_environment()

    # Shared session state
    context = {
        "data_path": csv_path,
        # Initialize other context variables if needed, e.g., 'ml_reports': {}
    }

    # ==================================================
    # Step 1 — Sequential: Profiler Agent
    # ==================================================
    print("\n=== 1. SEQUENTIAL: Data Profiler Agent Running ===")
    if not DataProfilerAgent().run(context):
        print("Profiler Agent failed. Aborting.")
        return
    print("Profiler Agent Finished.")

    # ==================================================
    # Step 2 — Sequential: Data Cleaner Agent
    # ==================================================
    print("\n=== 2. SEQUENTIAL: Data Cleaner Agent Running ===")
    if not DataCleanerAgent().run(context):
        print("Data Cleaner Agent failed. Aborting.")
        return
    print("Cleaner Agent Finished.")

    # ==================================================
    # Step 3 — Parallel: Insights, Search, Visualization
    # ==================================================
    print("\n\n=== 3. PARALLEL EXECUTION: Insights / Search / Viz ===")

    parallel_agents = [
        InternalInsightsAgent,  # Renamed from InsightsAgent
        ExternalContextAgent,  # Renamed from SearchAgent
        VisualizationAgent
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(run_agent_wrapper, agent, context)
            for agent in parallel_agents
        ]
        results = [f.result() for f in futures]  # Wait for all results

    if all(results):
        print("Parallel Agents Finished.")
    else:
        print("Warning: One or more parallel agents failed.")

    # ==================================================
    # Step 4 — ML Agent (Sequential)
    # ==================================================
    print("\n=== 4. SEQUENTIAL: ML Agent Running ===")
    ml_agent = MLAgent()
    if not ml_agent.run(context):
        print("ML Agent failed. Aborting recommendations.")
    else:
        print("ML Agent Finished.")

        # ==================================================
        # Step 5 — Recommendation Agent (Sequential)
        # ==================================================
        print("\n=== 5. SEQUENTIAL: Recommendation Agent Running ===")
        rc_agent = RecommendationAgent()
        if not rc_agent.run(context):
            print("Recommendation Agent failed.")
        else:
            print("Recommendation Agent Finished.")

    # ==================================================
    # Step 6 — Report Writer
    # ==================================================
    print("\n=== 6. Report Writer Agent Running ===")
    ReportWriterAgent().run(context)
    print("Report Writer Agent Finished.")
    print("\n--- ✅ Enterprise Data Analysis Pipeline Finished ---")
    print("Final Report saved to: reports/final_analysis_report.md")


if __name__ == "__main__":
    main()
