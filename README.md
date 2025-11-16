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


# Enterprise Data Analysis Pipeline

## Project Overview

The Enterprise Data Analysis Pipeline is a modular, multi-agent system designed to automate complex data workflows. It performs end-to-end analysis on raw business data, covering profiling, cleaning, advanced machine learning, visualization, and final report synthesis using the Gemini API for comprehensive, actionable insights.

The architecture is built on a Sequential/Parallel execution model to maximize efficiency, ensuring that prerequisites (like data cleaning) are met before running concurrent analysis tasks (like visualization and internal insights).

## Key Features

Dynamic Profiling & Cleaning: Automatically loads data, handles missing values, and identifies data types and statistics.

Modular Agents: Specialized agents for distinct tasks (Profiling, Cleaning, Insights, ML, Viz, Reporting, Recommendations).

LLM-Powered Synthesis: Utilizes the Gemini 2.5 Flash model via the google-generativeai SDK to interpret complex data artifacts and synthesize a final strategic report.

ML Integration: Executes predictive modeling (ARIMA forecasting, Anomaly Detection) and saves results to dedicated reports.

Memory Bank: Stores key findings from previous runs, allowing the Internal Insights Agent to provide context and compare current data against historical trends.

Visualization: Generates diagnostic plots (Heatmaps, Categorical Comparisons) and saves them as PNG files.


# Setup and Dependencies

# This project requires Python and several data science and machine learning libraries.

## 1. Requirements

First, ensure you have the necessary libraries installed.

pip install -r requirements.txt
# If requirements.txt is not present, use:
# pip install pandas numpy scikit-learn statsmodels matplotlib seaborn google-genai


## 2. API Key Configuration

The pipeline relies on the Gemini API for the Insights and Report Writer agents.

Set Environment Variable: The recommended and most secure approach is to set the GEMINI_API_KEY as an environment variable in your shell or system:

export GEMINI_API_KEY="YOUR_API_KEY_HERE"


Configuration File: The config.py file reads this environment variable to configure the llm_client.py.

Execution

## 1. Define the Pipeline

The file run_pipeline.py defines the flow using a list of steps, specifying whether agents run SEQUENTIAL or PARALLEL.

The current execution flow is:

SEQUENTIAL: Data Profiler

SEQUENTIAL: Data Cleaner

PARALLEL: Internal Insights, External Context (Mock), Visualization

SEQUENTIAL: ML Agent (Forecasting & Anomaly Detection)

SEQUENTIAL: Recommendation Agent

SEQUENTIAL: Report Writer

## 2. Run the Analysis

Execute the main pipeline script from the root directory:

python run_pipeline.py


## 3. Review Results

All outputs are saved to the reports/ directory:

Final Report: reports/final_analysis_report.md

Visualizations: reports/plots/*.png

ML Outputs: reports/ml/*.csv

### Final Report saved to: reports\final_analysis_report.md

### Check the reports/ directory for your final analysis report and generated plots!
