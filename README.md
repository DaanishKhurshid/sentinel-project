# sentinel-project
graph TD
    A([Start]) --> B[Fetch Logs]
    B --> C[Monitor Agent]
    C --> D[Diagnostician Agent]
    D --> E[Remediation Agent]
    E --> F{Verify}
    F -- Pass --> G([End])
    F -- Fail --> D
    
    %% Style adjustments
    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#ccf,stroke:#333,stroke-width:2px

    Sentinel: Autonomous System Health Guardian
Sentinel is an intelligent monitoring system designed for cloud-native platforms. It autonomously investigates system anomalies in real-time and provides a Data Intelligence Interface for infrastructure health queries.

Overview
Sentinel utilizes a multi-agent architecture built with CrewAI and LangGraph to provide self-healing capabilities for system infrastructure. It monitors logs, diagnoses root causes, proposes remediation, and performs verification in a circular, automated loop.

Key Features
Autonomous Workflow: A self-healing LangGraph loop that manages monitoring, diagnosis, and remediation.

Multi-Agent System: Specialized agents for monitoring, diagnostics, remediation, and data intelligence.

MCP-Style Gateway: A centralized interface (SentinelGateway) for all system interactions.

Safety Guardrails: Automated risk-filtering to prevent critical commands (e.g., system reboots) during operation.

Observability: Integration with LangSmith for full lifecycle tracing and auditing.

Project Structure
gateway/server.py: MCP-style gateway for system access.

functions/db_utils.py: Database connection and SQL execution interface.

crew.py: Definition of specialized AI agents.

orchestrator.py: Main LangGraph workflow orchestrator.

verify_setup.py: Utility script for testing system connectivity.

Setup and Installation
Clone the repository:

Bash
git clone <repository-url>
Set up a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure your environment variables in a .env file:

GEMINI_API_KEY

LANGSMITH_API_KEY

Usage
To start the Sentinel workflow, run the orchestrator script:

Bash
python orchestrator.py
This will initialize the agents, fetch system logs, and enter the autonomous monitoring loop.

License
This project is intended for educational purposes as part of the AI Bootcamp.