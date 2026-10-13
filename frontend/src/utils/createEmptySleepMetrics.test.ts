import { describe, expect, test } from "vitest";

import { createEmptySleepMetrics } from "./createEmptySleepMetrics";


describe("createEmptySleepMetrics", () => {

    // Verify that all Sleep Metrics fields are initialized.
    test("creates empty Sleep Metrics", () => {

        const sleepMetrics =
            createEmptySleepMetrics();

        expect(sleepMetrics.date).toBe("");

        expect(sleepMetrics.sleepStartTime).toBe("");
        expect(sleepMetrics.sleepEndTime).toBe("");

        expect(
            sleepMetrics.totalSleepDurationHr
        ).toBe("");

        expect(sleepMetrics.coreSleepHr).toBe("");
        expect(sleepMetrics.deepSleepHr).toBe("");

        expect(sleepMetrics.awakeHr).toBe("");
        expect(sleepMetrics.remSleepHr).toBe("");

        expect(sleepMetrics.source).toBe("");

    });

});