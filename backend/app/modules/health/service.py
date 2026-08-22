from app.modules.health.repository import HealthRepository
from app.modules.health.schemas import DailyLog, BodyMeasurements
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
        Create the Repository used by the HealthService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = HealthRepository()


# -----------------------------------------------------------------------------
# Daily Log
#
# Business operations for Daily Logs.
# -----------------------------------------------------------------------------

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

    def upsert_daily_log(self,log_date: date,daily_log: DailyLog,) -> None:
        """
        Update the Daily Log if it already exists.
        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_daily_log(
            log_date,
            daily_log,
        )

        if not updated:
            self._repository.create_daily_log(daily_log)

# -----------------------------------------------------------------------------
# Body Measurements
#
# Business operations for Body Measurements.
# -----------------------------------------------------------------------------

    def get_body_measurements(self) -> list[BodyMeasurements]:
        """
        Retrieve all Body Measurements.
        """
        return self._repository.get_body_measurements()


    def get_body_measurement(self,measurement_date: date,) -> BodyMeasurements | None:
        """
        Return the Body Measurements for the specified date.
        If no record exists, return None.
        """
        return self._repository.get_body_measurement(measurement_date)


    def create_body_measurement(self,body_measurement: BodyMeasurements,) -> None:
        """
        Create a new Body Measurements record.
        """
        self._repository.create_body_measurement(body_measurement)


    def upsert_body_measurement(self,measurement_date: date,body_measurement: BodyMeasurements,) -> None:
        """
        Update the Body Measurement if it already exists.
        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_body_measurement(measurement_date,body_measurement,)

        if not updated:
            self._repository.create_body_measurement(body_measurement,)