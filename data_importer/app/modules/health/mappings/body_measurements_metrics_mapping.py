# Maps fields expected by our Personal Assistant backend
# to their corresponding locations in the Health Auto Export JSON.
#
# The importer should use this mapping instead of hardcoding
# Health Auto Export field names in its processing logic.

BODY_MEASUREMENTS_METRICS_MAPPING = {
    "weight_kg": {
        "source_name": "weight_body_mass",
        "value_field": "qty",
        "value_type": "float",
        "conversion": "lb_to_kg",
    },

    "body_mass_index": {
        "source_name": "body_mass_index",
        "value_field": "qty",
        "value_type": "float",
    },

    "body_fat_percent": {
        "source_name": "body_fat_percentage",
        "value_field": "qty",
        "value_type": "float",
    },
}