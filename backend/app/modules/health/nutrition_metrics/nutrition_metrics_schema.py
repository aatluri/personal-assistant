from datetime import date

from pydantic import BaseModel


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

    water_ml: float | None = None
    cholesterol_mg: float | None = None

    source: str | None = None