from datetime import date, datetime

from app.modules.health.workout_metrics.workout_metrics_google_sheets_repository import (
    WorkoutMetricsGoogleSheetsRepository,
)
from app.modules.health.workout_metrics.workout_metrics_schema import (
    WorkoutMetrics,
)


# A missing workout duration is only calculated from the start and end
# times when the span is plausible for one workout. Shorter or longer
# spans are treated as bad data, and the duration is saved as sent.
MIN_WORKOUT_MINUTES = 1
MAX_WORKOUT_MINUTES = 24 * 60


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
        self._repository = WorkoutMetricsGoogleSheetsRepository()


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
        Create a new Workout Metrics record, calculating a missing
        duration from the start and end times when possible.
        """
        self._repository.create_workout_metric(
            self._with_missing_duration_calculated(
                workout_metric.workout_start_time,
                workout_metric,
            )
        )


    def upsert_workout_metric(
        self,
        workout_start_time: datetime,
        workout_metric: WorkoutMetrics,
    ) -> None:
        """
        Update the Workout Metrics record if it already exists.

        If no matching record is found, create a new one instead.
        A missing duration is calculated from the start and end times
        when possible.
        """

        workout_metric = self._with_missing_duration_calculated(
            workout_start_time,
            workout_metric,
        )

        updated = self._repository.update_workout_metric(
            workout_start_time,
            workout_metric,
        )

        if not updated:
            self._repository.create_workout_metric(
                workout_metric
            )


    def _with_missing_duration_calculated(
        self,
        workout_start_time: datetime,
        workout_metric: WorkoutMetrics,
    ) -> WorkoutMetrics:
        """
        Return the record to save, with a missing workout duration filled
        in where possible.

        When the incoming workout_duration_min is 0 or empty:

        1. If a real duration (> 0) is already stored for this workout,
           keep it. The incoming value is dropped, so the update leaves
           it alone.
        2. Otherwise, calculate the duration in whole minutes from the
           start and end times when the span is between
           MIN_WORKOUT_MINUTES and MAX_WORKOUT_MINUTES.
        3. Otherwise, save the duration exactly as sent (a 0 stays 0).

        A real incoming duration is always saved as sent.
        """

        if workout_metric.workout_duration_min:
            return workout_metric

        existing = self._repository.get_workout_metric(
            workout_start_time
        )

        if existing is not None and existing.workout_duration_min:
            return workout_metric.model_copy(
                update={"workout_duration_min": None}
            )

        # Stored times have no timezone; incoming ones may. Compare both
        # as local times.
        span_minutes = (
            workout_metric.workout_end_time.replace(tzinfo=None)
            - workout_metric.workout_start_time.replace(tzinfo=None)
        ).total_seconds() / 60

        if not MIN_WORKOUT_MINUTES <= span_minutes <= MAX_WORKOUT_MINUTES:
            return workout_metric

        return workout_metric.model_copy(
            update={"workout_duration_min": round(span_minutes)}
        )
