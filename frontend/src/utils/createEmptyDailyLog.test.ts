import { describe, expect, test } from "vitest";

import { createEmptyDailyLog } from "./createEmptyDailyLog";

/*
    createEmptyDailyLog Tests

    Each test follows the same sequence:

    1. Call the utility function.
    2. Verify that an empty DailyLog
       object is returned.
*/

describe("createEmptyDailyLog", () => {

    // Verify that all Daily Log sections are created.
    test("creates empty Daily Log", () => {

        const dailyLog = createEmptyDailyLog();

        expect(dailyLog.workout.workoutType).toBe("");
        expect(dailyLog.body.weight).toBe("");
        expect(dailyLog.activity.steps).toBe("");
        expect(dailyLog.hydration.water).toBe("");
        expect(dailyLog.notes.notes).toBe("");

    });

});