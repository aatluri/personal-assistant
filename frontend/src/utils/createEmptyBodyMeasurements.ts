/*
    Creates a new empty Body Measurements record.

    Used when:
    1. The page first loads.
    2. No Body Measurements exist for a date.
*/

import type { BodyMeasurements } from "../types/BodyMeasurements";

export function createEmptyBodyMeasurements(): BodyMeasurements {

    return {

        date: "",

        /* ------------------------------ */
        /* Body Composition               */
        /* ------------------------------ */

        bodyFat: "",
        muscleMass: "",
        visceralFat: "",

        /* ------------------------------ */
        /* Measurements                   */
        /* ------------------------------ */

        neck: "",
        chest: "",
        waist: "",
        stomach: "",
        hips: "",

        leftArm: "",
        rightArm: "",

        leftForearm: "",
        rightForearm: "",

        leftThigh: "",
        rightThigh: "",

        leftCalf: "",
        rightCalf: "",

        /* ------------------------------ */
        /* Notes                          */
        /* ------------------------------ */

        notes: "",

    };

}