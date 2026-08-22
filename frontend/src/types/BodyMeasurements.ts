/*
    BodyMeasurements

    Defines the structure of all data stored
    for the Body Measurements page.
*/

export interface BodyMeasurements {

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