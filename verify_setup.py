from gateway.server import SentinelGateway

def run_test():
    try:
        logs = SentinelGateway.get_system_logs()
        print("Successfully retrieved logs:")
        print(logs)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_test()