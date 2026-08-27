import { describe, expect, test } from "vitest";

import { calculateSleepDuration } from "./calculateSleepDuration";

/*
    calculateSleepDuration Tests

    Each test follows the same sequence:

    1. Call the utility function.
    2. Pass known input values.
    3. Verify that the returned value
       matches the expected result.
*/

describe("calculateSleepDuration", () => {

    // Verify that the correct duration is calculated.
    test("calculates duration", () => {

        expect(
            calculateSleepDuration(
                "22:00",
                "06:00",
            )
        ).toBe("8h 0m");

    });

    // Verify that sleep crossing midnight is handled correctly.
    test("supports midnight", () => {

        expect(
            calculateSleepDuration(
                "23:30",
                "07:15",
            )
        ).toBe("7h 45m");

    });

    // Verify that a missing start time returns "-".
    test("missing start time", () => {

        expect(
            calculateSleepDuration(
                "",
                "07:00",
            )
        ).toBe("-");

    });

    // Verify that a missing end time returns "-".
    test("missing end time", () => {

        expect(
            calculateSleepDuration(
                "22:00",
                "",
            )
        ).toBe("-");

    });

    // Verify that both missing values return "-".
    test("missing both values", () => {

        expect(
            calculateSleepDuration(
                "",
                "",
            )
        ).toBe("-");

    });

});