import { describe, expect, test } from "vitest";

import { createEmptyHealthMetrics } from "./createEmptyHealthMetrics";


describe("createEmptyHealthMetrics", () => {

    // Verify that all Health Metrics fields are initialized.
    test("creates empty Health Metrics", () => {

        const healthMetrics =
            createEmptyHealthMetrics();

        expect(healthMetrics.date).toBe("");

        expect(healthMetrics.stepCount).toBe("");

        expect(healthMetrics.activeEnergyKcal).toBe("");
        expect(healthMetrics.restingEnergyKcal).toBe("");

        expect(
            healthMetrics.atrialFibrillationBurdenPercent
        ).toBe("");

        expect(
            healthMetrics.bloodOxygenSaturationPercent
        ).toBe("");

        expect(
            healthMetrics.breathingDisturbancesCount
        ).toBe("");

        expect(
            healthMetrics.cardioRecoveryBpm
        ).toBe("");

        expect(
            healthMetrics.flightsClimbed
        ).toBe("");

        expect(
            healthMetrics.heartRateMinBpm
        ).toBe("");

        expect(
            healthMetrics.heartRateMaxBpm
        ).toBe("");

        expect(
            healthMetrics.heartRateVariabilityMs
        ).toBe("");

        expect(
            healthMetrics.physicalEffortKcalHrKg
        ).toBe("");

        expect(
            healthMetrics.respiratoryRateBpm
        ).toBe("");

        expect(
            healthMetrics.restingHeartRateBpm
        ).toBe("");

        expect(
            healthMetrics.source
        ).toBe("");

    });

});