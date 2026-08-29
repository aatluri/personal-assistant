from app.modules.health.lab_service import generate_report_key


# ---------------------------------------------------------
# Test Report Key Generation
# ---------------------------------------------------------

print("\n--- TEST: GENERATE REPORT KEY ---")

report_date = "2025-06-02"
file_name = "Blood work Adarsh 20250602.pdf"

report_key = generate_report_key(
    report_date,
    file_name,
)

print(f"Generated Report_Key: {report_key}")

assert report_key.startswith("LAB_20250602_")

# LAB_ + 8 date characters + _ + 12 hash characters
assert len(report_key) == 25

print("PASS: Report_Key format is correct")


# ---------------------------------------------------------
# Test Same Input Generates Same Key
# ---------------------------------------------------------

print("\n--- TEST: DETERMINISTIC REPORT KEY ---")

report_key_again = generate_report_key(
    report_date,
    file_name,
)

assert report_key_again == report_key

print("PASS: Same report date and filename generate same key")


# ---------------------------------------------------------
# Test Different Filename Generates Different Key
# ---------------------------------------------------------

print("\n--- TEST: DIFFERENT FILENAME ---")

different_file_key = generate_report_key(
    report_date,
    "Different Report.pdf",
)

assert different_file_key != report_key

print("PASS: Different filename generates different key")


# ---------------------------------------------------------
# Test Different Date Generates Different Key
# ---------------------------------------------------------

print("\n--- TEST: DIFFERENT REPORT DATE ---")

different_date_key = generate_report_key(
    "2025-06-03",
    file_name,
)

assert different_date_key != report_key
assert different_date_key.startswith("LAB_20250603_")

print("PASS: Different report date generates different key")


print("\n===================================")
print("ALL REPORT KEY GENERATION TESTS PASSED")
print("===================================")