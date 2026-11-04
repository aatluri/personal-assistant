"""
Guards for E2E test cleanup.

The backend E2E tests run against the real Google Sheet and delete the
rows they create afterwards. Every cleanup function calls one of these
guards before touching the Sheet, for each value it matches rows on.

Test data always uses clearly fake values: the year 2099, keys starting
with TEST_, and file names starting with api_test_. If a cleanup is ever
pointed at anything else (for example a real date copied into a new
test), the guard stops the test instead of deleting real data.
"""


TEST_YEAR = "2099"
TEST_KEY_PREFIX = "TEST_"
TEST_FILE_NAME_PREFIX = "api_test_"


def require_test_date(
    value: str,
) -> None:
    """
    Allow only dates or date-times in the test year 2099, such as
    "January 01, 2099" or "January 01, 2099 10:00:00".
    """

    if TEST_YEAR not in value:
        raise ValueError(
            f"Refusing to delete rows for {value!r}: "
            f"only {TEST_YEAR} test dates may be deleted."
        )


def require_test_key(
    value: str,
) -> None:
    """
    Allow only keys starting with TEST_, such as "TEST_API_LDL".
    """

    if not value.startswith(TEST_KEY_PREFIX):
        raise ValueError(
            f"Refusing to delete rows for key {value!r}: "
            f"only keys starting with {TEST_KEY_PREFIX!r} may be deleted."
        )


def require_test_file_name(
    value: str,
) -> None:
    """
    Allow only file names starting with api_test_, such as
    "api_test_report.pdf".
    """

    if not value.startswith(TEST_FILE_NAME_PREFIX):
        raise ValueError(
            f"Refusing to delete rows for file {value!r}: "
            f"only file names starting with {TEST_FILE_NAME_PREFIX!r} "
            "may be deleted."
        )
