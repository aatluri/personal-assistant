# Prefixes added to a file's name in Google Drive after it is imported.
FAILED_PREFIX = "FAILED_"
PROCESSED_PREFIX = "PROCESSED_"

# Health Auto Export updates the files for today and yesterday on every
# export (the same file in Drive). A file dated within this many days of
# today can still change, so it is imported again on every run and only
# renamed PROCESSED_ once it is this many days old (see
# orchestrators/file_lifecycle.py).
REIMPORT_DAYS = 2

# Health Auto Export names its files <prefix>YYYY-MM-DD.json, for example
# HealthMetrics-2026-10-12.json. Only files matching this pattern are imported.
HEALTH_METRICS_FILE_PREFIX = "HealthMetrics-"
WORKOUT_METRICS_FILE_PREFIX = "WorkoutMetrics-"
HEART_RATE_NOTIFICATIONS_FILE_PREFIX = "HeartRateNotifications-"
FILE_SUFFIX = ".json"

# Date formats used by Health Auto Export.
# Timestamps inside the exports, e.g. "2026-10-29 08:00:08 +0530".
HEALTH_AUTO_EXPORT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %z"
# The date in a file name, e.g. the "2026-10-29" in HealthMetrics-2026-10-29.json.
FILENAME_DATE_FORMAT = "%Y-%m-%d"

# The source recorded with every imported record.
SOURCE = "Health Auto Export"

# Unit conversions. Health Auto Export uses US units; the backend stores
# metric units, and the conversions happen here in the importer.
FL_OZ_US_TO_ML = 29.5735
LB_TO_KG = 0.45359237
MILES_TO_KM = 1.609344
MPS_TO_KMPH = 3.6  # metres per second to kilometres per hour
SECONDS_PER_MINUTE = 60
