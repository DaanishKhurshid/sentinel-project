from crewai import Agent

class SentinelAgents:
    @staticmethod
    def monitor_agent():
        return Agent(
            role='Monitor Agent',
            goal='Parse logs and telemetry to detect anomalies.',
            backstory='You are a vigilant system observer.',
            verbose=True
        )

    @staticmethod
    def diagnostician_agent():
        return Agent(
            role='Diagnostician Agent',
            goal='Determine the root cause of anomalies using the knowledge base.',
            backstory='You are an expert systems engineer.',
            verbose=True
        )

    @staticmethod
    def remediation_agent():
        return Agent(
            role='Remediation Agent',
            goal='Execute corrective actions while respecting safety constraints.',
            backstory='You are a cautious operator.',
            verbose=True
        )

    @staticmethod
    def data_intelligence_agent():
        return Agent(
            role='Data Intelligence Agent',
            goal='Translate natural language to SQL to retrieve health data.',
            backstory='You are a database specialist.',
            verbose=True
        )