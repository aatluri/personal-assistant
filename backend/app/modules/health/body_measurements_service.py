from datetime import date

from app.modules.health.body_measurements_repository import (
    BodyMeasurementsRepository,
)
from app.modules.health.schemas import BodyMeasurements

class BodyMeasurementsService:
    """
    Service layer for Body Measurements.

    The service acts as the bridge between the repository and the
    rest of the application.

    Responsibilities:
    - Implement Body Measurements business logic.
    - Coordinate repository operations.
    - Perform calculations and validations when required.
    - Return BodyMeasurements models to callers.

    The service should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the BodyMeasurementsService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = BodyMeasurementsRepository()


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