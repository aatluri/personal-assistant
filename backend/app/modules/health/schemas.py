from datetime import date, datetime

from pydantic import BaseModel


class DailyLog(BaseModel):
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