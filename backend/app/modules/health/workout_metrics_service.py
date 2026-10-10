from datetime import date, datetime

from app.modules.health.workout_metrics_repository import (
    WorkoutMetricsRepository,
)
from app.modules.health.schemas import WorkoutMetrics


class WorkoutMetricsService:
    """
    Service layer for Workout Metrics.

    The service acts as the bridge between the repository and the
    rest of the application.

    Responsibilities:
    - Implement Workout Metrics business logic.
    - Coordinate repository operations.
    - Perform calculations and validations when required.
    - Return WorkoutMetrics models to callers.

    The service should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the WorkoutMetricsService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = WorkoutMetricsRepository()


    # -------------------------------------------------------------------------
    # Workout Metrics
    #
    # Business operations for Workout Metrics.
    # -------------------------------------------------------------------------

    def get_workout_metrics(self) -> list[WorkoutMetrics]:
        """
        Retrieve all Workout Metrics.
        """
        return self._repository.get_workout_metrics()


    def get_workout_metrics_by_date(self,workout_date: date,) -> list[WorkoutMetrics]:
        return self._repository.get_workout_metrics_by_date(
            workout_date
        )

    def get_workout_metric(
        self,
        workout_start_time: datetime,
    ) -> WorkoutMetrics | None:
        """
        Return the Workout Metrics for the specified Workout Start Time.

        If no record exists, return None.
        """
        return self._repository.get_workout_metric(
            workout_start_time
        )


    def create_workout_metric(
        self,
        workout_metric: WorkoutMetrics,
    ) -> None:
        """
        Create a new Workout Metrics record.
        """
        self._repository.create_workout_metric(
            workout_metric
        )


    def upsert_workout_metric(
        self,
        workout_start_time: datetime,
        workout_metric: WorkoutMetrics,
    ) -> None:
        """
        Update the Workout Metrics record if it already exists.

        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_workout_metric(
            workout_start_time,
            workout_metric,
        )

        if not updated:
            self._repository.create_workout_metric(
                workout_metric
            )