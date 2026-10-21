from datetime import date

from pydantic import BaseModel


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