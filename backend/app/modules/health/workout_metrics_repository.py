from datetime import datetime, timedelta

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import WorkoutMetrics


DATE_FORMAT = "%B %d, %Y"
DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"


class WorkoutMetricsRepository:
    """
    Repository responsible for Workout Metrics data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the Workout_Metrics worksheet.
    - Convert raw worksheet rows into WorkoutMetrics objects.
    - Convert WorkoutMetrics objects into worksheet rows.

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

    def get_workout_metrics(self) -> list[WorkoutMetrics]:
        """
        Retrieve every Workout Metrics record from the worksheet.
        """

        worksheet = self._get_workout_metrics_worksheet()

        rows = worksheet.get_all_records()

        return [
            self._row_to_workout_metrics(row)
            for row in rows
        ]

    def get_workout_metric(
        self,
        workout_start_time: datetime,
    ) -> WorkoutMetrics | None:
        """
        Return the Workout Metrics record identified by its
        workout start time.

        Workout Start Time acts as the unique key.

        If no matching record exists, return None.
        """

        workout_metrics = self.get_workout_metrics()

        for workout_metric in workout_metrics:

            if workout_metric.workout_start_time == workout_start_time:
                return workout_metric

        return None

    def create_workout_metric(
        self,
        workout_metric: WorkoutMetrics,
    ) -> None:
        """
        Create a new Workout Metrics record.

        The supplied WorkoutMetrics object is converted into
        a worksheet row and appended to the Workout_Metrics worksheet.
        """

        worksheet = self._get_workout_metrics_worksheet()

        worksheet.append_row(
            self._workout_metric_to_row(
                workout_metric,
            ),
            value_input_option="USER_ENTERED",
        )

    def update_workout_metric(
        self,
        workout_start_time: datetime,
        workout_metric: WorkoutMetrics,
    ) -> bool:
        """
        Update an existing Workout Metrics record identified
        by its Workout Start Time.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_workout_metrics_worksheet()

        rows = worksheet.get_all_values()

        # Row 1 contains the worksheet headers,
        # so workout data starts at row 2.
        for row_number, row in enumerate(rows[1:], start=2):

            # Workout Start Time is column C.
            if len(row) < 3 or not row[2]:
                continue

            row_workout_start_time = datetime.strptime(
                row[2],
                DATETIME_FORMAT,
            )

            if row_workout_start_time == workout_start_time:

                updated_row = self._workout_metric_to_row(
                    workout_metric,
                )

                # Workout_Metrics contains columns A:K.
                worksheet.update(
                    range_name=f"A{row_number}:K{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False

    def _get_workout_metrics_worksheet(self):
        """
        Return the Workout_Metrics worksheet.
        """

        client = get_sheets_client()

        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_WORKOUT_METRICS_WORKSHEET
        )

    def _workout_metric_to_row(
        self,
        workout_metric: WorkoutMetrics,
    ) -> list:
        """
        Convert a WorkoutMetrics object into a worksheet row.
        """

        return [
            workout_metric.date.strftime(DATE_FORMAT),

            workout_metric.workout_type,

            workout_metric.workout_start_time.strftime(
                DATETIME_FORMAT
            ),

            workout_metric.workout_end_time.strftime(
                DATETIME_FORMAT
            ),

            self._timedelta_to_duration(
                workout_metric.workout_duration
            ),

            workout_metric.total_energy_kcal,
            workout_metric.active_energy_kcal,

            workout_metric.max_heart_rate_bpm,
            workout_metric.avg_heart_rate_bpm,

            workout_metric.distance_mi,
            workout_metric.avg_speed_mph,
        ]

    def _row_to_workout_metrics(
        self,
        row: dict,
    ) -> WorkoutMetrics:
        """
        Convert a single Google Sheets row into a
        WorkoutMetrics object.
        """

        return WorkoutMetrics(

            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            workout_type=row["Workout Type"],

            workout_start_time=datetime.strptime(
                row["Workout Start Time"],
                DATETIME_FORMAT,
            ),

            workout_end_time=datetime.strptime(
                row["Workout End Time"],
                DATETIME_FORMAT,
            ),

            workout_duration=self._duration_to_timedelta(
                row["Workout Duration"]
            ),

            total_energy_kcal=self._empty_to_none(
                row["Total Energy (kcal)"]
            ),

            active_energy_kcal=self._empty_to_none(
                row["Active Energy (kcal)"]
            ),

            max_heart_rate_bpm=self._empty_to_none(
                row["Max Heart Rate (bpm)"]
            ),

            avg_heart_rate_bpm=self._empty_to_none(
                row["Avg Heart Rate (bpm)"]
            ),

            distance_mi=self._empty_to_none(
                row["Distance (mi)"]
            ),

            avg_speed_mph=self._empty_to_none(
                row["Avg Speed (mi/hr)"]
            ),
        )

    def _duration_to_timedelta(
        self,
        value: str,
    ) -> timedelta:
        """
        Convert an HH:MM:SS duration string into timedelta.

        Example:
            "01:30:00" -> timedelta(hours=1, minutes=30)
        """

        hours, minutes, seconds = map(
            int,
            value.split(":"),
        )

        return timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )

    def _timedelta_to_duration(
        self,
        value: timedelta,
    ) -> str:
        """
        Convert timedelta into an HH:MM:SS duration string.

        Example:
            timedelta(hours=1, minutes=30) -> "01:30:00"
        """

        total_seconds = int(
            value.total_seconds()
        )

        hours, remainder = divmod(
            total_seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        return f"{hours:02}:{minutes:02}:{seconds:02}"