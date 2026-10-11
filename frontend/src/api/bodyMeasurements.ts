/*
Body Measurements API

Communication layer between the Body Measurements
frontend and backend.

Responsibilities:
- Send HTTP requests to the backend.
- Convert backend API models into frontend models.
- Convert frontend models into backend request models.
*/

import type { BodyMeasurements } from "../types/BodyMeasurements";


/*
Converts an empty numeric field into null
before sending it to the backend.
*/
function buildNumber(
    value: number | ""
): number | null {
    return value === "" ? null : value;
}


/*
Retrieves the Body Measurements for the specified date.

Returns null if no record exists.
*/
export async function getBodyMeasurement(
    date: string
): Promise<BodyMeasurements | null> {

    const response = await fetch(
        `http://localhost:8000/health/body-measurements/${date}`
    );

    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error(
            "Failed to load Body Measurements"
        );
    }

    const apiResponse = await response.json();


    /*
    Convert the backend API model into
    the frontend BodyMeasurements model.
    */
    const bodyMeasurements: BodyMeasurements = {

        date,

        weight:
            apiResponse.weight_kg ?? "",

        bodyMassIndex:
            apiResponse.body_mass_index ?? "",

        bodyFat:
            apiResponse.body_fat_percent ?? "",

        muscleMass:
            apiResponse.muscle_mass_percent ?? "",

        visceralFat:
            apiResponse.visceral_fat ?? "",


        neck:
            apiResponse.neck_cm ?? "",

        chest:
            apiResponse.chest_cm ?? "",

        waist:
            apiResponse.waist_cm ?? "",

        stomach:
            apiResponse.stomach_cm ?? "",

        hips:
            apiResponse.hips_cm ?? "",


        leftArm:
            apiResponse.left_arm_cm ?? "",

        rightArm:
            apiResponse.right_arm_cm ?? "",


        leftForearm:
            apiResponse.left_forearm_cm ?? "",

        rightForearm:
            apiResponse.right_forearm_cm ?? "",


        leftThigh:
            apiResponse.left_thigh_cm ?? "",

        rightThigh:
            apiResponse.right_thigh_cm ?? "",


        leftCalf:
            apiResponse.left_calf_cm ?? "",

        rightCalf:
            apiResponse.right_calf_cm ?? "",


        notes:
            apiResponse.notes ?? "",
    };

    return bodyMeasurements;
}


/*
Saves Body Measurements.

Workflow:
1. Convert the frontend model into the backend API model.
2. Send a PUT request.
3. Throw an error if the save fails.
*/
export async function saveBodyMeasurement(
    selectedDate: string,
    bodyMeasurement: BodyMeasurements,
): Promise<void> {

    const request = {

        date:
            selectedDate,

        weight_kg:
            buildNumber(bodyMeasurement.weight),

        body_mass_index:
            buildNumber(bodyMeasurement.bodyMassIndex),

        body_fat_percent:
            buildNumber(bodyMeasurement.bodyFat),

        muscle_mass_percent:
            buildNumber(bodyMeasurement.muscleMass),

        visceral_fat:
            buildNumber(bodyMeasurement.visceralFat),


        neck_cm:
            buildNumber(bodyMeasurement.neck),

        chest_cm:
            buildNumber(bodyMeasurement.chest),

        waist_cm:
            buildNumber(bodyMeasurement.waist),

        stomach_cm:
            buildNumber(bodyMeasurement.stomach),

        hips_cm:
            buildNumber(bodyMeasurement.hips),


        left_arm_cm:
            buildNumber(bodyMeasurement.leftArm),

        right_arm_cm:
            buildNumber(bodyMeasurement.rightArm),


        left_forearm_cm:
            buildNumber(bodyMeasurement.leftForearm),

        right_forearm_cm:
            buildNumber(bodyMeasurement.rightForearm),


        left_thigh_cm:
            buildNumber(bodyMeasurement.leftThigh),

        right_thigh_cm:
            buildNumber(bodyMeasurement.rightThigh),


        left_calf_cm:
            buildNumber(bodyMeasurement.leftCalf),

        right_calf_cm:
            buildNumber(bodyMeasurement.rightCalf),


        notes:
            bodyMeasurement.notes,
    };


    const response = await fetch(
        "http://localhost:8000/health/body-measurements",
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(request),
        }
    );


    if (!response.ok) {

        const error = await response.text();

        console.error(error);

        throw new Error(
            "Failed to save Body Measurements"
        );
    }
}