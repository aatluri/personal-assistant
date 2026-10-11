export interface HealthMetrics {
    date: string;

    stepCount: number | "";

    activeEnergyKcal: number | "";
    restingEnergyKcal: number | "";

    atrialFibrillationBurdenPercent: number | "";
    bloodOxygenSaturationPercent: number | "";
    breathingDisturbancesCount: number | "";

    cardioRecoveryBpm: number | "";
    flightsClimbed: number | "";

    heartRateMinBpm: number | "";
    heartRateMaxBpm: number | "";
    heartRateVariabilityMs: number | "";

    physicalEffortKcalHrKg: number | "";
    respiratoryRateBpm: number | "";
    restingHeartRateBpm: number | "";

    source: string;
}