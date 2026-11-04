import pytest

from tests.helpers.e2e_guards import (
    require_test_date,
    require_test_file_name,
    require_test_key,
)


"""
E2E Cleanup Guard Tests

These verify the guards the E2E tests call before deleting rows from the
real Google Sheet: test values are allowed, real-looking values are
refused before anything is deleted.
"""


# Verify that 2099 test dates and date-times are allowed.
@pytest.mark.parametrize(
    "value",
    [
        "January 01, 2099",
        "January 01, 2099 10:00:00",
    ],
)
def test_require_test_date_allows_2099(value):

    require_test_date(value)


# Verify that real dates are refused.
@pytest.mark.parametrize(
    "value",
    [
        "October 12, 2026",
        "October 12, 2026 10:00:00",
        "",
    ],
)
def test_require_test_date_refuses_real_dates(value):

    with pytest.raises(ValueError, match="only 2099 test dates"):
        require_test_date(value)


# Verify that TEST_ keys are allowed.
def test_require_test_key_allows_test_keys():

    require_test_key("TEST_API_LDL")
    require_test_key("TEST_API_REPORT_001")


# Verify that real keys are refused.
@pytest.mark.parametrize(
    "value",
    [
        "LDL",
        "LAB_20260829_4d71c9a83f12",
        "",
    ],
)
def test_require_test_key_refuses_real_keys(value):

    with pytest.raises(ValueError, match="only keys starting with 'TEST_'"):
        require_test_key(value)


# Verify that api_test_ file names are allowed.
def test_require_test_file_name_allows_test_file_names():

    require_test_file_name("api_test_report.pdf")


# Verify that real file names are refused.
@pytest.mark.parametrize(
    "value",
    [
        "Blood work Adarsh 20250602.pdf",
        "report.pdf",
        "",
    ],
)
def test_require_test_file_name_refuses_real_file_names(value):

    with pytest.raises(ValueError, match="only file names starting with"):
        require_test_file_name(value)
