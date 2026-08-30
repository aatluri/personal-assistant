from app.modules.health.lab_save_schemas import (
    LabReportSaveRequest,
    LabResultSave,
)

from app.modules.health.lab_service import (
    save_lab_report,
)


print("\n--- TEST: SAVE LAB REPORT SERVICE ---")


# =========================================================
# 1. Create Test Save Request
# =========================================================

save_request = LabReportSaveRequest(
    report_date="2026-08-30",
    collection_date="2026-08-30",
    report_datetime="2026-08-30 10:00:00",
    report_type="TEST",
    laboratory_name="TEST LAB",
    file_name="test_lab_save_service.pdf",
    notes="Created by test_lab_save_service.py",

    results=[
        # Numeric result - should be saved.
        LabResultSave(
            marker_key="FASTING_GLUCOSE",
            numerical_value=101,
            unit="mg/dl",
        ),

        # Another numeric result - should be saved.
        LabResultSave(
            marker_key="LDL_CHOLESTEROL",
            numerical_value=133,
            unit="mg/dl",
        ),

        # Text result - should also be saved.
        LabResultSave(
            marker_key="STOOL_OCCULT_BLOOD",
            text_value="Negative",
        ),

        # Completely empty result - should NOT be saved.
        LabResultSave(
            marker_key="VITAMIN_B12",
            numerical_value=None,
            text_value="",
            unit="pg/ml",
        ),

        # Whitespace-only text is also empty
        # and should NOT be saved.
        LabResultSave(
            marker_key="VITAMIN_D_25_HYDROXY",
            numerical_value=None,
            text_value="   ",
            unit="ng/ml",
        ),
    ],
)


# =========================================================
# 2. Save Report
# =========================================================

response = save_lab_report(
    save_request
)


# =========================================================
# 3. Display Saved Report
# =========================================================

print("\n--- SAVED REPORT ---")

print(f"Report Key:       {response.report.report_key}")
print(f"Report Date:      {response.report.report_date}")
print(f"Collection Date:  {response.report.collection_date}")
print(f"Report DateTime:  {response.report.report_datetime}")
print(f"Report Type:      {response.report.report_type}")
print(f"Laboratory Name:  {response.report.laboratory_name}")
print(f"File Name:        {response.report.file_name}")


# =========================================================
# 4. Display Saved Results
# =========================================================

print("\n--- SAVED RESULTS ---")

for result in response.results:
    print(
        f"{result.report_key} | "
        f"{result.marker_key} | "
        f"{result.numerical_value} | "
        f"{result.text_value} | "
        f"{result.unit}"
    )


# =========================================================
# 5. Validate Report
# =========================================================

assert response.report.report_key.startswith(
    "LAB_20260830_"
)

assert response.report.report_date == "2026-08-30"

assert response.report.file_name == (
    "test_lab_save_service.pdf"
)


# =========================================================
# 6. Validate Result Filtering
# =========================================================

# We supplied 5 marker values:
#
# FASTING_GLUCOSE       -> saved
# LDL_CHOLESTEROL       -> saved
# STOOL_OCCULT_BLOOD    -> saved
# VITAMIN_B12           -> ignored
# VITAMIN_D_25_HYDROXY  -> ignored
#
# Therefore exactly 3 Lab_Results rows should be created.

assert len(response.results) == 3


saved_marker_keys = {
    result.marker_key
    for result in response.results
}

assert "FASTING_GLUCOSE" in saved_marker_keys
assert "LDL_CHOLESTEROL" in saved_marker_keys
assert "STOOL_OCCULT_BLOOD" in saved_marker_keys

assert "VITAMIN_B12" not in saved_marker_keys
assert "VITAMIN_D_25_HYDROXY" not in saved_marker_keys


# =========================================================
# 7. Validate Report_Key Propagation
# =========================================================

# Every Lab_Result created by this save operation must use
# the same Report_Key as the Lab_Report.

for result in response.results:
    assert (
        result.report_key
        == response.report.report_key
    )


print("\n================================")
print("LAB REPORT SAVE SERVICE PASSED")
print("================================")