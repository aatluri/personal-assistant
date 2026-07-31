from app.modules.health.repository import HealthRepository
from app.modules.health.schemas import DailyLog
from datetime import date


class HealthService:
    """
    Service layer for the Health module.

    The service acts as the bridge between the repository and the
    rest of the application (API, AI Assistant, UI, etc.).

    Responsibilities:
    - Implement business logic.
    - Coordinate one or more repositories.
    - Perform calculations and validations.
    - Return domain models to callers.

    The service should not know how data is stored.
    It simply requests data from the repository.
    """

    def __init__(self):
        """
        Create an instance of the HealthRepository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = HealthRepository()

    def get_daily_logs(self) -> list[DailyLog]:
        """
        Retrieve all daily logs.

        Currently this simply delegates to the repository.

        In the future this method may:
        - Filter records
        - Sort records
        - Apply business rules
        - Perform calculations
        - Combine data from multiple repositories
        """

        return self._repository.get_daily_logs()

    def get_daily_log(self, log_date: date) -> DailyLog | None:
        """
        Return the Daily Log for the specified date.
        If no record exists, return None.
        """

        return self._repository.get_daily_log(log_date)

    def get_latest_daily_log(self) -> DailyLog | None:
        """
        Return the most recent Daily Log.
        """

        return self._repository.get_latest_daily_log()

    def create_daily_log(self, daily_log: DailyLog) -> None:
        """
        Create a new Daily Log.
        """

        self._repository.create_daily_log(daily_log)

    def update_daily_log(self,log_date: date,daily_log: DailyLog,) -> bool:
        """
        Update an existing Daily Log.

        Returns True if the log was updated, otherwise False.
        """

        return self._repository.update_daily_log(
            log_date,
            daily_log,
        )