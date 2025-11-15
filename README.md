# Enterprise Data Analyst Multi-Agent System (EDAMAS)
A multi-agent system that automatically profiles, cleans, analyzes, visualizes, and reports on any business dataset in seconds.

# Problem Statement

Businesses generate large volumes of data every day—sales, customers, operations, finance, and more. But most teams lack the time, technical skill, or tools to properly analyze this information. As a result, many decisions are made without evidence, insights are missed, and opportunities are lost.

Traditional data analysis requires:

cleaning messy data

profiling columns

finding patterns

creating charts

building reports

and sometimes training models

This takes hours or days for a human analyst.

My project solves this by building an autonomous, multi-agent data analyst system that does all this automatically from a single user request.

# Why Agents?

Traditional scripts or notebooks can't communicate, delegate tasks, or reason about complex workflows.

Agents are perfect for this because:

They can divide the problem into multiple specialized roles

They reason about data quality, missing values, and insights

They can call tools like Python code execution or chart generation

They maintain memory about the dataset across the entire session

They support long-running operations, ideal for modeling and reporting

They create explainable steps, which is important for business adoption

A multi-agent system behaves like a virtual data team:
one agent cleans the data, another analyzes it, another writes the report.

This produces better insights, faster, and more reliably than a single agent or a static script.


# Enterprise Data Analysis Agent Pipeline
This project showcases a powerful multi-agent system designed for end-to-end data analysis. It automates data preparation, external market research, internal insight generation, visualization, and professional report writing using a combination of sequential and parallel processing.

# Architecture & Agent Roles
The pipeline executes in four distinct phases, ensuring data quality is established before parallel processing begins.

Phase	               |  Agent Name	          | Core Functionality
1. Sequential\n Setup	 | Data Profiler Agent	| Reads raw CSV, generates a statistical data profile, and validates initial quality.
   
3. Sequential Setup	| Data Cleaner Agent	| Handles nulls (NaN), removes duplicates, and enforces correct data types (e.g., Price, Quantity) for downstream calculations.
   
3A. Parallel Execution |	Internal Insights Agent |	Analyzes the cleaned data profile and historical context from the memory bank to generate LLM-powered business insights.

3B. Parallel Execution |	External Context Agent | Performs a targeted Google Search to acquire current market trends relevant to the data (e.g., Electronics, Food industries).

3C. Parallel Execution |	Visualization Agent	| Generates key business charts (sales_trend.png, top_products.png) using Matplotlib, with robust logic for finding sales and date columns.

5. Sequential Report |	Report Writer Agent |	Consolidates ALL outputs (plots, insights, context) and uses the LLM to write a comprehensive, final analysis report.

# ⚙️ Setup & Execution

## 1. PrerequisitesPython 3.9+ installed.
## 2. Git installed (for cloning and pushing).
## 3. A Gemini API Key is required for the LLM agents.

# 2. Environment Setup

Clone the repository and install the required libraries within a virtual environment (venv is recommended)

:Bash# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd Enterprise-Agents

#  Create and activate the virtual environment

python -m venv venv
.\venv\Scripts\activate# Use 'source venv/bin/activate' on Linux/macOS

#  Install dependencies
pip install -r requirements.txt

# 3. Configuration & DataEnsure 
### your necessary files and folders exist:

File/Folder | 	Path	  |  Purpose	|  Initialization		

Data File   | 	data/sales_data.csv |	Input data for analysis.	| Must be manually populated.		

Output Folder	| reports/	| Main output directory.	| Created by initial setup.		

Plot Folder | 	reports/plots/	| Directory for charts.	| Created automatically by the Visualization Agent.		

Memory Bank |	reports/memory_bank.json |	Stores historical insights.	| Must be initialized with {"past_insights": []}.		

# 4. API Key
## Set your Gemini API key as an environment variable in your terminal session. This must be done every time you open a new terminal.

Bash# For PowerShell (Windows)
$env:GEMINI_API_KEY="AIzaSy...YOUR...KEY...HERE"

# Running the Pipeline
Execute the code using the single command below. The terminal output will trace the progress of the sequential and parallel agents.
The Execution Command Bash#  python run_pipeline.py
 
# Expected Output Flow
A successful run confirms that all phases have been completed, culminating in the final markdown report
....
=== 3C. PARALLEL: Visualization Agent Running ===

--- [TOOL:Viz] Plotting sales over time to reports\plots\sales_trend.png ---

Calculated TotalSale using Price * Quantity.

--- [TOOL:Viz] Plotting top products to reports\plots\top_products.png ---

Visualization Agent Finished.
...
=== 4. SEQUENTIAL: Report Writer Agent Running ===
Report Writer Agent Finished. Report saved to reports\final_analysis_report.md

--- ✅ Enterprise Data Analysis Pipeline Finished ---

### Final Report saved to: reports\final_analysis_report.md

### Check the reports/ directory for your final analysis report and generated plots!
