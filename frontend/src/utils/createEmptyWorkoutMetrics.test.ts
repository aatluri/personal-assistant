import { describe, expect, test } from "vitest";

import { createEmptyWorkoutMetrics } from "./createEmptyWorkoutMetrics";


describe("createEmptyWorkoutMetrics", () => {

    // Verify that all Workout Metrics fields are initialized.
    test("creates empty Workout Metrics", () => {

        const workoutMetrics =
            createEmptyWorkoutMetrics();

        expect(workoutMetrics.date).toBe("");

        expect(workoutMetrics.workoutType).toBe("");

        expect(workoutMetrics.workoutStartTime).toBe("");
        expect(workoutMetrics.workoutEndTime).toBe("");
        expect(workoutMetrics.workoutDuration).toBe("");

        expect(workoutMetrics.totalEnergyKcal).toBe("");
        expect(workoutMetrics.activeEnergyKcal).toBe("");

        expect(workoutMetrics.maxHeartRateBpm).toBe("");
        expect(workoutMetrics.avgHeartRateBpm).toBe("");

        expect(workoutMetrics.distanceMi).toBe("");
        expect(workoutMetrics.avgSpeedMph).toBe("");

    });

});