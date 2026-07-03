from typing import TypedDict, List, Optional

class SentinelState(TypedDict):
    """The shared state for the Sentinel system."""
    raw_logs: Optional[List[dict]]
    anomaly_analysis: Optional[str]
    root_cause: Optional[str]
    remediation_plan: Optional[str]
    is_resolved: bool


from gateway.server import SentinelGateway

def fetch_logs_node(state: SentinelState):
    """Fetches logs from the gateway and updates the state."""
    print("--- Fetching logs from Gateway ---")
    logs = SentinelGateway.get_system_logs()
    return {"raw_logs": logs}

from langgraph.graph import StateGraph, END

# Initialize the graph with your state
workflow = StateGraph(SentinelState)

# Add your first node (the one we created)
workflow.add_node("fetch_logs", fetch_logs_node)

# Set the entry point
workflow.set_entry_point("fetch_logs")

# Connect the node to the end
workflow.add_edge("fetch_logs", END)

# Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    print("--- Running Graph ---")
    final_state = app.invoke({}) # We pass an empty dict to start
    print("Final State logs:", final_state.get("raw_logs"))