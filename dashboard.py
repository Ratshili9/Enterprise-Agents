import streamlit as st
import os
import subprocess
import pandas as pd
import glob
import time

# --- Configuration ---
FINAL_REPORT_PATH = "reports/final_analysis_report.md"
PLOTS_DIR = "reports/plots"

st.set_page_config(layout="wide", page_title="Enterprise AI Data Pipeline")

def run_pipeline(uploaded_file_path):
    """
    Executes the main pipeline script as a subprocess and captures the output.
    """
    # 1. Clear old reports and plots before running
    if os.path.exists(FINAL_REPORT_PATH):
        os.remove(FINAL_REPORT_PATH)
    if os.path.exists(PLOTS_DIR):
        for f in glob.glob(os.path.join(PLOTS_DIR, '*')):
            os.remove(f)

    # 2. Command to execute the main pipeline script
    command = ["python", "run_pipeline.py", "--file", uploaded_file_path]
    
    # 3. Use st.empty() to stream output to the dashboard
    output_container = st.empty()
    output_text = ""
    
    # 4. CRITICAL FIX: Set environment variable to force UTF-8 encoding for the child process
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8' # <-- This is the key change!
    
    try:
        # We pass the encoding and the environment variables to ensure compatibility
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # Capture errors along with stdout
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding='utf-8', 
            env=env # <--- Pass the modified environment
        )

        for line in process.stdout: 
            output_text += line
            # Stream the output line-by-line to the dashboard
            output_container.code(output_text, language="bash")
            time.sleep(0.01) # Small delay for better streaming effect

        process.wait()
        
        if process.returncode == 0:
            st.success("✅ Pipeline Finished Successfully!")
            return True
        else:
            st.error(f"❌ Pipeline failed with return code {process.returncode}. Check logs above.")
            return False

    except FileNotFoundError:
        st.error("❌ Error: 'run_pipeline.py' not found. Ensure it is in the same directory.")
        return False
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        return False

def display_results():
    """Displays the final report and plots."""
    if os.path.exists(FINAL_REPORT_PATH):
        st.markdown("---")
        st.header("📝 Final Analysis Report")
        
        with open(FINAL_REPORT_PATH, 'r', encoding='utf-8') as f:
            report_content = f.read()
        st.markdown(report_content)
        
    st.markdown("---")
    st.header("📊 Generated Visualizations")
    
    plot_files = glob.glob(os.path.join(PLOTS_DIR, '*.png'))
    if plot_files:
        # Create two columns, so plots look better on wide screens
        cols = st.columns(2) 
        
        for i, plot_path in enumerate(plot_files):
            col = cols[i % 2] # Cycle between the two columns
            with col:
                plot_name = os.path.basename(plot_path).replace('_', ' ').title()
                st.subheader(plot_name)
                st.image(plot_path)
    else:
        st.info("No plots were generated. Check pipeline logs for warnings (e.g., missing numeric columns).")


# ======================================================
# Main Dashboard UI
# ======================================================
def app():
    st.title("Enterprise AI Pipeline: Data Analysis Engine")
    st.subheader("Automated data profiling, insights, ML prediction, and reporting.")
    
    uploaded_file = st.file_uploader(
        "Upload a CSV File to Analyze", 
        type=["csv"]
    )
    
    # Placeholder for saving the uploaded file locally
    local_path = None

    if uploaded_file is not None:
        # Save the uploaded file temporarily to the 'data' directory for the pipeline to read
        os.makedirs("data", exist_ok=True)
        local_path = os.path.join("data", uploaded_file.name)
        
        with open(local_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' uploaded and ready for analysis.")
        
        if st.button("🚀 Start Analysis"):
            with st.spinner('Running AI Pipeline... (This may take 30-60 seconds)'):
                success = run_pipeline(local_path)
                
            if success:
                display_results()

    # NOTE: The block that re-ran the results on every app refresh has been removed here.

if __name__ == '__main__':
    # Ensure necessary folders exist at startup
    os.makedirs("data", exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)
    app()