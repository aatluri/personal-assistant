WORKOUT_METRICS_MAPPING = {

    "workout_type": {
        "source_field": "name",
    },

    "workout_start_time": {
        "source_field": "start",
    },

    "workout_end_time": {
        "source_field": "end",
    },

    "workout_duration_min": {
        "source_field": "duration",
    },

    "total_energy_kcal": {
        "source_field": "totalEnergy",
        "value_field": "qty",
    },

    "active_energy_kcal": {
        "source_field": "activeEnergyBurned",
        "value_field": "qty",
    },

    "max_heart_rate_bpm": {
        "source_field": "heartRate",
        "value_field": "max",
        "nested_value_field": "qty",
    },

    "avg_heart_rate_bpm": {
        "source_field": "heartRate",
        "value_field": "avg",
        "nested_value_field": "qty",
    },

    "distance_km": {
        "source_field": "distance",
        "value_field": "qty",
    },

    "avg_speed_kmph": {
        "source_field": "activities",
        "value_field": "metrics",
        "nested_value_field": "speed",
        "final_value_field": "qty",
    },
}