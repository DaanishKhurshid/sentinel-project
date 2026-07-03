from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from gateway.server import SentinelGateway
from agents.crew import SentinelAgents
from crewai import Crew, Task, Process

# State definition
class SentinelState(TypedDict):
    raw_logs: Optional[List[dict]]
    anomaly_analysis: Optional[str]
    root_cause: Optional[str]
    remediation_plan: Optional[str]
    is_resolved: bool

# Nodes
def fetch_logs_node(state: SentinelState):
    print("--- Fetching logs ---")
    return {"raw_logs": SentinelGateway.get_system_logs()}

def monitor_node(state: SentinelState):
    print("--- Running Monitor Agent ---")
    
    # Get your agent from crew.py
    monitor_agent = SentinelAgents.monitor_agent()
    
    # Define the task
    task = Task(
        description=f"Analyze these logs for errors: {state['raw_logs']}",
        expected_output="A summary of errors detected.",
        agent=monitor_agent
    )
    
    # Create the Crew
    monitor_crew = Crew(
        agents=[monitor_agent],
        tasks=[task],
        process=Process.sequential
    )
    
    # Run the Crew
    result = monitor_crew.kickoff()
    return {"anomaly_analysis": str(result)}

# Graph setup
workflow = StateGraph(SentinelState)
workflow.add_node("fetch_logs", fetch_logs_node)
workflow.add_node("monitor", monitor_node)

workflow.set_entry_point("fetch_logs")
workflow.add_edge("fetch_logs", "monitor")
workflow.add_edge("monitor", END)

app = workflow.compile()

if __name__ == "__main__":
    final_state = app.invoke({})
    print("--- Final Analysis ---")
    print(final_state.get("anomaly_analysis"))