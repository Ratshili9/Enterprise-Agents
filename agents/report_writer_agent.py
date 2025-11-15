import os
from agents.llm_client import generate_text
from config import FINAL_REPORT_FILE

class ReportWriterAgent:
    def run(self, context: dict) -> bool:
        """Combines all artifacts into a final Markdown report."""
        print("\n=== 4. SEQUENTIAL: Report Writer Agent Running ===")
        try:
            profile = context['profile_report']
            insights = context['internal_insights']
            external_context = context['external_context']
            plot_paths = context['plot_paths']
        except KeyError as e:
            print(f"Report Writer Error: Missing key {e} in context.")
            return False

        # Create image links in Markdown
        image_md = ""
        for path in plot_paths:
            # We assume plots are in a folder relative to the final report location
            relative_path = os.path.basename(path)
            image_md += f"![Visualization]({relative_path})\n\n"
            
        prompt = f"""
        You are a senior analyst compiling the final, comprehensive business report. 
        Your task is to synthesize all three inputs (Internal Insights, External Context, and Visualizations) 
        into a single, polished, professional Markdown document.
        
        **Report Structure:**
        1. **Executive Summary** (1 paragraph synthesizing internal/external context)
        2. **Internal Data Profile** (The full profile)
        3. **Key Internal Insights** (The 3 bullet points)
        4. **External Market Context** (The search results for enrichment)
        5. **Visualizations** (The plot images)
        
        ---
        [DATA PROFILE]
        {profile}
        ---
        [INTERNAL INSIGHTS]
        {insights}
        ---
        [EXTERNAL CONTEXT]
        {external_context}
        ---
        [VISUALIZATIONS MARKDOWN]
        {image_md}
        ---
        
        Now, generate the final report in Markdown.
        """
        
        final_report = generate_text(prompt)
        
        # Save final artifact
        os.makedirs(os.path.dirname(FINAL_REPORT_FILE), exist_ok=True)
        with open(FINAL_REPORT_FILE, "w") as f:
            f.write(final_report)
            
        context['final_report'] = final_report
        print(f"Report Writer Agent Finished. Report saved to {FINAL_REPORT_FILE}")
        return True