from app.modules.health.service import HealthService


def main():
    service = HealthService()

    daily_logs = service.get_daily_logs()

    print(f"Found {len(daily_logs)} daily logs.\n")

    if daily_logs:
        print(daily_logs[0])


if __name__ == "__main__":
    main()