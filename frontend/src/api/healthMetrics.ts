import type { HealthMetrics } from "../types/HealthMetrics";


/*
Convert an optional frontend number into the value
expected by the backend.

Empty fields are stored as null.
*/
function buildNumber(
    value: number | ""
): number | null {
    return value === "" ? null : value;
}


/*
Retrieve Health Metrics for a specific date.

Returns null when no Health Metrics record exists
for the selected date.
*/
export async function getHealthMetric(
    date: string,
): Promise<HealthMetrics | null> {

    const response = await fetch(
        `http://localhost:8000/health/health-metrics/${date}`
    );

    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error("Failed to load Health Metrics");
    }

    const apiResponse = await response.json();

    const healthMetrics: HealthMetrics = {
        date: apiResponse.date,

        stepCount: apiResponse.step_count ?? "",

        activeEnergyKcal: apiResponse.active_energy_kcal ?? "",
        restingEnergyKcal: apiResponse.resting_energy_kcal ?? "",

        atrialFibrillationBurdenPercent:
            apiResponse.atrial_fibrillation_burden_percent ?? "",

        bloodOxygenSaturationPercent:
            apiResponse.blood_oxygen_saturation_percent ?? "",

        breathingDisturbancesCount:
            apiResponse.breathing_disturbances_count ?? "",

        cardioRecoveryBpm:
            apiResponse.cardio_recovery_bpm ?? "",

        flightsClimbed:
            apiResponse.flights_climbed ?? "",

        heartRateMinBpm:
            apiResponse.heart_rate_min_bpm ?? "",

        heartRateMaxBpm:
            apiResponse.heart_rate_max_bpm ?? "",

        heartRateVariabilityMs:
            apiResponse.heart_rate_variability_ms ?? "",

        physicalEffortKcalHrKg:
            apiResponse.physical_effort_kcal_hr_kg ?? "",

        respiratoryRateBpm:
            apiResponse.respiratory_rate_bpm ?? "",

        restingHeartRateBpm:
            apiResponse.resting_heart_rate_bpm ?? "",

        source: apiResponse.source ?? "",
    };

    return healthMetrics;
}


/*
Save Health Metrics for the selected date.

PUT is used because the backend endpoint performs
an upsert:
- create the record if it does not exist
- update it if it already exists
*/
export async function saveHealthMetric(
    selectedDate: string,
    healthMetrics: HealthMetrics,
): Promise<void> {

    const request = {
        date: selectedDate,

        step_count:
            buildNumber(healthMetrics.stepCount),

        active_energy_kcal:
            buildNumber(healthMetrics.activeEnergyKcal),

        resting_energy_kcal:
            buildNumber(healthMetrics.restingEnergyKcal),

        atrial_fibrillation_burden_percent:
            buildNumber(
                healthMetrics.atrialFibrillationBurdenPercent
            ),

        blood_oxygen_saturation_percent:
            buildNumber(
                healthMetrics.bloodOxygenSaturationPercent
            ),

        breathing_disturbances_count:
            buildNumber(
                healthMetrics.breathingDisturbancesCount
            ),

        cardio_recovery_bpm:
            buildNumber(healthMetrics.cardioRecoveryBpm),

        flights_climbed:
            buildNumber(healthMetrics.flightsClimbed),

        heart_rate_min_bpm:
            buildNumber(healthMetrics.heartRateMinBpm),

        heart_rate_max_bpm:
            buildNumber(healthMetrics.heartRateMaxBpm),

        heart_rate_variability_ms:
            buildNumber(healthMetrics.heartRateVariabilityMs),

        physical_effort_kcal_hr_kg:
            buildNumber(healthMetrics.physicalEffortKcalHrKg),

        respiratory_rate_bpm:
            buildNumber(healthMetrics.respiratoryRateBpm),

        resting_heart_rate_bpm:
            buildNumber(healthMetrics.restingHeartRateBpm),

        source:
            healthMetrics.source || null,
    };


    const response = await fetch(
        "http://localhost:8000/health/health-metrics",
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        }
    );


    if (!response.ok) {
        const error = await response.text();

        console.error(error);

        throw new Error("Failed to save Health Metrics");
    }
}