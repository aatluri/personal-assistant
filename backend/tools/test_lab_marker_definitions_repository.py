from app.modules.health.lab_repository import (
    create_lab_marker_definition,
    get_lab_marker_definition,
    list_lab_marker_definitions,
    update_lab_marker_definition,
)

from app.modules.health.lab_schemas import LabMarkerDefinition


TEST_MARKER_KEY = "TEST_LDL"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: CREATE LAB MARKER DEFINITION ---")

new_definition = LabMarkerDefinition(
    marker_key=TEST_MARKER_KEY,
    display_name="Test LDL Cholesterol",
    category="Cardiovascular",
    panel="Lipid Profile",
    sample_type="Serum",
    value_type="Numeric",
    default_unit="mg/dL",
    is_active=True,
)

created_definition = create_lab_marker_definition(
    new_definition
)

assert created_definition.marker_key == TEST_MARKER_KEY
assert created_definition.display_name == "Test LDL Cholesterol"
assert created_definition.is_active is True

print("PASS: Lab marker definition created")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER DEFINITION ---")

retrieved_definition = get_lab_marker_definition(
    TEST_MARKER_KEY
)

assert retrieved_definition is not None
assert retrieved_definition.marker_key == TEST_MARKER_KEY
assert (
    retrieved_definition.display_name
    == "Test LDL Cholesterol"
)
assert retrieved_definition.category == "Cardiovascular"
assert retrieved_definition.panel == "Lipid Profile"
assert retrieved_definition.sample_type == "Serum"
assert retrieved_definition.value_type == "Numeric"
assert retrieved_definition.default_unit == "mg/dL"
assert retrieved_definition.is_active is True

print("PASS: Lab marker definition retrieved")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT MARKER ---")

missing_definition = get_lab_marker_definition(
    "MARKER_DOES_NOT_EXIST"
)

assert missing_definition is None

print("PASS: Non-existent marker returns None")


# ---------------------------------------------------------
# Test List
# ---------------------------------------------------------

print("\n--- TEST: LIST LAB MARKER DEFINITIONS ---")

definitions = list_lab_marker_definitions()

assert isinstance(definitions, list)

assert any(
    definition.marker_key == TEST_MARKER_KEY
    for definition in definitions
)

print(
    f"PASS: Lab marker definitions listed "
    f"({len(definitions)} definitions found)"
)


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: UPDATE LAB MARKER DEFINITION ---")

updated_data = LabMarkerDefinition(
    marker_key="THIS_KEY_SHOULD_NOT_BE_SAVED",# This is not the actual key. We are passing it to test later that the update doesnt change the original key
    display_name="Updated LDL Cholesterol",
    category="Updated Cardiovascular",
    panel="Updated Lipid Profile",
    sample_type="Plasma",
    value_type="Numeric",
    default_unit="mmol/L",
    is_active=False,
)

updated_definition = update_lab_marker_definition(
    TEST_MARKER_KEY,
    updated_data,
)

assert updated_definition is not None

# Original Marker_Key must remain unchanged
assert updated_definition.marker_key == TEST_MARKER_KEY

print("PASS: Lab marker definition updated")


# ---------------------------------------------------------
# Verify Update in Google Sheets
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

retrieved_updated_definition = get_lab_marker_definition(
    TEST_MARKER_KEY
)

assert retrieved_updated_definition is not None
assert retrieved_updated_definition.marker_key == TEST_MARKER_KEY
assert (
    retrieved_updated_definition.display_name
    == "Updated LDL Cholesterol"
)
assert (
    retrieved_updated_definition.category
    == "Updated Cardiovascular"
)
assert (
    retrieved_updated_definition.panel
    == "Updated Lipid Profile"
)
assert retrieved_updated_definition.sample_type == "Plasma"
assert retrieved_updated_definition.default_unit == "mmol/L"
assert retrieved_updated_definition.is_active is False

print("PASS: Updated values retrieved successfully")


# ---------------------------------------------------------
# Verify Marker_Key Was Not Changed
# ---------------------------------------------------------

print("\n--- TEST: MARKER KEY IMMUTABILITY ---")

wrong_key_definition = get_lab_marker_definition(
    "THIS_KEY_SHOULD_NOT_BE_SAVED"
)

assert wrong_key_definition is None

original_key_definition = get_lab_marker_definition(
    TEST_MARKER_KEY
)

assert original_key_definition is not None
assert original_key_definition.marker_key == TEST_MARKER_KEY

print("PASS: Marker_Key cannot be changed")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT MARKER ---")

missing_update = update_lab_marker_definition(
    "MARKER_DOES_NOT_EXIST",
    updated_data,
)

assert missing_update is None

print("PASS: Updating non-existent marker returns None")


print("\n==============================================")
print("ALL LAB_MARKER_DEFINITIONS REPOSITORY TESTS PASSED")
print("==============================================")