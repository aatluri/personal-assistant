from app.modules.health.repository import HealthRepository
from app.modules.health.schemas import DailyLog


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