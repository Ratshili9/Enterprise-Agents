import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from config import DATA_FILE, REPORT_DIR, FINAL_REPORT_FILE
from agents.data_profiler_agent import DataProfilerAgent
from agents.data_cleaner_agent import DataCleanerAgent
from agents.internal_insights_agent import InternalInsightsAgent
from agents.external_context_agent import ExternalContextAgent
from agents.visualization_agent import VisualizationAgent
from agents.report_writer_agent import ReportWriterAgent
import agents.llm_client # Ensure LLM is configured

def setup_environment():
    """Create necessary directories and clean up old reports."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    if os.path.exists(FINAL_REPORT_FILE):
        os.remove(FINAL_REPORT_FILE)
    if os.path.exists(os.path.join(REPORT_DIR, 'plots')):
        shutil.rmtree(os.path.join(REPORT_DIR, 'plots'))
    print(f"--- Environment Setup Complete: {REPORT_DIR} prepared. ---")

def run_agent_wrapper(agent_class, context):
    """Wrapper function to run an agent instance."""
    return agent_class().run(context)

def main():
    if agents.llm_client.LLM_MODEL is None:
        print("Pipeline aborted: LLM configuration failed.")
        return
        
    setup_environment()
    
    # Session Memory
    context = {}
    
    # --- 1. Sequential Phase ---
    # Agent 1: Data Profiler
    if not DataProfilerAgent().run(context, DATA_FILE):
        return
        
    # Agent 2: Data Cleaner
    if not DataCleanerAgent().run(context):
        return
        
    # --- 2. Parallel Phase (Fan-out) ---
    print("\n\n=== 3. PARALLEL EXECUTION: Running Insights, Search, and Viz concurrently ===")
    
    parallel_agents = [
        InternalInsightsAgent, 
        ExternalContextAgent, 
        VisualizationAgent
    ]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit each agent to the executor. Each agent receives the *same* context dictionary reference.
        futures = [executor.submit(run_agent_wrapper, agent, context) for agent in parallel_agents]
        
        # Wait for all parallel tasks to complete
        results = [f.result() for f in futures]
        
        if not all(results):
            print("\nPipeline stopped: One or more parallel agents failed.")
            return

    # --- 3. Sequential Phase (Fan-in) ---
    # Agent 4: Report Writer
    if not ReportWriterAgent().run(context):
        return

    # --- Final Output ---
    print("\n\n--- ✅ Enterprise Data Analysis Pipeline Finished ---")
    print(f"Final Report saved to: {FINAL_REPORT_FILE}")
    print("\n--- Summary of State (Session Memory) ---")
    print(f"Total keys in context: {len(context)}")
    print(f"Internal Insights generated? {'key_insights' in context}")
    print(f"External Context acquired? {'external_context' in context}")
    print(f"Plots created: {len(context.get('plot_paths', []))}")


if __name__ == "__main__":
    main()