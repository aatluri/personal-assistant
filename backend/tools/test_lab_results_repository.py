from app.modules.health.lab_repository import (
    create_lab_result,
    get_lab_result,
    list_lab_results,
    update_lab_result,
)

from app.modules.health.lab_schemas import LabResult


TEST_REPORT_KEY = "TEST_REPORT_001"
TEST_MARKER_KEY = "TEST_LDL"


# ---------------------------------------------------------
# Test Create - Numerical Result
# ---------------------------------------------------------

print("\n--- TEST: CREATE NUMERICAL LAB RESULT ---")

new_result = LabResult(
    report_key=TEST_REPORT_KEY,
    marker_key=TEST_MARKER_KEY,
    numerical_value=110,
    text_value="",
    unit="mg/dL",
)

created_result = create_lab_result(new_result)

assert created_result.report_key == TEST_REPORT_KEY
assert created_result.marker_key == TEST_MARKER_KEY
assert created_result.numerical_value == 110
assert created_result.text_value == ""
assert created_result.unit == "mg/dL"

print("PASS: Numerical lab result created")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB RESULT ---")

retrieved_result = get_lab_result(
    TEST_REPORT_KEY,
    TEST_MARKER_KEY,
)

assert retrieved_result is not None
assert retrieved_result.report_key == TEST_REPORT_KEY
assert retrieved_result.marker_key == TEST_MARKER_KEY
assert retrieved_result.numerical_value == 110
assert retrieved_result.text_value == ""
assert retrieved_result.unit == "mg/dL"

print("PASS: Lab result retrieved")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT LAB RESULT ---")

missing_result = get_lab_result(
    "REPORT_DOES_NOT_EXIST",
    "MARKER_DOES_NOT_EXIST",
)

assert missing_result is None

print("PASS: Non-existent lab result returns None")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: LIST ALL LAB RESULTS ---")

results = list_lab_results()

assert isinstance(results, list)

assert any(
    result.report_key == TEST_REPORT_KEY
    and result.marker_key == TEST_MARKER_KEY
    for result in results
)

print(
    f"PASS: Lab results listed "
    f"({len(results)} results found)"
)


# ---------------------------------------------------------
# Test List By Report_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY REPORT KEY ---")

report_results = list_lab_results(
    report_key=TEST_REPORT_KEY
)

assert isinstance(report_results, list)
assert len(report_results) >= 1

assert all(
    result.report_key == TEST_REPORT_KEY
    for result in report_results
)

print("PASS: Lab results filtered by Report_Key")


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY MARKER KEY ---")

marker_results = list_lab_results(
    marker_key=TEST_MARKER_KEY
)

assert isinstance(marker_results, list)
assert len(marker_results) >= 1

assert all(
    result.marker_key == TEST_MARKER_KEY
    for result in marker_results
)

print("PASS: Lab results filtered by Marker_Key")


# ---------------------------------------------------------
# Test List By Report_Key + Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY BOTH KEYS ---")

filtered_results = list_lab_results(
    report_key=TEST_REPORT_KEY,
    marker_key=TEST_MARKER_KEY,
)

assert len(filtered_results) >= 1

assert all(
    result.report_key == TEST_REPORT_KEY
    and result.marker_key == TEST_MARKER_KEY
    for result in filtered_results
)

print("PASS: Lab results filtered by both keys")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: UPDATE LAB RESULT ---")

updated_data = LabResult(
    report_key="THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
    marker_key="THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
    numerical_value=125,
    text_value="",
    unit="mmol/L",
)

updated_result = update_lab_result(
    TEST_REPORT_KEY,
    TEST_MARKER_KEY,
    updated_data,
)

assert updated_result is not None

print("PASS: Lab result updated")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

retrieved_updated_result = get_lab_result(
    TEST_REPORT_KEY,
    TEST_MARKER_KEY,
)

assert retrieved_updated_result is not None
assert retrieved_updated_result.numerical_value == 125
assert retrieved_updated_result.text_value == ""
assert retrieved_updated_result.unit == "mmol/L"

print("PASS: Updated values retrieved successfully")


# ---------------------------------------------------------
# Verify Unique Key Fields Were Not Changed
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

wrong_key_result = get_lab_result(
    "THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
    "THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
)

assert wrong_key_result is None

original_result = get_lab_result(
    TEST_REPORT_KEY,
    TEST_MARKER_KEY,
)

assert original_result is not None
assert original_result.report_key == TEST_REPORT_KEY
assert original_result.marker_key == TEST_MARKER_KEY

print("PASS: Report_Key and Marker_Key cannot be changed")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT LAB RESULT ---")

missing_update = update_lab_result(
    "REPORT_DOES_NOT_EXIST",
    "MARKER_DOES_NOT_EXIST",
    updated_data,
)

assert missing_update is None

print("PASS: Updating non-existent lab result returns None")


# ---------------------------------------------------------
# Test Text Result
# ---------------------------------------------------------

print("\n--- TEST: TEXT LAB RESULT ---")

text_result = LabResult(
    report_key="TEST_REPORT_002",
    marker_key="TEST_HBSAG",
    numerical_value=None,
    text_value="Negative",
    unit="",
)

create_lab_result(text_result)

retrieved_text_result = get_lab_result(
    "TEST_REPORT_002",
    "TEST_HBSAG",
)

assert retrieved_text_result is not None
assert retrieved_text_result.numerical_value is None
assert retrieved_text_result.text_value == "Negative"
assert retrieved_text_result.unit == ""

print("PASS: Text lab result handled correctly")


print("\n========================================")
print("ALL LAB_RESULTS REPOSITORY TESTS PASSED")
print("========================================")