from datetime import datetime
from datetime import date
from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import DailyLog
from app.modules.health.schemas import BodyMeasurements

# -----------------------------------------------------------------------------
# Date formats used by the Google Sheet.
#
# Keeping these as constants means that if the sheet format ever changes,
# we only need to update them here instead of searching through the code.
# -----------------------------------------------------------------------------
DATE_FORMAT = "%B %d, %Y"
DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"


class HealthRepository:
    """
    Repository responsible for all Health module data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read data from the Daily_Log worksheet.
    - Convert raw worksheet rows into DailyLog objects.

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


# -----------------------------------------------------------------------------
# Daily Log
#
# Methods responsible for reading and writing Daily Log records
# from the Daily_Log worksheet.
# -----------------------------------------------------------------------------

    def get_daily_logs(self) -> list[DailyLog]:
        """
        Retrieves every record from the Daily_Log worksheet.

        Workflow:
        1. Authenticate with Google Sheets.
        2. Open the configured spreadsheet.
        3. Open the Daily_Log worksheet.
        4. Read all worksheet rows.
        5. Convert each row into a DailyLog object.
        6. Return a list of DailyLog objects.
        """

        worksheet = self._get_daily_log_worksheet()
        rows = worksheet.get_all_records()
        return [
            self._row_to_daily_log(row)
            for row in rows
        ]


    def get_daily_log(self, log_date: date) -> DailyLog | None:
        """
        Return the Daily Log for the specified date.
        If no matching record exists, return None.
        """

        daily_logs = self.get_daily_logs()
        for daily_log in daily_logs:
            if daily_log.date == log_date:
                return daily_log
        return None

    def get_latest_daily_log(self) -> DailyLog | None:

        """
        Return the most recent Daily Log.
        If no records exist, return None.
        """

        daily_logs = self.get_daily_logs()
        if not daily_logs:
            return None
        return max(
            daily_logs,
            key=lambda log: log.date,
        )


    def create_daily_log(self, daily_log: DailyLog) -> None:
        """
        Create a new Daily Log.

        The supplied DailyLog is converted into a worksheet row
        and appended to the Daily_Log worksheet.
        """

        worksheet = self._get_daily_log_worksheet()

        worksheet.append_row(
            self._daily_log_to_row(daily_log),
            value_input_option="USER_ENTERED",
        )

    def update_daily_log(self,log_date: date,daily_log: DailyLog,) -> bool:
        """
        Update an existing Daily Log identified by its date.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_daily_log_worksheet()

        rows = worksheet.get_all_values()

        # Search the worksheet for a row with the matching date.
        # If found, replace the entire row with the updated values.
        # Row 1 contains the worksheet headers, so data starts at row 2.
        for row_number, row in enumerate(rows[1:], start=2):
            if not row or not row[0]:
                continue

            row_date = datetime.strptime(
                row[0],
                DATE_FORMAT,
            ).date()

            if row_date == log_date:
                updated_row = self._daily_log_to_row(daily_log)

                worksheet.update(
                    range_name=f"A{row_number}:X{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False

    def _get_daily_log_worksheet(self):
        """
        Return a reference to the Daily_Log worksheet.

        All Daily Log repository methods use this helper
        instead of creating their own Google Sheets connection.
        """

        # Create an authenticated Google Sheets client.
        client = get_sheets_client()

        # Open the spreadsheet using its ID from the application configuration.
        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_DAILY_LOG_WORKSHEET
        )


    def _daily_log_to_row(self,daily_log: DailyLog,) -> list:
        """
        Convert a DailyLog object into the list format
        expected by Google Sheets.

        The column order must match the worksheet exactly.
        """

        return [
            daily_log.date.strftime(DATE_FORMAT),

            daily_log.weight_kg,

            daily_log.workout_type,
            daily_log.workout_summary,
            daily_log.workout_duration_min,
            daily_log.workout_calories_burnt,

            daily_log.steps,
            daily_log.total_calories_burnt,

            daily_log.breakfast,
            daily_log.lunch,
            daily_log.dinner,
            daily_log.snacks,

            daily_log.protein_g,
            daily_log.carbs_g,
            daily_log.fibre_g,
            daily_log.fat_g,
            daily_log.sugar_g,
            daily_log.calories_consumed,

            daily_log.water_ml,

            daily_log.first_meal_time.strftime(DATETIME_FORMAT)
            if daily_log.first_meal_time
            else "",

            daily_log.last_meal_time.strftime(DATETIME_FORMAT)
            if daily_log.last_meal_time
            else "",

            daily_log.sleep_start_time.strftime(DATETIME_FORMAT)
            if daily_log.sleep_start_time
            else "",

            daily_log.sleep_end_time.strftime(DATETIME_FORMAT)
            if daily_log.sleep_end_time
            else "",

            daily_log.notes,
        ]


    def _row_to_daily_log(self, row: dict) -> DailyLog:
        """
        Converts a single Google Sheets row into a DailyLog object.

        Input:
            Dictionary returned by Google Sheets.

        Output:
            Fully populated DailyLog model.

        Why keep this as a separate method?

        - Makes get_daily_logs() much easier to read.
        - Keeps all mapping logic in one place.
        - Prevents duplication if other repository methods need the same
          conversion logic in the future.
        """

        return DailyLog(

            # -------------------------------------------------------------
            # Convert the worksheet date string into a Python date object.
            # Example:
            # "August 1, 2026"
            #      ↓
            # date(2026, 8, 1)
            # -------------------------------------------------------------
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            # -------------------------------------------------------------
            # Numeric fields.
            #
            # Google Sheets returns an empty string for blank cells.
            # Using "or None" converts empty strings into None so the
            # application works with proper null values.
            # -------------------------------------------------------------
            weight_kg=self._empty_to_none(row["Weight (kg)"]),

            workout_type=row["Workout Type"] or None,
            workout_summary=row["Workout Summary"] or None,
            workout_duration_min=self._empty_to_none(row["Workout Duration (min)"]),
            workout_calories_burnt=self._empty_to_none(row["Workout Calories Burnt"]),

            steps=self._empty_to_none(row["Steps"]),
            total_calories_burnt=self._empty_to_none(row["Total Calories Burnt"]),

            breakfast=row["Breakfast"] or None,
            lunch=row["Lunch"] or None,
            dinner=row["Dinner"] or None,
            snacks=row["Snacks"] or None,

            protein_g=self._empty_to_none(row["Protein(g)"]),
            carbs_g=self._empty_to_none(row["Carbs(g)"]),
            fibre_g=self._empty_to_none(row["Fibre(g)"]),
            fat_g=self._empty_to_none(row["Fat(g)"]),
            sugar_g=self._empty_to_none(row["Sugar(g)"]),
            calories_consumed=self._empty_to_none(row["Calories Consumed"]),

            water_ml=self._empty_to_none(row["Water(ml)"]),

            # -------------------------------------------------------------
            # DateTime fields.
            #
            # If the worksheet cell is empty, store None.
            #
            # Otherwise convert the string into a Python datetime object.
            #
            # Example:
            #
            # "7/29/2026 7:20:00"
            #
            # becomes
            #
            # datetime(2026, 7, 29, 7, 20, 0)
            # -------------------------------------------------------------
            first_meal_time=(
                datetime.strptime(
                    row["First Meal Time"],
                    DATETIME_FORMAT,
                )
                if row["First Meal Time"]
                else None
            ),

            last_meal_time=(
                datetime.strptime(
                    row["Last Meal Time"],
                    DATETIME_FORMAT,
                )
                if row["Last Meal Time"]
                else None
            ),

            sleep_start_time=(
                datetime.strptime(
                    row["Sleep Start Time"],
                    DATETIME_FORMAT,
                )
                if row["Sleep Start Time"]
                else None
            ),

            sleep_end_time=(
                datetime.strptime(
                    row["Sleep End Time"],
                    DATETIME_FORMAT,
                )
                if row["Sleep End Time"]
                else None
            ),

            notes=row["Notes"] or None,
        )


# -----------------------------------------------------------------------------
# Body Measurements
#
# Methods responsible for reading and writing Body Measurements
# from the BodyMeasurements worksheet.
# -----------------------------------------------------------------------------

    def get_body_measurements(self) -> list[BodyMeasurements]:
        """
        Retrieves every record from the BodyMeasurements worksheet.

        Workflow:
        1. Authenticate with Google Sheets.
        2. Open the configured spreadsheet.
        3. Open the BodyMeasurements worksheet.
        4. Read all worksheet rows.
        5. Convert each row into a BodyMeasurements object.
        6. Return a list of BodyMeasurements objects.
        """

        worksheet = self._get_body_measurements_worksheet()

        # ---------------------------------------------------------------------
        # Read every row from the worksheet.
        #
        # get_all_records() returns a list of dictionaries.
        # ---------------------------------------------------------------------
        rows = worksheet.get_all_records()

        # ---------------------------------------------------------------------
        # Convert every worksheet row into a BodyMeasurements object.
        # ---------------------------------------------------------------------
        return [
            self._row_to_body_measurement(row)
            for row in rows
        ]


    def get_body_measurement(self,measurement_date: date,) -> BodyMeasurements | None:
        """
        Return the Body Measurements for the specified date.

        If no matching record exists, return None.
        """

        body_measurements = self.get_body_measurements()

        for body_measurement in body_measurements:

            if body_measurement.date == measurement_date:
                return body_measurement

        return None

    def create_body_measurement(self,body_measurement: BodyMeasurements,) -> None:
        """
        Create a new Body Measurements record.

        The supplied BodyMeasurements object is converted
        into a worksheet row and appended to the
        BodyMeasurements worksheet.
        """

        worksheet = self._get_body_measurements_worksheet()

        worksheet.append_row(
            self._body_measurement_to_row(
                body_measurement,
            ),
            value_input_option="USER_ENTERED",
        )

    def update_body_measurement(self,measurement_date: date,body_measurement: BodyMeasurements,) -> bool:
        """
        Update an existing Body Measurements record identified
        by its date.

        Returns:
            True if the matching row was found and updated.
            False if no matching row exists.
        """

        worksheet = self._get_body_measurements_worksheet()

        rows = worksheet.get_all_values()

        # Search the worksheet for a row with the matching date.
        # If found, replace the entire row with the updated values.
        # Row 1 contains the worksheet headers, so data starts at row 2.
        for row_number, row in enumerate(rows[1:], start=2):

            if not row or not row[0]:
                continue

            row_date = datetime.strptime(
                row[0],
                DATE_FORMAT,
            ).date()

            if row_date == measurement_date:

                updated_row = self._body_measurement_to_row(
                    body_measurement,
                )

                worksheet.update(
                    range_name=f"A{row_number}:R{row_number}",
                    values=[updated_row],
                    value_input_option="USER_ENTERED",
                )

                return True

        return False


    def _get_body_measurements_worksheet(self):
        """
        Return the BodyMeasurements worksheet.
        """

        # Create an authenticated Google Sheets client.
        client = get_sheets_client()

        # Open the spreadsheet using its ID from the application configuration.
        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        return spreadsheet.worksheet(
            settings.HEALTH_BODY_MEASUREMENTS_WORKSHEET
        )

    def _body_measurement_to_row(
    self,
    body_measurement: BodyMeasurements,
    ) -> list:
        """
        Convert a BodyMeasurements object
        into a worksheet row.
        """

        return [

            body_measurement.date.strftime(DATE_FORMAT),

            body_measurement.body_fat_percent,
            body_measurement.muscle_mass_percent,
            body_measurement.visceral_fat,

            body_measurement.neck_cm,
            body_measurement.chest_cm,
            body_measurement.waist_cm,
            body_measurement.stomach_cm,
            body_measurement.hips_cm,

            body_measurement.left_arm_cm,
            body_measurement.right_arm_cm,

            body_measurement.left_forearm_cm,
            body_measurement.right_forearm_cm,

            body_measurement.left_thigh_cm,
            body_measurement.right_thigh_cm,

            body_measurement.left_calf_cm,
            body_measurement.right_calf_cm,

            body_measurement.notes,

        ]

    def _row_to_body_measurement(
    self,
    row: dict,
    ) -> BodyMeasurements:
        """
        Converts a single Google Sheets row into a
        BodyMeasurements object.

        Input:
            Dictionary returned by Google Sheets.

        Output:
            Fully populated BodyMeasurements model.
        """

        return BodyMeasurements(

            # -------------------------------------------------------------
            # Convert the worksheet date string into a Python date object.
            # -------------------------------------------------------------
            date=datetime.strptime(
                row["Date"],
                DATE_FORMAT,
            ).date(),

            # -------------------------------------------------------------
            # Numeric fields.
            #
            # Google Sheets returns an empty string for blank cells.
            # Using "or None" converts empty strings into None.
            # -------------------------------------------------------------
            body_fat_percent=self._empty_to_none(row["Body Fat (%)"]),
            muscle_mass_percent=self._empty_to_none(row["Muscle Mass (%)"]),
            visceral_fat=self._empty_to_none(row["Visceral Fat (%)"]),

            neck_cm=self._empty_to_none(row["Neck (cm)"]),
            chest_cm=self._empty_to_none(row["Chest (cm)"]),
            waist_cm=self._empty_to_none(row["Waist (cm)"]),
            stomach_cm=self._empty_to_none(row["Stomach (cm)"]),
            hips_cm=self._empty_to_none(row["Hips (cm)"]),

            left_arm_cm=self._empty_to_none(row["Left Arm (cm)"]),
            right_arm_cm=self._empty_to_none(row["Right Arm (cm)"]),

            left_forearm_cm=self._empty_to_none(row["Left Forearm (cm)"]),
            right_forearm_cm=self._empty_to_none(row["Right Forearm (cm)"]),

            left_thigh_cm=self._empty_to_none(row["Left Thigh (cm)"]),
            right_thigh_cm=self._empty_to_none(row["Right Thigh (cm)"]),

            left_calf_cm=self._empty_to_none(row["Left Calf (cm)"]),
            right_calf_cm=self._empty_to_none(row["Right Calf (cm)"]),


            notes=row["Notes"] or None,
        )