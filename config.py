import os

# --- General Configuration ---
# Use environment variable for security
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = 'gemini-2.5-flash'

# --- File Paths ---
DATA_FILE = 'data/sales_data.csv'
REPORT_DIR = 'reports'
MEMORY_FILE = os.path.join(REPORT_DIR, 'memory_bank.json')
FINAL_REPORT_FILE = os.path.join(REPORT_DIR, 'final_analysis_report.md')
PLOTS_DIR = os.path.join(REPORT_DIR, 'plots')