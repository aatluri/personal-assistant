WORKOUT_CONFIG = {
    "source_path": "data.workouts",
    "fields": {
        "date": "start",
        "workout_type": "name",
        "workout_start_time": "start",
        "workout_end_time": "end",
        "workout_duration": "duration",
        "total_energy": "totalEnergy.qty",
        "active_energy": "activeEnergyBurned.qty",
        "max_heart_rate": "heartRate.max.qty",
        "avg_heart_rate": "heartRate.avg.qty",
        "distance": "distance.qty",
        "avg_speed": "speed.qty",
    }
}

NUTRITION_CONFIG = {
    "source_path": "data.metrics",
    "date_field": "data.0.date",
    "source_field": "data.0.source",

    "fields": {
        "dietary_energy": {
            "metric_name": "dietary_energy",
            "value_path": "data.0.qty",
        },
        "protein": {
            "metric_name": "protein",
            "value_path": "data.0.qty",
        },
        "carbohydrates": {
            "metric_name": "carbohydrates",
            "value_path": "data.0.qty",
        },
        "fiber": {
            "metric_name": "fiber",
            "value_path": "data.0.qty",
        },
        "sugar": {
            "metric_name": "dietary_sugar",
            "value_path": "data.0.qty",
        },
        "total_fat": {
            "metric_name": "total_fat",
            "value_path": "data.0.qty",
        },
        "saturated_fat": {
            "metric_name": "saturated_fat",
            "value_path": "data.0.qty",
        },
        "polyunsaturated_fat": {
            "metric_name": "polyunsaturated_fat",
            "value_path": "data.0.qty",
        },
        "monounsaturated_fat": {
            "metric_name": "monounsaturated_fat",
            "value_path": "data.0.qty",
        },
        "water": {
            "metric_name": "dietary_water",
            "value_path": "data.0.qty",
        },
        "cholesterol": {
            "metric_name": "cholesterol",
            "value_path": "data.0.qty",
        },
    }
}


SLEEP_CONFIG = {
    "source_path": "data.metrics",
    "metric_name": "sleep_analysis",
    "data_path": "data",

    "fields": {
        "date": "date",
        "sleep_start_time": "sleepStart",
        "sleep_end_time": "sleepEnd",
        "total_sleep_duration": "totalSleep",
        "core_sleep": "core",
        "rem_sleep": "rem",
        "deep_sleep": "deep",
        "awake": "awake",
        "source": "source",
    }
}

HEALTH_METRICS_CONFIG = {
    "source_path": "data.metrics",
    "date_field": "data.0.date",
    "source_field": "data.0.source",

    "fields": {
        "step_count": {
            "metric_name": "step_count",
            "value_path": "data.0.qty",
        },
        "active_energy": {
            "metric_name": "active_energy",
            "value_path": "data.0.qty",
        },
        "resting_energy": {
            "metric_name": "basal_energy_burned",
            "value_path": "data.0.qty",
        },
        "atrial_fibrillation_burden": {
            "metric_name": "atrial_fibrillation_burden",
            "value_path": "data.0.qty",
        },
        "blood_oxygen_saturation": {
            "metric_name": "blood_oxygen_saturation",
            "value_path": "data.0.qty",
        },
        "breathing_disturbances": {
            "metric_name": "breathing_disturbances",
            "value_path": "data.0.qty",
        },
        "cardio_recovery": {
            "metric_name": "cardio_recovery",
            "value_path": "data.0.qty",
        },
        "flights_climbed": {
            "metric_name": "flights_climbed",
            "value_path": "data.0.qty",
        },
        "heart_rate_min": {
            "metric_name": "heart_rate",
            "value_path": "data.0.Min",
        },
        "heart_rate_max": {
            "metric_name": "heart_rate",
            "value_path": "data.0.Max",
        },
        "heart_rate_variability": {
            "metric_name": "heart_rate_variability",
            "value_path": "data.0.qty",
        },
        "physical_effort": {
            "metric_name": "physical_effort",
            "value_path": "data.0.qty",
        },
        "respiratory_rate": {
            "metric_name": "respiratory_rate",
            "value_path": "data.0.qty",
        },
        "resting_heart_rate": {
            "metric_name": "resting_heart_rate",
            "value_path": "data.0.qty",
        },
    },


}


HEART_RATE_NOTIFICATION_CONFIG = {
    "source_path": "data.heartRateNotifications",

    "fields": {
        "start_datetime": "start",
        "end_datetime": "end",
        "notification_type": "heartNotification",
        "threshold": "threshold",
        "heart_rate_readings": "heartRateData",
        "source": "source.name",
    }
}

BODY_MEASUREMENTS_CONFIG = {
    "source_path": "data.metrics",

    "fields": {
        "weight": {
            "metric_name": "weight",
            "value_path": "data.0.qty",
        },
        "body_mass_index": {
            "metric_name": "body_mass_index",
            "value_path": "data.0.qty",
        },
        "body_fat": {
            "metric_name": "body_fat_percentage",
            "value_path": "data.0.qty",
        },
    }
}