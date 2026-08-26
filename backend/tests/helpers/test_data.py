from datetime import date

from app.modules.health.schemas import DailyLog
from app.modules.health.schemas import BodyMeasurements


# ---------------------------------------------------------------------
# Daily Log
# ---------------------------------------------------------------------

def create_daily_log_row(**overrides) -> dict:
    """
    Return a fake Google Sheets Daily Log row.
    Creates a dictionary that looks exactly like a row returned by Google Sheets. It's used when testing methods that read from the worksheet.

    Individual values can be overridden by passing keyword arguments.

    Example:
        create_daily_log_row(**{"Weight (kg)": 82})
    """

    row = {
        "Date": "August 26, 2026",

        "Weight (kg)": 80,

        "Workout Type": "HIIT",
        "Workout Summary": "Push-ups",
        "Workout Duration (min)": 60,
        "Workout Calories Burnt": 700,

        "Steps": 10000,
        "Total Calories Burnt": 2500,

        "Breakfast": "",
        "Lunch": "",
        "Dinner": "",
        "Snacks": "",

        "Protein(g)": "",
        "Carbs(g)": "",
        "Fibre(g)": "",
        "Fat(g)": "",
        "Sugar(g)": "",
        "Calories Consumed": "",

        "Water(ml)": "",

        "First Meal Time": "",
        "Last Meal Time": "",
        "Sleep Start Time": "",
        "Sleep End Time": "",

        "Notes": "",
    }

    row.update(overrides)

    return row


def create_daily_log(**overrides) -> DailyLog:
    """
    Return a DailyLog object.
    Creates a DailyLog object. It's used when testing methods that write to the worksheet or when a repository/service method expects a DailyLog object as input.

    Individual fields can be overridden.

    Example:
        create_daily_log(weight_kg=82)
    """

    daily_log = DailyLog(
        date=date(2026, 8, 26),

        weight_kg=80,

        workout_type="HIIT",
        workout_summary="Push-ups",
        workout_duration_min=60,
        workout_calories_burnt=700,

        steps=10000,
        total_calories_burnt=2500,

        breakfast=None,
        lunch=None,
        dinner=None,
        snacks=None,

        protein_g=None,
        carbs_g=None,
        fibre_g=None,
        fat_g=None,
        sugar_g=None,
        calories_consumed=None,

        water_ml=None,

        first_meal_time=None,
        last_meal_time=None,
        sleep_start_time=None,
        sleep_end_time=None,

        notes=None,
    )

    return daily_log.model_copy(update=overrides)


# ---------------------------------------------------------------------
# Body Measurements
# Creates a dictionary that looks exactly like a row returned by Google Sheets. It's used when testing methods that read from the worksheet.
# ---------------------------------------------------------------------

def create_body_measurement_row(**overrides) -> dict:
    """
    Return a fake Google Sheets Body Measurements row.
    Creates a dictionary that looks exactly like a row returned by Google Sheets. It's used when testing methods that read from the worksheet.
    """

    row = {
        "Date": "August 26, 2026",

        "Body Fat (%)": 18,
        "Muscle Mass (%)": 42,
        "Visceral Fat (%)": 8,

        "Neck (cm)": 40,
        "Chest (cm)": 102,
        "Waist (cm)": 84,
        "Stomach (cm)": 88,
        "Hips (cm)": 98,

        "Left Arm (cm)": 36,
        "Right Arm (cm)": 36,

        "Left Forearm (cm)": 31,
        "Right Forearm (cm)": 31,

        "Left Thigh (cm)": 58,
        "Right Thigh (cm)": 58,

        "Left Calf (cm)": 39,
        "Right Calf (cm)": 39,

        "Notes": "",
    }

    row.update(overrides)

    return row


def create_body_measurement(**overrides) -> BodyMeasurements:
    """
    Return a BodyMeasurements object.
    Creates a BodyMeasurements object. It's used when testing methods that write to the worksheet or when a repository/service method expects a DailyLog object as input.
    """

    measurement = BodyMeasurements(
        date=date(2026, 8, 26),

        body_fat_percent=18,
        muscle_mass_percent=42,
        visceral_fat=8,

        neck_cm=40,
        chest_cm=102,
        waist_cm=84,
        stomach_cm=88,
        hips_cm=98,

        left_arm_cm=36,
        right_arm_cm=36,

        left_forearm_cm=31,
        right_forearm_cm=31,

        left_thigh_cm=58,
        right_thigh_cm=58,

        left_calf_cm=39,
        right_calf_cm=39,

        notes=None,
    )

    return measurement.model_copy(update=overrides)