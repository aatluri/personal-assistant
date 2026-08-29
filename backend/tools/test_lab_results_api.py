import requests


BASE_URL = "http://127.0.0.1:8000/health/lab-results"

TEST_REPORT_KEY = "TEST_API_REPORT_001"
TEST_MARKER_KEY = "TEST_API_LDL"


# ---------------------------------------------------------
# Test Create
# ---------------------------------------------------------

print("\n--- TEST: POST LAB RESULT ---")

new_result = {
    "report_key": TEST_REPORT_KEY,
    "marker_key": TEST_MARKER_KEY,
    "numerical_value": 110,
    "text_value": "",
    "unit": "mg/dL",
}

response = requests.post(
    BASE_URL,
    json=new_result,
)

assert response.status_code == 201, response.text

created_result = response.json()

assert created_result["report_key"] == TEST_REPORT_KEY
assert created_result["marker_key"] == TEST_MARKER_KEY
assert created_result["numerical_value"] == 110
assert created_result["text_value"] == ""
assert created_result["unit"] == "mg/dL"

print("PASS: Lab result created through API")


# ---------------------------------------------------------
# Test Get
# ---------------------------------------------------------

print("\n--- TEST: GET LAB RESULT ---")

params = {
    "marker_key": TEST_MARKER_KEY,
}

response = requests.get(
    f"{BASE_URL}/{TEST_REPORT_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_result = response.json()

assert retrieved_result["report_key"] == TEST_REPORT_KEY
assert retrieved_result["marker_key"] == TEST_MARKER_KEY
assert retrieved_result["numerical_value"] == 110
assert retrieved_result["unit"] == "mg/dL"

print("PASS: Lab result retrieved through API")


# ---------------------------------------------------------
# Test List All
# ---------------------------------------------------------

print("\n--- TEST: GET ALL LAB RESULTS ---")

response = requests.get(BASE_URL)

assert response.status_code == 200, response.text

results = response.json()

assert isinstance(results, list)

assert any(
    result["report_key"] == TEST_REPORT_KEY
    and result["marker_key"] == TEST_MARKER_KEY
    for result in results
)

print(
    f"PASS: Lab results listed through API "
    f"({len(results)} results found)"
)


# ---------------------------------------------------------
# Test List By Report_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY REPORT KEY ---")

response = requests.get(
    BASE_URL,
    params={
        "report_key": TEST_REPORT_KEY,
    },
)

assert response.status_code == 200, response.text

report_results = response.json()

assert isinstance(report_results, list)
assert len(report_results) >= 1

assert all(
    result["report_key"] == TEST_REPORT_KEY
    for result in report_results
)

print("PASS: Lab results filtered by Report_Key")


# ---------------------------------------------------------
# Test List By Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY MARKER KEY ---")

response = requests.get(
    BASE_URL,
    params={
        "marker_key": TEST_MARKER_KEY,
    },
)

assert response.status_code == 200, response.text

marker_results = response.json()

assert isinstance(marker_results, list)
assert len(marker_results) >= 1

assert all(
    result["marker_key"] == TEST_MARKER_KEY
    for result in marker_results
)

print("PASS: Lab results filtered by Marker_Key")


# ---------------------------------------------------------
# Test List By Report_Key + Marker_Key
# ---------------------------------------------------------

print("\n--- TEST: LIST RESULTS BY BOTH KEYS ---")

response = requests.get(
    BASE_URL,
    params={
        "report_key": TEST_REPORT_KEY,
        "marker_key": TEST_MARKER_KEY,
    },
)

assert response.status_code == 200, response.text

filtered_results = response.json()

assert isinstance(filtered_results, list)
assert len(filtered_results) >= 1

assert all(
    result["report_key"] == TEST_REPORT_KEY
    and result["marker_key"] == TEST_MARKER_KEY
    for result in filtered_results
)

print("PASS: Lab results filtered by both keys")


# ---------------------------------------------------------
# Test Update
# ---------------------------------------------------------

print("\n--- TEST: PUT LAB RESULT ---")

updated_data = {
    "report_key": "THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
    "marker_key": "THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
    "numerical_value": 125,
    "text_value": "",
    "unit": "mg/dL",
}

response = requests.put(
    f"{BASE_URL}/{TEST_REPORT_KEY}",
    params=params,
    json=updated_data,
)

assert response.status_code == 200, response.text

updated_result = response.json()

assert updated_result["report_key"] == TEST_REPORT_KEY
assert updated_result["marker_key"] == TEST_MARKER_KEY
assert updated_result["numerical_value"] == 125

print("PASS: Lab result updated through API")


# ---------------------------------------------------------
# Verify Update
# ---------------------------------------------------------

print("\n--- TEST: VERIFY UPDATE ---")

response = requests.get(
    f"{BASE_URL}/{TEST_REPORT_KEY}",
    params=params,
)

assert response.status_code == 200, response.text

retrieved_updated_result = response.json()

assert retrieved_updated_result["report_key"] == TEST_REPORT_KEY
assert retrieved_updated_result["marker_key"] == TEST_MARKER_KEY
assert retrieved_updated_result["numerical_value"] == 125
assert retrieved_updated_result["unit"] == "mg/dL"

print("PASS: Updated values verified")


# ---------------------------------------------------------
# Verify Unique Key Immutability
# ---------------------------------------------------------

print("\n--- TEST: UNIQUE KEY IMMUTABILITY ---")

response = requests.get(
    f"{BASE_URL}/THIS_REPORT_KEY_SHOULD_NOT_BE_SAVED",
    params={
        "marker_key": "THIS_MARKER_KEY_SHOULD_NOT_BE_SAVED",
    },
)

assert response.status_code == 404

response = requests.get(
    f"{BASE_URL}/{TEST_REPORT_KEY}",
    params=params,
)

assert response.status_code == 200

original_result = response.json()

assert original_result["report_key"] == TEST_REPORT_KEY
assert original_result["marker_key"] == TEST_MARKER_KEY

print("PASS: Report_Key and Marker_Key cannot be changed")


# ---------------------------------------------------------
# Test Get - Not Found
# ---------------------------------------------------------

print("\n--- TEST: GET NON-EXISTENT LAB RESULT ---")

response = requests.get(
    f"{BASE_URL}/REPORT_DOES_NOT_EXIST",
    params={
        "marker_key": "MARKER_DOES_NOT_EXIST",
    },
)

assert response.status_code == 404
assert response.json()["detail"] == "Lab result not found"

print("PASS: Non-existent lab result returns 404")


# ---------------------------------------------------------
# Test Update - Not Found
# ---------------------------------------------------------

print("\n--- TEST: UPDATE NON-EXISTENT LAB RESULT ---")

response = requests.put(
    f"{BASE_URL}/REPORT_DOES_NOT_EXIST",
    params={
        "marker_key": "MARKER_DOES_NOT_EXIST",
    },
    json=updated_data,
)

assert response.status_code == 404
assert response.json()["detail"] == "Lab result not found"

print("PASS: Updating non-existent lab result returns 404")


# ---------------------------------------------------------
# Test Text Result
# ---------------------------------------------------------

print("\n--- TEST: TEXT LAB RESULT ---")

text_result = {
    "report_key": TEST_REPORT_KEY,
    "marker_key": "TEST_API_TEXT_RESULT",
    "numerical_value": None,
    "text_value": "Negative",
    "unit": "",
}

response = requests.post(
    BASE_URL,
    json=text_result,
)

assert response.status_code == 201, response.text

created_text_result = response.json()

assert created_text_result["numerical_value"] is None
assert created_text_result["text_value"] == "Negative"
assert created_text_result["unit"] == ""

print("PASS: Text lab result handled correctly")


print("\n======================================")
print("ALL LAB_RESULTS API TESTS PASSED")
print("======================================")