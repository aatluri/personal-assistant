"""
Date and time formats used in the Google Sheet.

Every metric repository reads and writes dates and times with these
formats, for example "October 08, 2026" and "October 08, 2026 06:30:00".
Changing them would also mean converting the dates already stored in the
Sheet.

The labs module (labs/lab_repository.py) stores its Updated timestamp in
a different format ("%Y-%m-%d %H:%M:%S") and does not use these.
"""

DATE_FORMAT = "%B %d, %Y"
DATETIME_FORMAT = "%B %d, %Y %H:%M:%S"
