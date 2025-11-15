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

# What I Created (Architecture Overview)

My system is called EDAMAS — Enterprise Data Analyst Multi-Agent System.

It contains five main agents, each with a specialized role:

## 1. Data Profiler Agent

Reads the dataset

Detects column types

Generates summary statistics

Identifies missing values and anomalies

##2. Data Cleaner Agent

Fixes missing or inconsistent values

Handles duplicates

Normalizes column formats

Produces a cleaned dataset

## 3. Insights Agent

Detects correlations

Finds trends or seasonality

Generates natural-language insights

Identifies outliers and patterns

## 4. Visualization Agent

Creates charts automatically (bar charts, line charts, histograms, correlation heatmaps)

Returns them to the user

Uses Python execution tools for rendering

## 5. Report Writer Agent

Combines all insights

Generates a structured business report

Creates recommendations for decision-makers

# Message Flow

User uploads a CSV and asks a question.

Data Profiler Agent analyzes structure.

Data Cleaner Agent prepares dataset.

Insights Agent performs reasoning.

Visualization Agent creates graphs.

Report Agent summarizes everything into a polished business PDF-style output.

Agents communicate using the built-in A2A multi-agent protocol.

# Tools Used

I built custom tools for:

loading CSV files

data profiling

cleaning functions

chart generation

basic machine-learning modeling

Plus ADK built-in tools:

code execution

memory

Google search (optional)

long-running operation pause/approval

# Memory

I used:

InMemorySessionService for agent state

Memory Bank to store dataset metadata across the entire workflow
(column types, cleaning actions, discovered insights, etc.)

This makes the system feel consistent and "intelligent" across multiple requests.

# Observability

I implemented:

structured logging for each agent

run-time metrics (rows, columns, missing counts, charts generated)

trace identifiers for delegations

clear output structure for debugging

This makes the project production-ready.

# Demo

The demo video shows:

User uploads sales.csv

Profiler Agent summarizes the dataset

Cleaner Agent fixes missing values

Insights Agent discovers:

top-selling categories

monthly revenue patterns

customer retention segments

Visualization Agent generates:

revenue over time chart

product category distribution

correlation heatmap

Report Agent outputs a final business report including recommendations

All of this happens automatically in a single multi-agent flow.

# The Build
Technologies Used

Python 3.10

Google Agents Developer Kit (ADK)

Gemini 2.0 Flash & Pro

Pandas / NumPy

Matplotlib

Streamlit (for optional UI)

# Engineering Decisions

I used multiple specialized agents instead of one general agent to improve reliability and structure.

I avoided overly complex ML models to ensure determinism and stability.

I built custom data tools instead of relying only on LLM reasoning.

I added well-documented folder structure and diagrams.

# System Strengths

Works on any CSV file

Produces insights in seconds

Fully autonomous

Easy to extend with new agents

Easy to deploy

High reliability due to agent specialization
