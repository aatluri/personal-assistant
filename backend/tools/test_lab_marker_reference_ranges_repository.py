from app.modules.health.lab_repository import (
    create_lab_marker_reference_range,
    get_lab_marker_reference_range,
    list_lab_marker_reference_ranges,
    update_lab_marker_reference_range,
)

from app.modules.health.lab_schemas import LabMarkerReferenceRange


TEST_MARKER_KEY = "TEST_LDL"
TEST_GENDER = "Male"
TEST_MIN_AGE = 18
TEST_MAX_AGE = 65


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: CREATE LAB MARKER REFERENCE RANGE ---")

new_reference_range = LabMarkerReferenceRange(
    marker_key=TEST_MARKER_KEY,
    gender=TEST_GENDER,
    min_age=TEST_MIN_AGE,
    max_age=TEST_MAX_AGE,
    lower_limit=0,
    upper_limit=130,
    unit="mg/dL",
    source="Repository Test",
)

created_reference_range = create_lab_marker_reference_range(
    new_reference_range
)

assert created_reference_range.marker_key == TEST_MARKER_KEY
assert created_reference_range.gender == TEST_GENDER
assert created_reference_range.min_age == TEST_MIN_AGE
assert created_reference_range.max_age == TEST_MAX_AGE
assert created_reference_range.lower_limit == 0
assert created_reference_range.upper_limit == 130

print("PASS: Lab marker reference range created")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER REFERENCE RANGE ---")

retrieved_reference_range = get_lab_marker_reference_range(
    TEST_MARKER_KEY,
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
)

assert retrieved_reference_range is not None
assert retrieved_reference_range.marker_key == TEST_MARKER_KEY
assert retrieved_reference_range.gender == TEST_GENDER
assert retrieved_reference_range.min_age == TEST_MIN_AGE
assert retrieved_reference_range.max_age == TEST_MAX_AGE
assert retrieved_reference_range.lower_limit == 0
assert retrieved_reference_range.upper_limit == 130
assert retrieved_reference_range.unit == "mg/dL"
assert retrieved_reference_range.source == "Repository Test"

print("PASS: Lab marker reference range retrieved")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT REFERENCE RANGE ---")

missing_reference_range = get_lab_marker_reference_range(
    "MARKER_DOES_NOT_EXIST",
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
)

assert missing_reference_range is None

print("PASS: Non-existent reference range returns None")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: LIST ALL LAB MARKER REFERENCE RANGES ---")

reference_ranges = list_lab_marker_reference_ranges()

assert isinstance(reference_ranges, list)

assert any(
    reference_range.marker_key == TEST_MARKER_KEY
    and reference_range.gender == TEST_GENDER
    and reference_range.min_age == TEST_MIN_AGE
    and reference_range.max_age == TEST_MAX_AGE
    for reference_range in reference_ranges
)

print(
    f"PASS: Lab marker reference ranges listed "
    f"({len(reference_ranges)} ranges found)"
)


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST REFERENCE RANGES BY MARKER KEY ---")

marker_reference_ranges = list_lab_marker_reference_ranges(
    TEST_MARKER_KEY
)

assert isinstance(marker_reference_ranges, list)
assert len(marker_reference_ranges) >= 1

assert all(
    reference_range.marker_key == TEST_MARKER_KEY
    for reference_range in marker_reference_ranges
)

print("PASS: Reference ranges filtered by Marker_Key")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: UPDATE LAB MARKER REFERENCE RANGE ---")

updated_data = LabMarkerReferenceRange(
    marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
    gender="Female",
    min_age=99,
    max_age=100,
    lower_limit=10,
    upper_limit=120,
    unit="mmol/L",
    source="Updated Repository Test",
)

updated_reference_range = update_lab_marker_reference_range(
    TEST_MARKER_KEY,
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
    updated_data,
)

assert updated_reference_range is not None

print("PASS: Lab marker reference range updated")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

retrieved_updated_range = get_lab_marker_reference_range(
    TEST_MARKER_KEY,
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
)

assert retrieved_updated_range is not None

assert retrieved_updated_range.lower_limit == 10
assert retrieved_updated_range.upper_limit == 120
assert retrieved_updated_range.unit == "mmol/L"
assert retrieved_updated_range.source == "Updated Repository Test"

print("PASS: Updated values retrieved successfully")


# ---------------------------------------------------------
# Verify Unique Key Fields Were Not Changed
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

# The deliberately supplied new combination should not exist.
wrong_key_range = get_lab_marker_reference_range(
    "THIS_KEY_SHOULD_NOT_BE_SAVED",
    "Female",
    99,
    100,
)

assert wrong_key_range is None

# The original unique-key combination should still exist.
original_key_range = get_lab_marker_reference_range(
    TEST_MARKER_KEY,
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
)

assert original_key_range is not None
assert original_key_range.marker_key == TEST_MARKER_KEY
assert original_key_range.gender == TEST_GENDER
assert original_key_range.min_age == TEST_MIN_AGE
assert original_key_range.max_age == TEST_MAX_AGE

print("PASS: Unique key fields cannot be changed")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT REFERENCE RANGE ---")

missing_update = update_lab_marker_reference_range(
    "MARKER_DOES_NOT_EXIST",
    TEST_GENDER,
    TEST_MIN_AGE,
    TEST_MAX_AGE,
    updated_data,
)

assert missing_update is None

print("PASS: Updating non-existent reference range returns None")


# ---------------------------------------------------------
# Test Optional Age Values
# ---------------------------------------------------------

print("\n--- TEST: OPTIONAL AGE VALUES ---")

optional_age_range = LabMarkerReferenceRange(
    marker_key="TEST_OPTIONAL_AGE",
    gender="All",
    min_age=None,
    max_age=None,
    lower_limit=5,
    upper_limit=10,
    unit="mg/dL",
    source="Repository Test",
)

create_lab_marker_reference_range(optional_age_range)

retrieved_optional_age_range = get_lab_marker_reference_range(
    "TEST_OPTIONAL_AGE",
    "All",
    None,
    None,
)

assert retrieved_optional_age_range is not None
assert retrieved_optional_age_range.min_age is None
assert retrieved_optional_age_range.max_age is None
assert retrieved_optional_age_range.lower_limit == 5
assert retrieved_optional_age_range.upper_limit == 10

print("PASS: Optional age values handled correctly")


print("\n===================================================")
print("ALL LAB_MARKER_REFERENCE_RANGES REPOSITORY TESTS PASSED")
print("===================================================")