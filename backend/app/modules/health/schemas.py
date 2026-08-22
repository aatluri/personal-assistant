"""
Health Schemas

Defines the Pydantic models used by the Health module.

These models represent the application's domain objects and are used by:
- The API layer for request and response validation.
- The Repository layer when reading from and writing to Google Sheets.
- The Service layer when passing data through the application.
"""
from datetime import date, datetime

from pydantic import BaseModel


class DailyLog(BaseModel):
    """
    Represents a single Daily Log entry.

    Each instance corresponds to one row in the Daily_Log worksheet.
    """
    date: date

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