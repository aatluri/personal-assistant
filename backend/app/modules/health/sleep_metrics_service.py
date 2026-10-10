from datetime import date

from app.modules.health.sleep_metrics_repository import (
    SleepMetricsRepository,
)
from app.modules.health.schemas import SleepMetrics


class SleepMetricsService:
    """
    Service layer for Sleep Metrics.

    The service acts as the bridge between the repository and the
    rest of the application.

    Responsibilities:
    - Implement Sleep Metrics business logic.
    - Coordinate repository operations.
    - Perform calculations and validations when required.
    - Return SleepMetrics models to callers.

    The service should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the SleepMetricsService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = SleepMetricsRepository()


    # -------------------------------------------------------------------------
    # Sleep Metrics
    #
    # Business operations for Sleep Metrics.
    # -------------------------------------------------------------------------

    def get_sleep_metrics(self) -> list[SleepMetrics]:
        """
        Retrieve all Sleep Metrics.
        """
        return self._repository.get_sleep_metrics()


    def get_sleep_metric(
        self,
        metric_date: date,
    ) -> SleepMetrics | None:
        """
        Return the Sleep Metrics for the specified date.

        If no record exists, return None.
        """
        return self._repository.get_sleep_metric(metric_date)


    def create_sleep_metric(
        self,
        sleep_metric: SleepMetrics,
    ) -> None:
        """
        Create a new Sleep Metrics record.
        """
        self._repository.create_sleep_metric(sleep_metric)


    def upsert_sleep_metric(
        self,
        metric_date: date,
        sleep_metric: SleepMetrics,
    ) -> None:
        """
        Update the Sleep Metrics if it already exists.

        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_sleep_metric(
            metric_date,
            sleep_metric,
        )

        if not updated:
            self._repository.create_sleep_metric(
                sleep_metric,
            )