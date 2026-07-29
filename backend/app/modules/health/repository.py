from datetime import datetime

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import DailyLog

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

        # ---------------------------------------------------------------------
        # Create an authenticated Google Sheets client.
        #
        # Authentication details are handled by get_sheets_client(), so the
        # repository does not need to know anything about credentials.
        # ---------------------------------------------------------------------
        client = get_sheets_client()

        # ---------------------------------------------------------------------
        # Open the spreadsheet using its ID from the application configuration.
        #
        # Storing the spreadsheet ID in configuration means we can easily point
        # the application to another spreadsheet without changing the code.
        # ---------------------------------------------------------------------
        spreadsheet = client.open_by_key(
            settings.GOOGLE_SHEETS_SPREADSHEET_ID
        )

        # ---------------------------------------------------------------------
        # Open the Daily_Log worksheet.
        #
        # The worksheet name is also stored in configuration so that it can be
        # renamed without modifying the repository.
        # ---------------------------------------------------------------------
        worksheet = spreadsheet.worksheet(
            settings.HEALTH_DAILY_LOG_WORKSHEET
        )

        # ---------------------------------------------------------------------
        # Read every row from the worksheet.
        #
        # get_all_records() returns a list of dictionaries.
        #
        # Example:
        #
        # [
        #     {
        #         "Date": "August 1, 2026",
        #         "Weight (kg)": 79,
        #         "Workout Type": "HIIT",
        #         ...
        #     },
        #     ...
        # ]
        # ---------------------------------------------------------------------
        rows = worksheet.get_all_records()

        # ---------------------------------------------------------------------
        # Convert every worksheet row into a DailyLog object.
        #
        # Instead of placing all the conversion logic here, we delegate that
        # responsibility to a private helper method.
        #
        # This keeps get_daily_logs() short and focused on retrieving data.
        # ---------------------------------------------------------------------
        return [
            self._row_to_daily_log(row)
            for row in rows
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
            weight_kg=row["Weight (kg)"] or None,

            workout_type=row["Workout Type"] or None,
            workout_summary=row["Workout Summary"] or None,
            workout_duration_min=row["Workout Duration (min)"] or None,
            workout_calories_burnt=row["Workout Calories Burnt"] or None,

            steps=row["Steps"] or None,
            total_calories_burnt=row["Total Calories Burnt"] or None,

            breakfast=row["Breakfast"] or None,
            lunch=row["Lunch"] or None,
            dinner=row["Dinner"] or None,
            snacks=row["Snacks"] or None,

            protein_g=row["Protein(g)"] or None,
            carbs_g=row["Carbs(g)"] or None,
            fibre_g=row["Fibre(g)"] or None,
            fat_g=row["Fat(g)"] or None,
            sugar_g=row["Sugar(g)"] or None,
            calories_consumed=row["Calories Consumed"] or None,

            water_ml=row["Water(ml)"] or None,

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