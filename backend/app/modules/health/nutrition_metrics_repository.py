from datetime import datetime, date

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import NutritionMetrics


DATE_FORMAT = "%B %d, %Y"


class NutritionMetricsRepository:
    """
    Repository responsible for Nutrition Metrics data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the Nutrition_Metrics worksheet.
    - Convert raw worksheet rows into NutritionMetrics objects.
    - Convert NutritionMetrics objects into worksheet rows.

    Responsibilities that DO NOT belong here:
    - Business rules
    - Calculations
    - Analytics
    - Validation beyond simple parsing

    Those belong in the Service layer.
    """

    def _empty_to_none(self, value):
        """
        Convert empty worksheet values into None.

        Google Sheets returns an empty string for blank cells.
        Numeric values, including 0, are preserved.
        """
        return None if value == "" else value

    def get_nutrition_metrics(self) -> list[NutritionMetrics]:
        """
        Retrieve every record from the Nutrition_Metrics worksheet.
        """

        worksheet = self._get_nutrition_metrics_worksheet()

        rows = worksheet.get_all_records()

        return [
            self._row_to_nutrition_metrics(row)
            for row in rows
        ]

    def get_nutrition_metric(
        self,
        metric_date: date,
    ) -> NutritionMetrics | None:
        """
        Return Nutrition Metrics for the specified date.

        If no matching record exists, return None.
        """

        nutrition_metrics = self.get_nutrition_metrics()

        for nutrition_metric in nutrition_metrics:

            if nutrition_metric.date == metric_date:
                return nutrition_metric

        return None

    def create_nutrition_metric(
        self,
        nutrition_metric: NutritionMetrics,
    ) -> None:
        """
        Create a new Nutrition Metrics record.
        """

        worksheet = self._get_nutrition_metrics_worksheet()

        worksheet.append_row(
            self._nutrition_metric_to_row(
                nutrition_metric,
            ),
            value_input_option="USER_ENTERED",
        )

    def update_nutrition_metric(
        self,
        metric_date: date,
        nutrition_metric: NutritionMetrics,
    ) -> bool:
        """
        Update an existing Nutrition Metrics record identified by its date.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_nutrition_metrics_worksheet()

        rows = worksheet.get_all_values()

        # Row 1 contains headers, so data starts at row 2.
        for row_number, row in enumerate(rows[1:], start=2):

            if not row or not row[0]:
                continue

            row_date = datetime.strptime(
                row[0],
                DATE_FORMAT,
            ).date()

            if row_date == metric_date:

                updated_row = self._nutrition_metric_to_row(
                    nutrition_metric,
                )

                worksheet.update(
                    range_name=f"A{row_number}:M{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False

    def _get_nutrition_metrics_worksheet(self):
        """
        Return the Nutrition_Metrics worksheet.
        """

        client = get_sheets_client()

        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_NUTRITION_METRICS_WORKSHEET
        )

    def _nutrition_metric_to_row(
        self,
        nutrition_metric: NutritionMetrics,
    ) -> list:
        """
        Convert a NutritionMetrics object into a worksheet row.
        """

        return [
            nutrition_metric.date.strftime(DATE_FORMAT),

            nutrition_metric.dietary_energy_kcal,

            nutrition_metric.protein_g,
            nutrition_metric.carbohydrates_g,
            nutrition_metric.fiber_g,
            nutrition_metric.sugar_g,

            nutrition_metric.total_fat_g,
            nutrition_metric.saturated_fat_g,
            nutrition_metric.polyunsaturated_fat_g,
            nutrition_metric.monounsaturated_fat_g,

            nutrition_metric.water_fl_oz_us,
            nutrition_metric.cholesterol_mg,

            nutrition_metric.source,
        ]

    def _row_to_nutrition_metrics(
        self,
        row: dict,
    ) -> NutritionMetrics:
        """
        Convert a single Google Sheets row into a NutritionMetrics object.
        """

        return NutritionMetrics(
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            dietary_energy_kcal=self._empty_to_none(
                row["Dietary Energy (kcal)"]
            ),

            protein_g=self._empty_to_none(
                row["Protein (g)"]
            ),

            carbohydrates_g=self._empty_to_none(
                row["Carbohydrates (g)"]
            ),

            fiber_g=self._empty_to_none(
                row["Fiber (g)"]
            ),

            sugar_g=self._empty_to_none(
                row["Sugar (g)"]
            ),

            total_fat_g=self._empty_to_none(
                row["Total Fat (g)"]
            ),

            saturated_fat_g=self._empty_to_none(
                row["Saturated Fat (g)"]
            ),

            polyunsaturated_fat_g=self._empty_to_none(
                row["Polyunsaturated Fat (g)"]
            ),

            monounsaturated_fat_g=self._empty_to_none(
                row["Monounsaturated Fat (g)"]
            ),

            water_fl_oz_us=self._empty_to_none(
                row["Water (fl_oz_us)"]
            ),

            cholesterol_mg=self._empty_to_none(
                row["Cholesterol (mg)"]
            ),

            source=row["Source"] or None,
        )