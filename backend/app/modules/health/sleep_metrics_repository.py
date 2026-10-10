from datetime import datetime, date

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import SleepMetrics


DATE_FORMAT = "%B %d, %Y"
DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"


class SleepMetricsRepository:
    """
    Repository responsible for Sleep Metrics data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the Sleep_Metrics worksheet.
    - Convert raw worksheet rows into SleepMetrics objects.
    - Convert SleepMetrics objects into worksheet rows.

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

    def get_sleep_metrics(self) -> list[SleepMetrics]:
        """
        Retrieve every record from the Sleep_Metrics worksheet.
        """

        worksheet = self._get_sleep_metrics_worksheet()

        rows = worksheet.get_all_records()

        return [
            self._row_to_sleep_metrics(row)
            for row in rows
        ]

    def get_sleep_metric(
        self,
        metric_date: date,
    ) -> SleepMetrics | None:
        """
        Return Sleep Metrics for the specified date.

        If no matching record exists, return None.
        """

        sleep_metrics = self.get_sleep_metrics()

        for sleep_metric in sleep_metrics:

            if sleep_metric.date == metric_date:
                return sleep_metric

        return None

    def create_sleep_metric(
        self,
        sleep_metric: SleepMetrics,
    ) -> None:
        """
        Create a new Sleep Metrics record.
        """

        worksheet = self._get_sleep_metrics_worksheet()

        worksheet.append_row(
            self._sleep_metric_to_row(
                sleep_metric,
            ),
            value_input_option="USER_ENTERED",
        )

    def update_sleep_metric(
        self,
        metric_date: date,
        sleep_metric: SleepMetrics,
    ) -> bool:
        """
        Update an existing Sleep Metrics record identified by its date.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_sleep_metrics_worksheet()

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

                updated_row = self._sleep_metric_to_row(
                    sleep_metric,
                )

                worksheet.update(
                    range_name=f"A{row_number}:I{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False

    def _get_sleep_metrics_worksheet(self):
        """
        Return the Sleep_Metrics worksheet.
        """

        client = get_sheets_client()

        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_SLEEP_METRICS_WORKSHEET
        )

    def _sleep_metric_to_row(
        self,
        sleep_metric: SleepMetrics,
    ) -> list:
        """
        Convert a SleepMetrics object into a worksheet row.
        """

        return [
            sleep_metric.date.strftime(DATE_FORMAT),

            (
                sleep_metric.sleep_start_time.strftime(DATETIME_FORMAT)
                if sleep_metric.sleep_start_time
                else None
            ),

            (
                sleep_metric.sleep_end_time.strftime(DATETIME_FORMAT)
                if sleep_metric.sleep_end_time
                else None
            ),

            sleep_metric.total_sleep_duration_hr,
            sleep_metric.core_sleep_hr,
            sleep_metric.rem_sleep_hr,
            sleep_metric.deep_sleep_hr,
            sleep_metric.awake_hr,

            sleep_metric.source,
        ]

    def _row_to_sleep_metrics(
        self,
        row: dict,
    ) -> SleepMetrics:
        """
        Convert a single Google Sheets row into a SleepMetrics object.
        """

        sleep_start_time = self._empty_to_none(
            row["Sleep Start Time"]
        )

        sleep_end_time = self._empty_to_none(
            row["Sleep End Time"]
        )

        return SleepMetrics(
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            sleep_start_time=(
                datetime.strptime(
                    sleep_start_time,
                    DATETIME_FORMAT,
                )
                if sleep_start_time
                else None
            ),

            sleep_end_time=(
                datetime.strptime(
                    sleep_end_time,
                    DATETIME_FORMAT,
                )
                if sleep_end_time
                else None
            ),

            total_sleep_duration_hr=self._empty_to_none(
                row["Total Sleep Duration (hr)"]
            ),

            core_sleep_hr=self._empty_to_none(
                row["Core Sleep (hr)"]
            ),

            rem_sleep_hr=self._empty_to_none(
                row["Rem Sleep (hr)"]
            ),

            deep_sleep_hr=self._empty_to_none(
                row["Deep Sleep (hr)"]
            ),

            awake_hr=self._empty_to_none(
                row["Awake (hr)"]
            ),

            source=row["Source"] or None,
        )