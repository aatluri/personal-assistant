/*
    BodyMeasurements

    Defines the structure of the Body Measurements
    object used throughout the frontend.

    This interface represents the page state and is
    shared between:
    - API layer
    - Page components
    - Utility functions
*/

export interface BodyMeasurements {
    /*
        Measurement date in YYYY-MM-DD format.
    */

    date: string;

    /* ------------------------------ */
    /* Body Composition               */
    /* ------------------------------ */

    bodyFat: number | "";
    muscleMass: number | "";
    visceralFat: number | "";

    /* ------------------------------ */
    /* Measurements                   */
    /* ------------------------------ */

    neck: number | "";
    chest: number | "";
    waist: number | "";
    stomach: number | "";
    hips: number | "";

    leftArm: number | "";
    rightArm: number | "";

    leftForearm: number | "";
    rightForearm: number | "";

    leftThigh: number | "";
    rightThigh: number | "";

    leftCalf: number | "";
    rightCalf: number | "";

    /* ------------------------------ */
    /* Notes                          */
    /* ------------------------------ */

    notes: string;

}