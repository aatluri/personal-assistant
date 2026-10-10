"""
Health Schemas

Defines the Pydantic models used by the Health module.

These models represent the application's domain objects and are used by:
- The API layer for request and response validation.
- The Repository layer when reading from and writing to Google Sheets.
- The Service layer when passing data through the application.
"""
from datetime import date, datetime, timedelta

from pydantic import BaseModel, field_serializer


class DailyLog(BaseModel):
    """
    Represents a single Daily Log entry.

    Each instance corresponds to one row in the Daily_Log worksheet.
    """
    date: date #primary key

    weight_kg: float | None = None

    workout_type: str | None = None
    workout_summary: str | None = None
    workout_duration_min: int | None = None
    workout_calories_burnt: int | None = None

    steps: int | None = None
    total_calories_burnt: int | None = None

    breakfast: str | None = None
    lunch: str | None = None
    dinner: str | None = None
    snacks: str | None = None

    protein_g: float | None = None
    carbs_g: float | None = None
    fibre_g: float | None = None
    fat_g: float | None = None
    sugar_g: float | None = None
    calories_consumed: int | None = None

    water_ml: int | None = None

    first_meal_time: datetime | None = None
    last_meal_time: datetime | None = None
    sleep_start_time: datetime | None = None
    sleep_end_time: datetime | None = None

    notes: str | None = None


class BodyMeasurements(BaseModel):
    """
    Represents a single Body Measurements entry.

    Each instance corresponds to one row in the BodyMeasurements worksheet.
    """
    date: date

    weight_kg: float  | None = None
    body_mass_index: float  | None = None
    body_fat_percent: float | None = None
    muscle_mass_percent: float | None = None
    visceral_fat: float | None = None

    neck_cm: float | None = None
    chest_cm: float | None = None
    waist_cm: float | None = None
    stomach_cm: float | None = None
    hips_cm: float | None = None

    left_arm_cm: float | None = None
    right_arm_cm: float | None = None

    left_forearm_cm: float | None = None
    right_forearm_cm: float | None = None

    left_thigh_cm: float | None = None
    right_thigh_cm: float | None = None

    left_calf_cm: float | None = None
    right_calf_cm: float | None = None

    notes: str | None = None



class WorkoutMetrics(BaseModel):

    """
    Represents a single Workout Metrics entry.

    Each instance corresponds to one row in the Workout_Metrics worksheet.
    """

    date: date
    workout_type: str
    workout_start_time: datetime #unique ket
    workout_end_time: datetime
    workout_duration: timedelta

    total_energy_kcal: float | None = None
    active_energy_kcal: float | None = None
    max_heart_rate_bpm: float | None = None
    avg_heart_rate_bpm: float | None = None
    distance_mi: float | None = None
    avg_speed_mph: float | None = None

    @field_serializer("workout_duration")
    def serialize_workout_duration(
        self,
        value: timedelta,
    ) -> str:
        total_seconds = int(value.total_seconds())

        hours, remainder = divmod(
            total_seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        return f"{hours:02}:{minutes:02}:{seconds:02}"


class SleepMetrics(BaseModel):
    """
    Represents a single Sleep Metrics entry.

    Each instance corresponds to one row in the Sleep_Metrics worksheet.
    """

    date: date  # primary key

    sleep_start_time: datetime | None = None
    sleep_end_time: datetime | None = None

    total_sleep_duration_hr: float | None = None
    core_sleep_hr: float | None = None
    rem_sleep_hr: float | None = None
    deep_sleep_hr: float | None = None
    awake_hr: float | None = None

    source: str | None = None


class HealthMetrics(BaseModel):
    """
    Represents a single Health Metrics entry.

    Each instance corresponds to one row in the Health_Metrics worksheet.
    """

    date: date  # primary key

    step_count: int | None = None

    active_energy_kcal: float | None = None
    resting_energy_kcal: float | None = None

    atrial_fibrillation_burden_percent: float | None = None
    blood_oxygen_saturation_percent: float | None = None
    breathing_disturbances_count: float | None = None
    cardio_recovery_bpm: float | None = None

    flights_climbed: int | None = None

    heart_rate_min_bpm: float | None = None
    heart_rate_max_bpm: float | None = None
    heart_rate_variability_ms: float | None = None

    physical_effort_kcal_hr_kg: float | None = None

    respiratory_rate_bpm: float | None = None
    resting_heart_rate_bpm: float | None = None

    source: str | None = None


class NutritionMetrics(BaseModel):
    """
    Represents a single Nutrition Metrics entry.

    Each instance corresponds to one row in the Nutrition_Metrics worksheet.
    """

    date: date  # primary key

    dietary_energy_kcal: float | None = None

    protein_g: float | None = None
    carbohydrates_g: float | None = None
    fiber_g: float | None = None
    sugar_g: float | None = None

    total_fat_g: float | None = None
    saturated_fat_g: float | None = None
    polyunsaturated_fat_g: float | None = None
    monounsaturated_fat_g: float | None = None

    water_fl_oz_us: float | None = None
    cholesterol_mg: float | None = None

    source: str | None = None