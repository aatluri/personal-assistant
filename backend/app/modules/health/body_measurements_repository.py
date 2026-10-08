from datetime import datetime, date

from app.config import settings
from app.database.sheets_client import get_sheets_client
from app.modules.health.schemas import BodyMeasurements


DATE_FORMAT = "%B %d, %Y"

class BodyMeasurementsRepository:
    """
    Repository responsible for Body Measurements data access.

    Responsibilities:
    - Connect to Google Sheets.
    - Read and write data from the Body_Measurements worksheet.
    - Convert raw worksheet rows into BodyMeasurements objects.
    - Convert BodyMeasurements objects into worksheet rows.

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
                # This has the columns which are to be considered in the respective google sheet.
                worksheet.update(
                    range_name=f"A{row_number}:T{row_number}",
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

            body_measurement.weight_kg,
            body_measurement.body_mass_index,

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
            weight_kg=self._empty_to_none(row["Weight (kg)"]),
            body_mass_index=self._empty_to_none(row["Body Mass Index"]),
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