from datetime import date

from app.modules.health.schemas import (
    DailyLog,
    BodyMeasurements,
    WorkoutMetrics,
    SleepMetrics,
    NutritionMetrics,
    HealthMetrics,
)

from datetime import date, datetime, timedelta

from app.modules.health.schemas import WorkoutMetrics


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

        "Weight (kg)": 80,
        "Body Mass Index": 26.7,


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

        weight_kg=80,
        body_mass_index=26.7,


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

# ---------------------------------------------------------------------
# Workout Metrics
# ---------------------------------------------------------------------


def create_workout_metric() -> WorkoutMetrics:
    """
    Create a WorkoutMetrics object used by repository helper tests.
    """

    return WorkoutMetrics(
        date=date(2026, 10, 8),
        workout_type="Functional Strength Training",
        workout_start_time=datetime(2026, 10, 8, 6, 30, 0),
        workout_end_time=datetime(2026, 10, 8, 7, 30, 0),
        workout_duration=timedelta(hours=1),
        total_energy_kcal=500,
        active_energy_kcal=420,
        max_heart_rate_bpm=175,
        avg_heart_rate_bpm=145,
        distance_mi=3.2,
        avg_speed_mph=6.4,
    )


def create_workout_metric_row() -> dict:
    """
    Create a Google Sheets-style row used by repository helper tests.
    """

    return {
        "Date": "October 08, 2026",
        "Workout Type": "Functional Strength Training",
        "Workout Start Time": "October 08, 2026 06:30:00",
        "Workout End Time": "October 08, 2026 07:30:00",
        "Workout Duration": "01:00:00",
        "Total Energy (kcal)": 500,
        "Active Energy (kcal)": 420,
        "Max Heart Rate (bpm)": 175,
        "Avg Heart Rate (bpm)": 145,
        "Distance (mi)": 3.2,
        "Avg Speed (mi/hr)": 6.4,
    }


# ---------------------------------------------------------------------
# Sleep Metrics
# ---------------------------------------------------------------------

def create_sleep_metric(**overrides) -> SleepMetrics:
    """
    Create a SleepMetrics object used by repository and service tests.

    Individual fields can be overridden.

    Example:
        create_sleep_metric(total_sleep_duration_hr=8.0)
    """

    sleep_metric = SleepMetrics(
        date=date(2026, 10, 8),

        sleep_start_time=datetime(2026, 10, 7, 23, 0, 0),
        sleep_end_time=datetime(2026, 10, 8, 7, 0, 0),

        total_sleep_duration_hr=7.5,
        core_sleep_hr=4.0,
        rem_sleep_hr=1.5,
        deep_sleep_hr=1.5,
        awake_hr=0.5,

        source="Apple Watch",
    )

    return sleep_metric.model_copy(update=overrides)


def create_sleep_metric_row(**overrides) -> dict:
    """
    Create a Google Sheets-style Sleep Metrics row used by repository tests.

    Individual values can be overridden.

    Example:
        create_sleep_metric_row(**{"Deep Sleep (hr)": 2.0})
    """

    row = {
        "Date": "October 08, 2026",

        "Sleep Start Time": "October 07, 2026 23:00:00",
        "Sleep End Time": "October 08, 2026 07:00:00",

        "Total Sleep Duration (hr)": 7.5,
        "Core Sleep (hr)": 4.0,
        "Rem Sleep (hr)": 1.5,
        "Deep Sleep (hr)": 1.5,
        "Awake (hr)": 0.5,

        "Source": "Apple Watch",
    }

    row.update(overrides)

    return row



# ---------------------------------------------------------------------
# Nutrition Metrics
# ---------------------------------------------------------------------

def create_nutrition_metric(**overrides) -> NutritionMetrics:
    """
    Create a NutritionMetrics object used by repository and service tests.

    Individual fields can be overridden.

    Example:
        create_nutrition_metric(protein_g=120)
    """

    nutrition_metric = NutritionMetrics(
        date=date(2026, 10, 8),

        dietary_energy_kcal=1800,

        protein_g=110,
        carbohydrates_g=180,
        fiber_g=30,
        sugar_g=40,

        total_fat_g=60,
        saturated_fat_g=18,
        polyunsaturated_fat_g=12,
        monounsaturated_fat_g=25,

        water_fl_oz_us=100,
        cholesterol_mg=250,

        source="Foodnoms",
    )

    return nutrition_metric.model_copy(update=overrides)


def create_nutrition_metric_row(**overrides) -> dict:
    """
    Create a Google Sheets-style Nutrition Metrics row used by repository tests.

    Individual values can be overridden.

    Example:
        create_nutrition_metric_row(**{"Protein (g)": 120})
    """

    row = {
        "Date": "October 08, 2026",

        "Dietary Energy (kcal)": 1800,

        "Protein (g)": 110,
        "Carbohydrates (g)": 180,
        "Fiber (g)": 30,
        "Sugar (g)": 40,

        "Total Fat (g)": 60,
        "Saturated Fat (g)": 18,
        "Polyunsaturated Fat (g)": 12,
        "Monounsaturated Fat (g)": 25,

        "Water (fl_oz_us)": 100,
        "Cholesterol (mg)": 250,

        "Source": "Foodnoms",
    }

    row.update(overrides)

    return row


# ---------------------------------------------------------------------
# Health Metrics
# ---------------------------------------------------------------------

def create_health_metric(**overrides) -> HealthMetrics:
    """
    Create a HealthMetrics object used by repository and service tests.

    Individual fields can be overridden.

    Example:
        create_health_metric(step_count=12000)
    """

    health_metric = HealthMetrics(
        date=date(2026, 10, 8),

        step_count=10000,

        active_energy_kcal=650,
        resting_energy_kcal=1800,

        atrial_fibrillation_burden_percent=0,
        blood_oxygen_saturation_percent=98,
        breathing_disturbances_count=2,
        cardio_recovery_bpm=30,

        flights_climbed=8,

        heart_rate_min_bpm=45,
        heart_rate_max_bpm=175,
        heart_rate_variability_ms=55,

        physical_effort_kcal_hr_kg=4.5,

        respiratory_rate_bpm=16,
        resting_heart_rate_bpm=52,

        source="Apple Watch",
    )

    return health_metric.model_copy(update=overrides)


def create_health_metric_row(**overrides) -> dict:
    """
    Create a Google Sheets-style Health Metrics row used by repository tests.

    Individual values can be overridden.

    Example:
        create_health_metric_row(**{"Step Count (count)": 12000})
    """

    row = {
        "Date": "October 08, 2026",

        "Step Count (count)": 10000,

        "Active Energy (kcal)": 650,
        "Resting Energy (kcal)": 1800,

        "Atrial Fibrillation Burden (%)": 0,
        "Blood Oxygen Saturation (%)": 98,
        "Breathing Disturbances (count)": 2,
        "Cardio Recovery (count/min)": 30,

        "Flights Climbed (count)": 8,

        "Heart Rate [Min] (count/min)": 45,
        "Heart Rate [Max] (count/min)": 175,
        "Heart Rate Variability (ms)": 55,

        "Physical Effort (kcal/hr¬∑kg)": 4.5,

        "Respiratory Rate (count/min)": 16,
        "Resting Heart Rate (count/min)": 52,

        "Source": "Apple Watch",
    }

    row.update(overrides)

    return row