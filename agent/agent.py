from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
import sqlite3
import pandas as pd
import re
# -------- Tools --------

@tool
def sql_query_tool(query: str) -> str:
    """Run a SQL query on the asset_usage table.

    IMPORTANT:
    - Abnormal assets are those where status = 'abnormal'
    - Use this condition when asked about abnormal usage.

    Table schema:
    asset_usage(asset_id TEXT, date TEXT, energy_kwh REAL, status TEXT)
    """
    conn = sqlite3.connect("data/assets.db")
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()

        # If agent writes wrong SQL, help it
        if not rows and "abnormal" in query.lower():
            cur.execute("SELECT * FROM asset_usage WHERE status='abnormal'")
            rows = cur.fetchall()

        return str(rows)
    except Exception as e:
        return f"SQL ERROR: {e}"
    finally:
        conn.close()




@tool
def pandas_analysis_tool() -> str:
    """
    Analyze energy trends for assets from asset_usage table.
    Input can be string, list, or dict. Tool handles all cases.
    """
    import re

    # Convert whatever comes into a string
    text = str(input)

    # Extract asset IDs like A1, A2, A3
    asset_ids = re.findall(r"A\d+", text)

    conn = sqlite3.connect("data/assets.db")
    df = pd.read_sql_query("SELECT * FROM asset_usage", conn)
    conn.close()

    if asset_ids:
        df = df[df["asset_id"].isin(asset_ids)]

    summary = df.groupby("asset_id")["energy_kwh"].mean()
    return summary.to_string()



# -------- Chat LLM (important change) --------
llm = ChatOllama(
    model="qwen2.5:3b-instruct",
    system="""
You are a data analyst agent.

You MUST use tools to answer questions.

If the user asks about assets, energy usage, trends, or abnormalities:
- FIRST use the SQL tool to fetch data from the asset_usage table.
- THEN use the pandas analysis tool to analyze the data.
- NEVER ask the user for data.
- ALWAYS retrieve data using tools.

Table schema:
asset_usage(asset_id TEXT, date TEXT, energy_kwh REAL, status TEXT)
"""
)

tools = [sql_query_tool, pandas_analysis_tool]

# -------- Agent --------


agent = create_react_agent(llm, tools,debug=True)


def ask_agent(question: str):
    for step in agent.stream({"messages": [("user", question)]}):
        print(step)   # this prints Thought / Action / Observation
    response = agent.invoke({"messages": [("user", question)]})
    return response["messages"][-1].content
