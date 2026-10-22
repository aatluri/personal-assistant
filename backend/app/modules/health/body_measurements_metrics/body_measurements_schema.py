from datetime import date

from pydantic import BaseModel


class BodyMeasurements(BaseModel):
    """
    Represents a single Body Measurements entry.

    Each instance corresponds to one row in the BodyMeasurements worksheet.
    """

    date: date

    weight_kg: float | None = None
    body_mass_index: float | None = None
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

    source: str | None = None