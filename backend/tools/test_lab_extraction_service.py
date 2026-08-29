from pathlib import Path

from app.modules.health.lab_extraction_service import (
    get_marker_definitions_for_extraction,
    extract_lab_report,
)


# =========================================================
# Test Marker Definitions
# =========================================================

print("\n--- TEST: MARKER DEFINITIONS FOR EXTRACTION ---")

definitions = get_marker_definitions_for_extraction()

assert isinstance(definitions, list)
assert len(definitions) > 0, (
    "No active Lab_Marker_Definitions found"
)

print(f"Active marker definitions found: {len(definitions)}")

for definition in definitions[:5]:
    print(definition)

print("PASS: Marker definitions prepared successfully")


# =========================================================
# Test Actual PDF Extraction
# =========================================================

print("\n--- TEST: LAB REPORT PDF EXTRACTION ---")

pdf_path = (
    Path(__file__).parent
    / "test_data"
    / "Blood work Adarsh 20250602.pdf"
)

assert pdf_path.exists(), (
    f"Test PDF not found: {pdf_path}"
)

extraction = extract_lab_report(
    file_path=str(pdf_path),
    file_name=pdf_path.name,
)


# =========================================================
# Display Extracted Report Metadata
# =========================================================

print("\n--- REPORT METADATA ---")

print(f"Report Date:      {extraction.report_date}")
print(f"Collection Date:  {extraction.collection_date}")
print(f"Report DateTime:  {extraction.report_datetime}")
print(f"Report Type:      {extraction.report_type}")
print(f"Laboratory Name:  {extraction.laboratory_name}")
print(f"File Name:        {extraction.file_name}")


# =========================================================
# Display Mapped Results
# =========================================================

print("\n--- MAPPED RESULTS ---")

for result in extraction.results:
    print(
        f"{result.marker_key} | "
        f"{result.reported_name} | "
        f"{result.numerical_value} | "
        f"{result.text_value} | "
        f"{result.unit}"
    )

print(
    f"\nMapped results: {len(extraction.results)}"
)


# =========================================================
# Display Unmapped Results
# =========================================================

print("\n--- UNMAPPED RESULTS ---")

for result in extraction.unmapped_results:
    print(
        f"{result.reported_name} | "
        f"{result.numerical_value} | "
        f"{result.text_value} | "
        f"{result.unit}"
    )

print(
    f"\nUnmapped results: "
    f"{len(extraction.unmapped_results)}"
)


# =========================================================
# Basic Validation
# =========================================================

assert extraction.file_name == pdf_path.name

assert (
    len(extraction.results)
    + len(extraction.unmapped_results)
    > 0
), "No lab results were extracted from the PDF"


print("\n====================================")
print("LAB REPORT EXTRACTION TEST PASSED")
print("====================================")