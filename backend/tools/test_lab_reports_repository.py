from app.modules.health.lab_repository import (
    create_lab_report,
    get_lab_report,
    list_lab_reports,
    update_lab_report,
)
from app.modules.health.lab_schemas import LabReport


TEST_REPORT_KEY = "TEST_LR_001"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: CREATE LAB REPORT ---")

new_report = LabReport(
    report_key=TEST_REPORT_KEY,
    report_date="2026-08-28",
    collection_date="2026-08-28",
    report_datetime="2026-08-28 10:30:00",
    report_type="Blood Work",
    laboratory_name="Test Laboratory",
    file_name="test_report.pdf",
    notes="Created by repository test",
)

created_report = create_lab_report(new_report)

assert created_report.report_key == TEST_REPORT_KEY
assert created_report.laboratory_name == "Test Laboratory"

print("PASS: Lab report created")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB REPORT ---")

retrieved_report = get_lab_report(TEST_REPORT_KEY)

assert retrieved_report is not None
assert retrieved_report.report_key == TEST_REPORT_KEY
assert retrieved_report.report_date == "2026-08-28"
assert retrieved_report.laboratory_name == "Test Laboratory"
assert retrieved_report.file_name == "test_report.pdf"

print("PASS: Lab report retrieved")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT LAB REPORT ---")

missing_report = get_lab_report("REPORT_DOES_NOT_EXIST")

assert missing_report is None

print("PASS: Non-existent report returns None")


# ---------------------------------------------------------
# Test List
# ---------------------------------------------------------

print("\n--- TEST: LIST LAB REPORTS ---")

reports = list_lab_reports()

assert isinstance(reports, list)
assert any(
    report.report_key == TEST_REPORT_KEY
    for report in reports
)

print(f"PASS: Lab reports listed ({len(reports)} reports found)")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: UPDATE LAB REPORT ---")

updated_data = LabReport(
    report_key="THIS_KEY_SHOULD_NOT_BE_SAVED" ,# This is not the actual key. We are passing it to test later that the update doesnt change the original key,
    report_date="2026-08-29",
    collection_date="2026-08-29",
    report_datetime="2026-08-29 11:45:00",
    report_type="Updated Blood Work",
    laboratory_name="Updated Test Laboratory",
    file_name="original_test_report.pdf",
    notes="Updated by repository test",
)

updated_report = update_lab_report(
    TEST_REPORT_KEY,
    updated_data,
)

assert updated_report is not None

# The original Report_Key must remain unchanged.
assert updated_report.report_key == TEST_REPORT_KEY

print("PASS: Lab report updated")


# ---------------------------------------------------------
# Verify Update in Google Sheets
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

retrieved_updated_report = get_lab_report(TEST_REPORT_KEY)

assert retrieved_updated_report is not None
assert retrieved_updated_report.report_key == TEST_REPORT_KEY
assert retrieved_updated_report.report_date == "2026-08-29"
assert (
    retrieved_updated_report.laboratory_name
    == "Updated Test Laboratory"
)
assert retrieved_updated_report.notes == "Updated by repository test"

print("PASS: Updated values retrieved successfully")


# ---------------------------------------------------------
# Verify Report_Key Was Not Changed
# ---------------------------------------------------------

print("\n--- TEST: REPORT KEY IMMUTABILITY ---")

wrong_key_report = get_lab_report(
    "THIS_KEY_SHOULD_NOT_BE_SAVED"
)

assert wrong_key_report is None

original_key_report = get_lab_report(TEST_REPORT_KEY)

assert original_key_report is not None
assert original_key_report.report_key == TEST_REPORT_KEY

print("PASS: Report_Key cannot be changed")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT REPORT ---")

missing_update = update_lab_report(
    "REPORT_DOES_NOT_EXIST",
    updated_data,
)

assert missing_update is None

print("PASS: Updating non-existent report returns None")


print("\n====================================")
print("ALL LAB_REPORTS REPOSITORY TESTS PASSED")
print("====================================")