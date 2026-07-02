from functions.db_utils import query_database

class SentinelGateway:
    @staticmethod
    def get_system_logs():
        return query_database("SELECT * FROM logs LIMIT 10;")

    @staticmethod
    def query_database(nl_query: str):
        # This will be refined once the Data Intelligence Agent is ready
        return query_database(nl_query)