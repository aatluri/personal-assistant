from app.modules.health.repository import HealthRepository

def main():
    repository = HealthRepository()
    daily_logs = repository.get_daily_logs()
    print(f"Found {len(daily_logs)} daily logs.\n")
    if daily_logs:
        print(daily_logs[0])

if __name__ == "__main__":
    main()