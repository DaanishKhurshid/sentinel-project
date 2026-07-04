from mcp.server.fastmcp import FastMCP
from functions.db_utils import query_database

mcp = FastMCP("Sentinel-Gateway")

@mcp.tool()
def get_system_logs():
    """Retrieve the last 10 system logs."""
    return query_database("SELECT * FROM logs LIMIT 10;")

@mcp.tool()
def execute_system_command(command: str):
    """Execute a system command (Read-only/Simulated)."""
    # Safety Check Guardrail
    if command in ["system_reboot", "format_disk"]:
        return "PERMISSION DENIED: High-risk command blocked."
    return f"Simulated execution of: {command}"

@mcp.tool()
def query_database(query: str):
    """Query the infrastructure database."""
    return query_database(query)

if __name__ == "__main__":
    mcp.run()