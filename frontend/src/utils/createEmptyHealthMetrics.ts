import type { HealthMetrics } from "../types/HealthMetrics";

export function createEmptyHealthMetrics(): HealthMetrics {
    return {
        date: "",

        stepCount: "",

        activeEnergyKcal: "",
        restingEnergyKcal: "",

        atrialFibrillationBurdenPercent: "",
        bloodOxygenSaturationPercent: "",
        breathingDisturbancesCount: "",

        cardioRecoveryBpm: "",
        flightsClimbed: "",

        heartRateMinBpm: "",
        heartRateMaxBpm: "",
        heartRateVariabilityMs: "",

        physicalEffortKcalHrKg: "",
        respiratoryRateBpm: "",
        restingHeartRateBpm: "",

        source: "",
    };
}