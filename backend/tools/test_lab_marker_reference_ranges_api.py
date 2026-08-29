import requests


BASE_URL = (
    "http://127.0.0.1:8000/health/lab-marker-reference-ranges"
)

TEST_MARKER_KEY = "TEST_API_LDL"
TEST_GENDER = "Male"
TEST_MIN_AGE = 18
TEST_MAX_AGE = 65


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: POST LAB MARKER REFERENCE RANGE ---")

new_reference_range = {
    "marker_key": TEST_MARKER_KEY,
    "gender": TEST_GENDER,
    "min_age": TEST_MIN_AGE,
    "max_age": TEST_MAX_AGE,
    "lower_limit": 0,
    "upper_limit": 130,
    "unit": "mg/dL",
    "source": "API Test",
}

response = requests.post(
    BASE_URL,
    json=new_reference_range,
)

assert response.status_code == 201, response.text

created_reference_range = response.json()

assert created_reference_range["marker_key"] == TEST_MARKER_KEY
assert created_reference_range["gender"] == TEST_GENDER
assert created_reference_range["min_age"] == TEST_MIN_AGE
assert created_reference_range["max_age"] == TEST_MAX_AGE
assert created_reference_range["lower_limit"] == 0
assert created_reference_range["upper_limit"] == 130
assert created_reference_range["unit"] == "mg/dL"

print("PASS: Lab marker reference range created through API")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER REFERENCE RANGE ---")

params = {
    "gender": TEST_GENDER,
    "min_age": TEST_MIN_AGE,
    "max_age": TEST_MAX_AGE,
}

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_reference_range = response.json()

assert retrieved_reference_range["marker_key"] == TEST_MARKER_KEY
assert retrieved_reference_range["gender"] == TEST_GENDER
assert retrieved_reference_range["min_age"] == TEST_MIN_AGE
assert retrieved_reference_range["max_age"] == TEST_MAX_AGE
assert retrieved_reference_range["lower_limit"] == 0
assert retrieved_reference_range["upper_limit"] == 130
assert retrieved_reference_range["unit"] == "mg/dL"
assert retrieved_reference_range["source"] == "API Test"

print("PASS: Lab marker reference range retrieved through API")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: GET ALL LAB MARKER REFERENCE RANGES ---")

response = requests.get(BASE_URL)

assert response.status_code == 200, response.text

reference_ranges = response.json()

assert isinstance(reference_ranges, list)

assert any(
    reference_range["marker_key"] == TEST_MARKER_KEY
    and reference_range["gender"] == TEST_GENDER
    and reference_range["min_age"] == TEST_MIN_AGE
    and reference_range["max_age"] == TEST_MAX_AGE
    for reference_range in reference_ranges
)

print(
    f"PASS: Lab marker reference ranges listed through API "
    f"({len(reference_ranges)} ranges found)"
)


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST REFERENCE RANGES BY MARKER KEY ---")

response = requests.get(
    BASE_URL,
    params={"marker_key": TEST_MARKER_KEY},
)

assert response.status_code == 200, response.text

marker_reference_ranges = response.json()

assert isinstance(marker_reference_ranges, list)
assert len(marker_reference_ranges) >= 1

assert all(
    reference_range["marker_key"] == TEST_MARKER_KEY
    for reference_range in marker_reference_ranges
)

print("PASS: Reference ranges filtered by Marker_Key")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: PUT LAB MARKER REFERENCE RANGE ---")

updated_data = {
    "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
    "gender": "Female",
    "min_age": 99,
    "max_age": 100,
    "lower_limit": 10,
    "upper_limit": 120,
    "unit": "mmol/L",
    "source": "Updated API Test",
}

response = requests.put(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
    json=updated_data,
)

assert response.status_code == 200, response.text

updated_reference_range = response.json()

assert updated_reference_range["marker_key"] == TEST_MARKER_KEY
assert updated_reference_range["gender"] == TEST_GENDER
assert updated_reference_range["min_age"] == TEST_MIN_AGE
assert updated_reference_range["max_age"] == TEST_MAX_AGE

print("PASS: Lab marker reference range updated through API")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_updated_range = response.json()

assert retrieved_updated_range["lower_limit"] == 10
assert retrieved_updated_range["upper_limit"] == 120
assert retrieved_updated_range["unit"] == "mmol/L"
assert retrieved_updated_range["source"] == "Updated API Test"

print("PASS: Updated values verified")


# ---------------------------------------------------------
# Verify Unique Key Immutability
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

wrong_params = {
    "gender": "Female",
    "min_age": 99,
    "max_age": 100,
}

response = requests.get(
    f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED",
    params=wrong_params,
)

assert response.status_code == 404

# Original unique-key combination must still exist.
response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200

original_range = response.json()

assert original_range["marker_key"] == TEST_MARKER_KEY
assert original_range["gender"] == TEST_GENDER
assert original_range["min_age"] == TEST_MIN_AGE
assert original_range["max_age"] == TEST_MAX_AGE

print(
    "PASS: Marker_Key, Gender, Min_Age and Max_Age "
    "cannot be changed"
)


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT REFERENCE RANGE ---")

response = requests.get(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
    params=params,
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker reference range not found"
)

print("PASS: Non-existent reference range returns 404")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT REFERENCE RANGE ---")

response = requests.put(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
    params=params,
    json=updated_data,
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker reference range not found"
)

print("PASS: Updating non-existent reference range returns 404")


# ---------------------------------------------------------
# Test Optional Age Values
# ---------------------------------------------------------

print("\n--- TEST: OPTIONAL AGE VALUES ---")

optional_age_range = {
    "marker_key": "TEST_API_OPTIONAL_AGE",
    "gender": "All",
    "min_age": None,
    "max_age": None,
    "lower_limit": 5,
    "upper_limit": 10,
    "unit": "mg/dL",
    "source": "API Test",
}

response = requests.post(
    BASE_URL,
    json=optional_age_range,
)

assert response.status_code == 201, response.text

response = requests.get(
    f"{BASE_URL}/TEST_API_OPTIONAL_AGE",
    params={
        "gender": "All",
    },
)

assert response.status_code == 200, response.text

retrieved_optional_range = response.json()

assert retrieved_optional_range["min_age"] is None
assert retrieved_optional_range["max_age"] is None
assert retrieved_optional_range["lower_limit"] == 5
assert retrieved_optional_range["upper_limit"] == 10

print("PASS: Optional age values handled correctly")


print("\n================================================")
print("ALL LAB_MARKER_REFERENCE_RANGES API TESTS PASSED")
print("================================================")