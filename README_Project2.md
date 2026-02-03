
# Agentic LLM Data Analyst using LangChain, LangGraph, Ollama, SQL and Pandas

This project demonstrates a true **Agentic AI system** where a Large Language Model autonomously:

- Plans which tools to use
- Executes SQL queries over structured data
- Performs analytical processing using Pandas
- Synthesizes a final answer using tool outputs

The system is built using LangChain + LangGraph with a local LLM served by Ollama.

Example question:
“Find assets with abnormal energy usage and analyze trends”

---

## How the Agent Works

User Question
      ↓
LLM plans tool usage
      ↓
SQL Tool executes
      ↓
LLM reasons over SQL result
      ↓
Pandas Tool executes
      ↓
LLM synthesizes final analytical answer

You can see this full trace live in the terminal logs.

---

## Tech Stack

LLM: Ollama (qwen2.5:3b-instruct)  
Agent Framework: LangChain + LangGraph  
Structured Data: SQLite  
Data Analysis: Pandas  
API: FastAPI  
Language: Python

---

## Project Structure

agentic-llm-data-analyst/
├── data/assets.db
├── agent/agent.py
├── api/app.py

---

## Running the Project

1. Activate conda environment

conda activate rag_env

2. Start Ollama

ollama run qwen2.5:3b-instruct

3. Run API

uvicorn api.app:app --reload

4. Ask a question

curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"Find assets with abnormal energy usage and analyze trends\"}"

---

## What You Will See

You will see:

Thought → SQL Tool  
Observation → SQL results  
Thought → Pandas Tool  
Observation → Trend analysis  
Final Answer

This is real Agentic AI behavior.

---

Author: Richa Verma
