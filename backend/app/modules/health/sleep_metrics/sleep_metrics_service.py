from datetime import date

from app.modules.health.sleep_metrics.sleep_metrics_google_sheets_repository import (
    SleepMetricsGoogleSheetsRepository,
)
from app.modules.health.sleep_metrics.sleep_metrics_schema import (
    SleepMetrics,
)


# A missing sleep total is only calculated from the start and end times
# when the span is plausible for one night's sleep. Shorter or longer
# spans are treated as bad data, and the total is saved as sent.
MIN_SLEEP_HOURS = 1
MAX_SLEEP_HOURS = 16


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
        self._repository = SleepMetricsGoogleSheetsRepository()


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
        Create a new Sleep Metrics record, calculating a missing total
        sleep duration from the start and end times when possible.
        """
        self._repository.create_sleep_metric(
            self._with_missing_total_calculated(
                sleep_metric.date,
                sleep_metric,
            )
        )


    def upsert_sleep_metric(
        self,
        metric_date: date,
        sleep_metric: SleepMetrics,
    ) -> None:
        """
        Update the Sleep Metrics if it already exists.

        If no matching record is found, create a new one instead.
        A missing total sleep duration is calculated from the start and
        end times when possible.
        """

        sleep_metric = self._with_missing_total_calculated(
            metric_date,
            sleep_metric,
        )

        updated = self._repository.update_sleep_metric(
            metric_date,
            sleep_metric,
        )

        if not updated:
            self._repository.create_sleep_metric(
                sleep_metric,
            )


    def _with_missing_total_calculated(
        self,
        metric_date: date,
        sleep_metric: SleepMetrics,
    ) -> SleepMetrics:
        """
        Return the record to save, with a missing total sleep duration
        filled in where possible.

        Health Auto Export sometimes reports a total of 0 even though the
        sleep start and end times are known. When the incoming total is 0
        or empty:

        1. If a real total (> 0) is already stored for this date, keep it.
           The incoming value is dropped, so the update leaves it alone.
        2. Otherwise, calculate the total from the start and end times
           (incoming, or else stored) when the span is between
           MIN_SLEEP_HOURS and MAX_SLEEP_HOURS. The result is the time
           between start and end, so it includes any time awake.
        3. Otherwise, save the total exactly as sent (a 0 stays 0).

        A real incoming total is always saved as sent.
        """

        if sleep_metric.total_sleep_duration_hr:
            return sleep_metric

        existing = self._repository.get_sleep_metric(metric_date)

        if existing is not None and existing.total_sleep_duration_hr:
            return sleep_metric.model_copy(
                update={"total_sleep_duration_hr": None}
            )

        start = sleep_metric.sleep_start_time or (
            existing.sleep_start_time if existing else None
        )
        end = sleep_metric.sleep_end_time or (
            existing.sleep_end_time if existing else None
        )

        if start is None or end is None:
            return sleep_metric

        # Stored times have no timezone; incoming ones may. Compare both
        # as local times.
        span_hours = (
            end.replace(tzinfo=None) - start.replace(tzinfo=None)
        ).total_seconds() / 3600

        if not MIN_SLEEP_HOURS <= span_hours <= MAX_SLEEP_HOURS:
            return sleep_metric

        return sleep_metric.model_copy(
            update={"total_sleep_duration_hr": round(span_hours, 2)}
        )
