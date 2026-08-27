import { describe, expect, test } from "vitest";

import { createEmptyBodyMeasurements } from "./createEmptyBodyMeasurements";

/*
    createEmptyBodyMeasurements Tests

    Each test follows the same sequence:

    1. Call the utility function.
    2. Verify that an empty BodyMeasurements
       object is returned.
*/

describe("createEmptyBodyMeasurements", () => {

    // Verify that all Body Measurements fields are initialized.
    test("creates empty Body Measurements", () => {

        const measurements =
            createEmptyBodyMeasurements();

        expect(measurements.bodyFat).toBe("");
        expect(measurements.neck).toBe("");
        expect(measurements.leftArm).toBe("");
        expect(measurements.rightCalf).toBe("");
        expect(measurements.notes).toBe("");

    });

});