from datetime import date

from app.modules.health.nutrition_metrics_repository import (
    NutritionMetricsRepository,
)
from app.modules.health.schemas import NutritionMetrics


class NutritionMetricsService:
    """
    Service layer for Nutrition Metrics.

    The service acts as the bridge between the repository and the
    rest of the application.

    Responsibilities:
    - Implement Nutrition Metrics business logic.
    - Coordinate repository operations.
    - Perform calculations and validations when required.
    - Return NutritionMetrics models to callers.

    The service should not know how data is stored.
    """

    def __init__(self):
        """
        Create the repository used by the NutritionMetricsService.

        The Service delegates all data access to the Repository.

        As the application grows, dependency injection can be used
        instead of creating the repository directly.
        """
        self._repository = NutritionMetricsRepository()


    # -------------------------------------------------------------------------
    # Nutrition Metrics
    #
    # Business operations for Nutrition Metrics.
    # -------------------------------------------------------------------------

    def get_nutrition_metrics(self) -> list[NutritionMetrics]:
        """
        Retrieve all Nutrition Metrics.
        """
        return self._repository.get_nutrition_metrics()


    def get_nutrition_metric(
        self,
        metric_date: date,
    ) -> NutritionMetrics | None:
        """
        Return the Nutrition Metrics for the specified date.

        If no record exists, return None.
        """
        return self._repository.get_nutrition_metric(metric_date)


    def create_nutrition_metric(
        self,
        nutrition_metric: NutritionMetrics,
    ) -> None:
        """
        Create a new Nutrition Metrics record.
        """
        self._repository.create_nutrition_metric(nutrition_metric)


    def upsert_nutrition_metric(
        self,
        metric_date: date,
        nutrition_metric: NutritionMetrics,
    ) -> None:
        """
        Update the Nutrition Metrics if it already exists.

        If no matching record is found, create a new one instead.
        """

        updated = self._repository.update_nutrition_metric(
            metric_date,
            nutrition_metric,
        )

        if not updated:
            self._repository.create_nutrition_metric(
                nutrition_metric,
            )