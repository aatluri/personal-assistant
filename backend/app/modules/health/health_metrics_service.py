from datetime import date

from app.modules.health.health_metrics_repository import (
    HealthMetricsRepository,
)
from app.modules.health.schemas import HealthMetrics


class HealthMetricsService:
    """
    Service layer for Health Metrics.

    The service acts as the bridge between the repository and the
    rest of the application.

    Responsibilities:
    - Implement Health Metrics business logic.
    - Coordinate repository operations.
    - Perform calculations and validations when required.
    - Return HealthMetrics models to callers.

    The service should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the HealthMetricsService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = HealthMetricsRepository()


    # -------------------------------------------------------------------------
    # Health Metrics
    #
    # Business operations for Health Metrics.
    # -------------------------------------------------------------------------

    def get_health_metrics(self) -> list[HealthMetrics]:
        """
        Retrieve all Health Metrics.
        """
        return self._repository.get_health_metrics()


    def get_health_metric(
        self,
        metric_date: date,
    ) -> HealthMetrics | None:
        """
        Return the Health Metrics for the specified date.

        If no record exists, return None.
        """
        return self._repository.get_health_metric(metric_date)


    def create_health_metric(
        self,
        health_metric: HealthMetrics,
    ) -> None:
        """
        Create a new Health Metrics record.
        """
        self._repository.create_health_metric(health_metric)


    def upsert_health_metric(
        self,
        metric_date: date,
        health_metric: HealthMetrics,
    ) -> None:
        """
        Update the Health Metrics if it already exists.

        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_health_metric(
            metric_date,
            health_metric,
        )

        if not updated:
            self._repository.create_health_metric(
                health_metric,
            )