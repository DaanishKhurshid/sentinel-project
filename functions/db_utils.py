# This handles the database connection safely
import sqlite3

def query_database(query: str):
    """Executes a SQL query on the system_telemetry database."""
    db_path = 'system_telemetry.db'
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return f"Error executing query: {str(e)}"