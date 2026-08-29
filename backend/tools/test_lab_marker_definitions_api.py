import requests


BASE_URL = (
    "http://127.0.0.1:8000/health/lab-marker-definitions"
)

TEST_MARKER_KEY = "TEST_API_LDL"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: POST /health/lab-marker-definitions ---")

new_definition = {
    "marker_key": TEST_MARKER_KEY,
    "display_name": "API Test LDL Cholesterol",
    "category": "Cardiovascular",
    "panel": "Lipid Profile",
    "sample_type": "Serum",
    "value_type": "Numeric",
    "default_unit": "mg/dL",
    "is_active": True,
}

response = requests.post(
    BASE_URL,
    json=new_definition,
)

assert response.status_code == 201, response.text

created_definition = response.json()

assert created_definition["marker_key"] == TEST_MARKER_KEY
assert (
    created_definition["display_name"]
    == "API Test LDL Cholesterol"
)
assert created_definition["is_active"] is True

print("PASS: Lab marker definition created through API")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER DEFINITION ---")

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}"
)

assert response.status_code == 200, response.text

retrieved_definition = response.json()

assert retrieved_definition["marker_key"] == TEST_MARKER_KEY
assert (
    retrieved_definition["display_name"]
    == "API Test LDL Cholesterol"
)
assert retrieved_definition["category"] == "Cardiovascular"
assert retrieved_definition["panel"] == "Lipid Profile"
assert retrieved_definition["sample_type"] == "Serum"
assert retrieved_definition["value_type"] == "Numeric"
assert retrieved_definition["default_unit"] == "mg/dL"
assert retrieved_definition["is_active"] is True

print("PASS: Lab marker definition retrieved through API")


# ---------------------------------------------------------
# Test List
# ---------------------------------------------------------

print("\n--- TEST: GET ALL LAB MARKER DEFINITIONS ---")

response = requests.get(BASE_URL)

assert response.status_code == 200, response.text

definitions = response.json()

assert isinstance(definitions, list)

assert any(
    definition["marker_key"] == TEST_MARKER_KEY
    for definition in definitions
)

print(
    f"PASS: Lab marker definitions listed through API "
    f"({len(definitions)} definitions found)"
)


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: PUT LAB MARKER DEFINITION ---")

updated_data = {
    "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
    "display_name": "Updated API LDL Cholesterol",
    "category": "Updated Cardiovascular",
    "panel": "Updated Lipid Profile",
    "sample_type": "Plasma",
    "value_type": "Numeric",
    "default_unit": "mmol/L",
    "is_active": False,
}

response = requests.put(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    json=updated_data,
)

assert response.status_code == 200, response.text

updated_definition = response.json()

assert updated_definition["marker_key"] == TEST_MARKER_KEY
assert (
    updated_definition["display_name"]
    == "Updated API LDL Cholesterol"
)
assert updated_definition["is_active"] is False

print("PASS: Lab marker definition updated through API")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}"
)

assert response.status_code == 200, response.text

retrieved_updated_definition = response.json()

assert retrieved_updated_definition["marker_key"] == TEST_MARKER_KEY
assert (
    retrieved_updated_definition["display_name"]
    == "Updated API LDL Cholesterol"
)
assert (
    retrieved_updated_definition["category"]
    == "Updated Cardiovascular"
)
assert retrieved_updated_definition["sample_type"] == "Plasma"
assert retrieved_updated_definition["default_unit"] == "mmol/L"
assert retrieved_updated_definition["is_active"] is False

print("PASS: Updated values verified")


# ---------------------------------------------------------
# Verify Marker_Key Immutability
# ---------------------------------------------------------

print("\n--- TEST: MARKER KEY IMMUTABILITY ---")

response = requests.get(
    f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED"
)

assert response.status_code == 404

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}"
)

assert response.status_code == 200
assert response.json()["marker_key"] == TEST_MARKER_KEY

print("PASS: Marker_Key cannot be changed")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT MARKER ---")

response = requests.get(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST"
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker definition not found"
)

print("PASS: Non-existent marker returns 404")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT MARKER ---")

response = requests.put(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
    json=updated_data,
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker definition not found"
)

print("PASS: Updating non-existent marker returns 404")


print("\n==============================================")
print("ALL LAB_MARKER_DEFINITIONS API TESTS PASSED")
print("==============================================")