

import os
from typing import TypedDict, List, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from gateway.server import SentinelGateway

# 1. Setup
load_dotenv()
MODE = 'AI' 

# 2. Configuration & AI Initialization
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "sentinel-project"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    system_instruction="""You are a Sentinel monitoring system agent. 
    Your ONLY task is to analyze system logs, diagnose root causes, and suggest remediation steps. 
    If a query is outside this scope, respond: 'I am sorry, that request is outside my operational scope.'"""
)

# 3. State
class SentinelState(TypedDict):
    raw_logs: Optional[List[dict]]
    anomaly_analysis: Optional[str]
    root_cause: Optional[str]
    remediation_plan: Optional[str]
    is_resolved: bool

# 4. Nodes
def fetch_logs_node(state: SentinelState):
    print("--- Fetching logs ---")
    return {"raw_logs": SentinelGateway.get_system_logs()}

def monitor_node(state: SentinelState):
    print("--- Running Monitor Node ---")
    logs = state.get("raw_logs", "No logs")
    if MODE == 'AI':
        response = llm.invoke(f"Analyze these logs for anomalies: {logs}")
        return {"anomaly_analysis": response.content}
    return {"anomaly_analysis": "MOCK: Anomaly detected in Auth-Service."}

def diagnostician_node(state: SentinelState):
    print("--- Running Diagnostician Node ---")
    analysis = state.get("anomaly_analysis", "No analysis")
    if MODE == 'AI':
        try:
            response = llm.invoke(f"Based on this analysis: {analysis}, what is the root cause?")
            return {"root_cause": response.content}
        except Exception:
            return {"root_cause": "Diagnostic service unavailable."}
    return {"root_cause": "MOCK: Database connection timeout."}

def remediation_node(state: SentinelState):
    print("\n--- Running Remediation Node ---")
    plan = "Restarting Auth-Service" if MODE == 'AI' else "MOCK: Restarting Auth-Service."
    print(f"Proposed Plan: {plan}")
    
    approval = input("Do you approve this remediation plan? (yes/no): ")
    if approval.lower() == "yes":
        return {"remediation_plan": plan, "is_resolved": True}
    return {"remediation_plan": "REJECTED BY USER", "is_resolved": False}

# 5. Graph Assembly
memory = MemorySaver()
workflow = StateGraph(SentinelState)

workflow.add_node("fetch_logs", fetch_logs_node)
workflow.add_node("monitor", monitor_node)
workflow.add_node("diagnostician", diagnostician_node)
workflow.add_node("remediation", remediation_node)

workflow.set_entry_point("fetch_logs")
workflow.add_edge("fetch_logs", "monitor")
workflow.add_edge("monitor", "diagnostician")
workflow.add_edge("diagnostician", "remediation")
workflow.add_edge("remediation", END)

app = workflow.compile(checkpointer=memory)

# 6. Runner
if __name__ == "__main__":
    print("--- Starting Sentinel Workflow ---")
    config = {"configurable": {"thread_id": "sentinel-run-1"}}
    final_state = app.invoke({}, config=config)
    
    print("\n--- Final Workflow Results ---")
    print(f"Analysis: {final_state.get('anomaly_analysis')}")
    print(f"Root Cause: {final_state.get('root_cause')}")
    print(f"Status: {'SUCCESS' if final_state.get('is_resolved') else 'FAILED/REJECTED'}")