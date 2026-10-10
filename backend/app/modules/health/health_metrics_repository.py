from datetime import datetime, date

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import HealthMetrics


DATE_FORMAT = "%B %d, %Y"


class HealthMetricsRepository:
    """
    Repository responsible for Health Metrics data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the Health_Metrics worksheet.
    - Convert raw worksheet rows into HealthMetrics objects.
    - Convert HealthMetrics objects into worksheet rows.

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

    def get_health_metrics(self) -> list[HealthMetrics]:
        """
        Retrieve every record from the Health_Metrics worksheet.
        """

        worksheet = self._get_health_metrics_worksheet()

        rows = worksheet.get_all_records()

        return [
            self._row_to_health_metrics(row)
            for row in rows
        ]

    def get_health_metric(
        self,
        metric_date: date,
    ) -> HealthMetrics | None:
        """
        Return Health Metrics for the specified date.

        If no matching record exists, return None.
        """

        health_metrics = self.get_health_metrics()

        for health_metric in health_metrics:

            if health_metric.date == metric_date:
                return health_metric

        return None

    def create_health_metric(
        self,
        health_metric: HealthMetrics,
    ) -> None:
        """
        Create a new Health Metrics record.
        """

        worksheet = self._get_health_metrics_worksheet()

        worksheet.append_row(
            self._health_metric_to_row(
                health_metric,
            ),
            value_input_option="USER_ENTERED",
        )

    def update_health_metric(
        self,
        metric_date: date,
        health_metric: HealthMetrics,
    ) -> bool:
        """
        Update an existing Health Metrics record identified by its date.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_health_metrics_worksheet()

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

                updated_row = self._health_metric_to_row(
                    health_metric,
                )

                worksheet.update(
                    range_name=f"A{row_number}:P{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False

    def _get_health_metrics_worksheet(self):
        """
        Return the Health_Metrics worksheet.
        """

        client = get_sheets_client()

        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_HEALTH_METRICS_WORKSHEET
        )

    def _health_metric_to_row(
        self,
        health_metric: HealthMetrics,
    ) -> list:
        """
        Convert a HealthMetrics object into a worksheet row.
        """

        return [
            health_metric.date.strftime(DATE_FORMAT),

            health_metric.step_count,

            health_metric.active_energy_kcal,
            health_metric.resting_energy_kcal,

            health_metric.atrial_fibrillation_burden_percent,
            health_metric.blood_oxygen_saturation_percent,
            health_metric.breathing_disturbances_count,
            health_metric.cardio_recovery_bpm,

            health_metric.flights_climbed,

            health_metric.heart_rate_min_bpm,
            health_metric.heart_rate_max_bpm,
            health_metric.heart_rate_variability_ms,

            health_metric.physical_effort_kcal_hr_kg,

            health_metric.respiratory_rate_bpm,
            health_metric.resting_heart_rate_bpm,

            health_metric.source,
        ]

    def _row_to_health_metrics(
        self,
        row: dict,
    ) -> HealthMetrics:
        """
        Convert a single Google Sheets row into a HealthMetrics object.
        """

        return HealthMetrics(
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            step_count=self._empty_to_none(
                row["Step Count (count)"]
            ),

            active_energy_kcal=self._empty_to_none(
                row["Active Energy (kcal)"]
            ),

            resting_energy_kcal=self._empty_to_none(
                row["Resting Energy (kcal)"]
            ),

            atrial_fibrillation_burden_percent=self._empty_to_none(
                row["Atrial Fibrillation Burden (%)"]
            ),

            blood_oxygen_saturation_percent=self._empty_to_none(
                row["Blood Oxygen Saturation (%)"]
            ),

            breathing_disturbances_count=self._empty_to_none(
                row["Breathing Disturbances (count)"]
            ),

            cardio_recovery_bpm=self._empty_to_none(
                row["Cardio Recovery (count/min)"]
            ),

            flights_climbed=self._empty_to_none(
                row["Flights Climbed (count)"]
            ),

            heart_rate_min_bpm=self._empty_to_none(
                row["Heart Rate [Min] (count/min)"]
            ),

            heart_rate_max_bpm=self._empty_to_none(
                row["Heart Rate [Max] (count/min)"]
            ),

            heart_rate_variability_ms=self._empty_to_none(
                row["Heart Rate Variability (ms)"]
            ),

            physical_effort_kcal_hr_kg=self._empty_to_none(
                row["Physical Effort (kcal/hr¬∑kg)"]
            ),

            respiratory_rate_bpm=self._empty_to_none(
                row["Respiratory Rate (count/min)"]
            ),

            resting_heart_rate_bpm=self._empty_to_none(
                row["Resting Heart Rate (count/min)"]
            ),

            source=row["Source"] or None,
        )