from app.modules.health.lab_repository import (
    list_lab_marker_definitions,
)
import base64
import json

from app.ai.openai_client import get_openai_client
from app.modules.health.lab_extraction_schemas import (
    LabReportExtraction,
)


def get_marker_definitions_for_extraction() -> list[dict]:
    """
    Get active lab marker definitions and convert them
    into the compact format required for AI extraction.

    These definitions will be provided to the AI so that
    extracted test names can be mapped to existing Marker_Keys.
    """

    definitions = list_lab_marker_definitions()

    marker_definitions = []

    for definition in definitions:

        # Ignore inactive markers.
        if not definition.is_active:
            continue

        marker_definitions.append(
            {
                "marker_key": definition.marker_key,
                "display_name": definition.display_name,
                "category": definition.category,
                "panel": definition.panel,
                "default_unit": definition.default_unit,
            }
        )

    return marker_definitions

def extract_lab_report(
    file_path: str,
    file_name: str,
) -> LabReportExtraction:
    """
    Extract lab report metadata and marker results from a PDF.

    The PDF and the existing active Lab_Marker_Definitions
    are sent to OpenAI.

    OpenAI maps report markers to existing Marker_Keys.
    Markers that cannot be confidently mapped are returned
    as unmapped_results.

    Nothing is saved to Google Sheets by this function.
    """

    # Get the marker definitions that OpenAI is allowed to use.
    marker_definitions = get_marker_definitions_for_extraction()

    if not marker_definitions:
        raise ValueError(
            "No active Lab_Marker_Definitions found"
        )

    # Convert the PDF to base64 so it can be sent to OpenAI.
    with open(file_path, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(
            pdf_file.read()
        ).decode("utf-8")

    client = get_openai_client()

    instructions = f"""
You are extracting structured data from a laboratory report.

Existing lab marker definitions:

{json.dumps(marker_definitions, indent=2)}

RULES:

1. Extract the report metadata from the PDF.

2. Extract every laboratory test result present in the report.

3. For each result, map it to an existing marker_key ONLY when
   you are confident that the test represents that marker.

4. Never invent a marker_key.

5. If a result cannot be confidently mapped to one of the
   provided marker definitions, place it in unmapped_results.

6. Preserve the test name from the report exactly as
   reported_name.

7. For numeric results:
   - numerical_value = numeric value
   - text_value = ""

8. For non-numeric results:
   - numerical_value = null
   - text_value = the reported result

9. Preserve the unit shown in the report.
   Do not convert units.

10. Do not use the laboratory's reference ranges as results.

11. Do not infer results that are not explicitly present
    in the report.

12. Format dates consistently:
    - report_date must use YYYY-MM-DD
    - collection_date must use YYYY-MM-DD
    - report_datetime must use YYYY-MM-DD HH:MM:SS

    Convert dates from the format shown in the report when necessary.

    Example:
    02/06/2025 → 2025-06-02
    02/06/2025 13:56:54 → 2025-06-02 13:56:54

13. If a metadata field is not available in the report,
    return an empty string.
    Do not guess or invent metadata.

14. file_name must be:
    {file_name}
"""

    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": file_name,
                        "file_data": (
                            f"data:application/pdf;base64,"
                            f"{pdf_base64}"
                        ),
                    },
                    {
                        "type": "input_text",
                        "text": instructions,
                    },
                ],
            }
        ],
        text_format=LabReportExtraction,
    )

    extraction = response.output_parsed

    if extraction is None:
        raise ValueError(
            "OpenAI did not return a valid lab report extraction"
        )

    return extraction