from app.modules.health.lab_repository import (
    create_lab_marker_interpretation,
    get_lab_marker_interpretation,
    list_lab_marker_interpretations,
    update_lab_marker_interpretation,
)

from app.modules.health.lab_schemas import LabMarkerInterpretation


TEST_MARKER_KEY = "TEST_LDL"
TEST_LABEL = "Optimal"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: CREATE LAB MARKER INTERPRETATION ---")

new_interpretation = LabMarkerInterpretation(
    marker_key=TEST_MARKER_KEY,
    label=TEST_LABEL,
    lower_limit=0,
    upper_limit=100,
)

created_interpretation = create_lab_marker_interpretation(
    new_interpretation
)

assert created_interpretation.marker_key == TEST_MARKER_KEY
assert created_interpretation.label == TEST_LABEL
assert created_interpretation.lower_limit == 0
assert created_interpretation.upper_limit == 100

print("PASS: Lab marker interpretation created")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER INTERPRETATION ---")

retrieved_interpretation = get_lab_marker_interpretation(
    TEST_MARKER_KEY,
    TEST_LABEL,
)

assert retrieved_interpretation is not None
assert retrieved_interpretation.marker_key == TEST_MARKER_KEY
assert retrieved_interpretation.label == TEST_LABEL
assert retrieved_interpretation.lower_limit == 0
assert retrieved_interpretation.upper_limit == 100

print("PASS: Lab marker interpretation retrieved")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT INTERPRETATION ---")

missing_interpretation = get_lab_marker_interpretation(
    "MARKER_DOES_NOT_EXIST",
    "Unknown",
)

assert missing_interpretation is None

print("PASS: Non-existent interpretation returns None")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: LIST ALL LAB MARKER INTERPRETATIONS ---")

interpretations = list_lab_marker_interpretations()

assert isinstance(interpretations, list)

assert any(
    interpretation.marker_key == TEST_MARKER_KEY
    and interpretation.label == TEST_LABEL
    for interpretation in interpretations
)

print(
    f"PASS: Lab marker interpretations listed "
    f"({len(interpretations)} interpretations found)"
)


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST INTERPRETATIONS BY MARKER KEY ---")

marker_interpretations = list_lab_marker_interpretations(
    TEST_MARKER_KEY
)

assert isinstance(marker_interpretations, list)
assert len(marker_interpretations) >= 1

assert all(
    interpretation.marker_key == TEST_MARKER_KEY
    for interpretation in marker_interpretations
)

print("PASS: Interpretations filtered by Marker_Key")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: UPDATE LAB MARKER INTERPRETATION ---")

updated_data = LabMarkerInterpretation(
    marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",
    label="THIS_LABEL_SHOULD_NOT_BE_SAVED",
    lower_limit=10,
    upper_limit=90,
)

updated_interpretation = update_lab_marker_interpretation(
    TEST_MARKER_KEY,
    TEST_LABEL,
    updated_data,
)

assert updated_interpretation is not None

print("PASS: Lab marker interpretation updated")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

retrieved_updated_interpretation = (
    get_lab_marker_interpretation(
        TEST_MARKER_KEY,
        TEST_LABEL,
    )
)

assert retrieved_updated_interpretation is not None
assert retrieved_updated_interpretation.lower_limit == 10
assert retrieved_updated_interpretation.upper_limit == 90

print("PASS: Updated values retrieved successfully")


# ---------------------------------------------------------
# Verify Unique Key Fields Were Not Changed
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

wrong_key_interpretation = get_lab_marker_interpretation(
    "THIS_KEY_SHOULD_NOT_BE_SAVED",
    "THIS_LABEL_SHOULD_NOT_BE_SAVED",
)

assert wrong_key_interpretation is None

original_interpretation = get_lab_marker_interpretation(
    TEST_MARKER_KEY,
    TEST_LABEL,
)

assert original_interpretation is not None
assert original_interpretation.marker_key == TEST_MARKER_KEY
assert original_interpretation.label == TEST_LABEL

print("PASS: Marker_Key and Label cannot be changed")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT INTERPRETATION ---")

missing_update = update_lab_marker_interpretation(
    "MARKER_DOES_NOT_EXIST",
    "Unknown",
    updated_data,
)

assert missing_update is None

print("PASS: Updating non-existent interpretation returns None")


# ---------------------------------------------------------
# Test Optional Limits
# ---------------------------------------------------------

print("\n--- TEST: OPTIONAL LIMIT VALUES ---")

optional_interpretation = LabMarkerInterpretation(
    marker_key="TEST_OPTIONAL_LIMIT",
    label="Above Range",
    lower_limit=100,
    upper_limit=None,
)

create_lab_marker_interpretation(
    optional_interpretation
)

retrieved_optional_interpretation = (
    get_lab_marker_interpretation(
        "TEST_OPTIONAL_LIMIT",
        "Above Range",
    )
)

assert retrieved_optional_interpretation is not None
assert retrieved_optional_interpretation.lower_limit == 100
assert retrieved_optional_interpretation.upper_limit is None

print("PASS: Optional limit values handled correctly")


print("\n=================================================")
print("ALL LAB_MARKER_INTERPRETATIONS REPOSITORY TESTS PASSED")
print("=================================================")