from app.modules.health.lab_schemas import (
    LabReport,
    LabMarkerDefinition,
    LabMarkerReferenceRange,
    LabMarkerInterpretation,
    LabResult,
)


# Test LabReport
report = LabReport(
    report_key="LR_20250602",
    report_date="2025-06-02",
    collection_date="2025-06-02",
    report_datetime="2025-06-02 13:56:54",
    report_type="Blood Work",
    laboratory_name="Vijaya Medical Centre",
    file_name="Blood work Adarsh 20250602.pdf",
)

print("LabReport:")
print(report.model_dump())


# Test LabMarkerDefinition
definition = LabMarkerDefinition(
    marker_key="LDL_CHOLESTEROL",
    display_name="LDL Cholesterol",
    category="Lipids",
    panel="Lipid Profile",
    sample_type="Serum",
    value_type="Numeric",
    default_unit="mg/dL",
    is_active=True,
)

print("\nLabMarkerDefinition:")
print(definition.model_dump())


# Test LabMarkerReferenceRange
reference_range = LabMarkerReferenceRange(
    marker_key="LDL_CHOLESTEROL",
    lower_limit=None,
    upper_limit=130,
    unit="mg/dL",
    source="Vijaya Medical Centre",
)

print("\nLabMarkerReferenceRange:")
print(reference_range.model_dump())


# Test LabMarkerInterpretation
interpretation = LabMarkerInterpretation(
    marker_key="VITAMIN_D",
    label="Insufficiency",
    lower_limit=20,
    upper_limit=29,
)

print("\nLabMarkerInterpretation:")
print(interpretation.model_dump())


# Test numeric LabResult
numeric_result = LabResult(
    report_key="LR_20250602",
    marker_key="LDL_CHOLESTEROL",
    numerical_value=133,
    unit="mg/dL",
)

print("\nNumeric LabResult:")
print(numeric_result.model_dump())


# Test text LabResult
text_result = LabResult(
    report_key="LR_20250602",
    marker_key="STOOL_OCCULT_BLOOD",
    text_value="Negative",
)

print("\nText LabResult:")
print(text_result.model_dump())