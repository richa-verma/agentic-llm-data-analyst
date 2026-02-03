from fastapi import FastAPI
from agent.agent import ask_agent

app = FastAPI()

@app.post("/ask")
def ask(q: dict):
    return {"answer": ask_agent(q["question"])}
