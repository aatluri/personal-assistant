import requests


BASE_URL = (
    "http://127.0.0.1:8000/health/lab-marker-interpretations"
)

TEST_MARKER_KEY = "TEST_API_LDL"
TEST_LABEL = "Optimal"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: POST LAB MARKER INTERPRETATION ---")

new_interpretation = {
    "marker_key": TEST_MARKER_KEY,
    "label": TEST_LABEL,
    "lower_limit": 0,
    "upper_limit": 100,
}

response = requests.post(
    BASE_URL,
    json=new_interpretation,
)

assert response.status_code == 201, response.text

created_interpretation = response.json()

assert created_interpretation["marker_key"] == TEST_MARKER_KEY
assert created_interpretation["label"] == TEST_LABEL
assert created_interpretation["lower_limit"] == 0
assert created_interpretation["upper_limit"] == 100

print("PASS: Lab marker interpretation created through API")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB MARKER INTERPRETATION ---")

params = {
    "label": TEST_LABEL,
}

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_interpretation = response.json()

assert retrieved_interpretation["marker_key"] == TEST_MARKER_KEY
assert retrieved_interpretation["label"] == TEST_LABEL
assert retrieved_interpretation["lower_limit"] == 0
assert retrieved_interpretation["upper_limit"] == 100

print("PASS: Lab marker interpretation retrieved through API")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: GET ALL LAB MARKER INTERPRETATIONS ---")

response = requests.get(BASE_URL)

assert response.status_code == 200, response.text

interpretations = response.json()

assert isinstance(interpretations, list)

assert any(
    interpretation["marker_key"] == TEST_MARKER_KEY
    and interpretation["label"] == TEST_LABEL
    for interpretation in interpretations
)

print(
    f"PASS: Lab marker interpretations listed through API "
    f"({len(interpretations)} interpretations found)"
)


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST INTERPRETATIONS BY MARKER KEY ---")

response = requests.get(
    BASE_URL,
    params={"marker_key": TEST_MARKER_KEY},
)

assert response.status_code == 200, response.text

marker_interpretations = response.json()

assert isinstance(marker_interpretations, list)
assert len(marker_interpretations) >= 1

assert all(
    interpretation["marker_key"] == TEST_MARKER_KEY
    for interpretation in marker_interpretations
)

print("PASS: Interpretations filtered by Marker_Key")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: PUT LAB MARKER INTERPRETATION ---")

updated_data = {
    "marker_key": "THIS_KEY_SHOULD_NOT_BE_SAVED",
    "label": "THIS_LABEL_SHOULD_NOT_BE_SAVED",
    "lower_limit": 10,
    "upper_limit": 90,
}

response = requests.put(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
    json=updated_data,
)

assert response.status_code == 200, response.text

updated_interpretation = response.json()

assert updated_interpretation["marker_key"] == TEST_MARKER_KEY
assert updated_interpretation["label"] == TEST_LABEL
assert updated_interpretation["lower_limit"] == 10
assert updated_interpretation["upper_limit"] == 90

print("PASS: Lab marker interpretation updated through API")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_updated_interpretation = response.json()

assert retrieved_updated_interpretation["marker_key"] == TEST_MARKER_KEY
assert retrieved_updated_interpretation["label"] == TEST_LABEL
assert retrieved_updated_interpretation["lower_limit"] == 10
assert retrieved_updated_interpretation["upper_limit"] == 90

print("PASS: Updated values verified")


# ---------------------------------------------------------
# Verify Unique Key Immutability
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

response = requests.get(
    f"{BASE_URL}/THIS_KEY_SHOULD_NOT_BE_SAVED",
    params={
        "label": "THIS_LABEL_SHOULD_NOT_BE_SAVED",
    },
)

assert response.status_code == 404

response = requests.get(
    f"{BASE_URL}/{TEST_MARKER_KEY}",
    params=params,
)

assert response.status_code == 200

original_interpretation = response.json()

assert original_interpretation["marker_key"] == TEST_MARKER_KEY
assert original_interpretation["label"] == TEST_LABEL

print("PASS: Marker_Key and Label cannot be changed")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT INTERPRETATION ---")

response = requests.get(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
    params={
        "label": "LABEL_DOES_NOT_EXIST",
    },
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker interpretation not found"
)

print("PASS: Non-existent interpretation returns 404")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT INTERPRETATION ---")

response = requests.put(
    f"{BASE_URL}/MARKER_DOES_NOT_EXIST",
    params={
        "label": "LABEL_DOES_NOT_EXIST",
    },
    json=updated_data,
)

assert response.status_code == 404
assert (
    response.json()["detail"]
    == "Lab marker interpretation not found"
)

print("PASS: Updating non-existent interpretation returns 404")


# ---------------------------------------------------------
# Test Optional Limits
# ---------------------------------------------------------

print("\n--- TEST: OPTIONAL LIMIT VALUES ---")

optional_interpretation = {
    "marker_key": "TEST_API_OPTIONAL_LIMIT",
    "label": "Detected",
    "lower_limit": None,
    "upper_limit": None,
}

response = requests.post(
    BASE_URL,
    json=optional_interpretation,
)

assert response.status_code == 201, response.text

response = requests.get(
    f"{BASE_URL}/TEST_API_OPTIONAL_LIMIT",
    params={
        "label": "Detected",
    },
)

assert response.status_code == 200, response.text

retrieved_optional_interpretation = response.json()

assert retrieved_optional_interpretation["lower_limit"] is None
assert retrieved_optional_interpretation["upper_limit"] is None

print("PASS: Optional limit values handled correctly")


print("\n================================================")
print("ALL LAB_MARKER_INTERPRETATIONS API TESTS PASSED")
print("================================================")