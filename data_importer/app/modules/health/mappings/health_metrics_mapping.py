# Maps fields expected by our Personal Assistant backend
# to their corresponding locations in the Health Auto Export JSON.
#
# The importer should use this mapping instead of hardcoding
# Health Auto Export field names in its processing logic.

HEALTH_METRICS_MAPPING = {
    "step_count": {
        "source_name": "step_count",
        "value_field": "qty",
        "value_type": "int",
    },

    "active_energy_kcal": {
        "source_name": "active_energy",
        "value_field": "qty",
        "value_type": "int",
    },

    "resting_energy_kcal": {
        "source_name": "basal_energy_burned",
        "value_field": "qty",
        "value_type": "int",
    },

    "atrial_fibrillation_burden_percent": {
        "source_name": "atrial_fibrillation_burden",
        "value_field": "qty",
        "value_type": "int",
    },

    "blood_oxygen_saturation_percent": {
        "source_name": "blood_oxygen_saturation",
        "value_field": "qty",
        "value_type": "int",
    },

    "breathing_disturbances_count": {
        "source_name": "breathing_disturbances",
        "value_field": "qty",
        "value_type": "int",
    },

    "cardio_recovery_bpm": {
        "source_name": "cardio_recovery",
        "value_field": "qty",
        "value_type": "int",
    },

    "flights_climbed": {
        "source_name": "flights_climbed",
        "value_field": "qty",
        "value_type": "int",
    },

    "heart_rate_min_bpm": {
        "source_name": "heart_rate",
        "value_field": "Min",
        "value_type": "int",
    },

    "heart_rate_max_bpm": {
        "source_name": "heart_rate",
        "value_field": "Max",
        "value_type": "int",
    },

    "heart_rate_variability_ms": {
        "source_name": "heart_rate_variability",
        "value_field": "qty",
        "value_type": "int",
    },

    "physical_effort_kcal_hr_kg": {
        "source_name": "physical_effort",
        "value_field": "qty",
        "value_type": "int",
    },

    "respiratory_rate_bpm": {
        "source_name": "respiratory_rate",
        "value_field": "qty",
        "value_type": "int",
    },

    "resting_heart_rate_bpm": {
        "source_name": "resting_heart_rate",
        "value_field": "qty",
        "value_type": "int",
    },
}