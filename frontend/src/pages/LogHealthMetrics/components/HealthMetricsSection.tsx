/*
HealthMetricsSection

Displays and updates the user's Health Metrics.

The page owns the state. This component is
responsible only for rendering and updating fields.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { HealthMetrics } from "../../../types/HealthMetrics";


interface HealthMetricsSectionProps {
    healthMetrics: HealthMetrics;

    setHealthMetrics: Dispatch<
        SetStateAction<HealthMetrics>
    >;
}


function HealthMetricsSection({
    healthMetrics,
    setHealthMetrics,
}: HealthMetricsSectionProps) {


    /*
    Update a single Health Metrics field.
    */
    function updateHealthMetric(
        key: keyof HealthMetrics,
        value: string | number | "",
    ) {

        setHealthMetrics((previous) => ({
            ...previous,
            [key]: value,
        }));

    }


    /*
    Convert the value from a numeric input.

    Empty inputs remain empty strings so the UI
    can represent fields that have no value.
    */
    function numericValue(value: string): number | "" {
        return value === "" ? "" : Number(value);
    }


    return (

        <section>

            <div className="grid gap-6 md:grid-cols-2">


                {/* Activity */}

                <TextInput
                    label="Step Count"
                    id="stepCount"
                    name="stepCount"
                    type="number"
                    min={0}
                    step={1}
                    value={healthMetrics.stepCount}
                    onChange={(event) =>
                        updateHealthMetric(
                            "stepCount",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Flights Climbed"
                    id="flightsClimbed"
                    name="flightsClimbed"
                    type="number"
                    min={0}
                    step={1}
                    value={healthMetrics.flightsClimbed}
                    onChange={(event) =>
                        updateHealthMetric(
                            "flightsClimbed",
                            numericValue(event.target.value)
                        )
                    }
                />


                {/* Energy */}

                <TextInput
                    label="Active Energy (kcal)"
                    id="activeEnergyKcal"
                    name="activeEnergyKcal"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.activeEnergyKcal}
                    onChange={(event) =>
                        updateHealthMetric(
                            "activeEnergyKcal",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Resting Energy (kcal)"
                    id="restingEnergyKcal"
                    name="restingEnergyKcal"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.restingEnergyKcal}
                    onChange={(event) =>
                        updateHealthMetric(
                            "restingEnergyKcal",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Physical Effort (kcal/hr·kg)"
                    id="physicalEffortKcalHrKg"
                    name="physicalEffortKcalHrKg"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.physicalEffortKcalHrKg}
                    onChange={(event) =>
                        updateHealthMetric(
                            "physicalEffortKcalHrKg",
                            numericValue(event.target.value)
                        )
                    }
                />

                <div />


                {/* Heart */}

                <TextInput
                    label="Heart Rate Min (bpm)"
                    id="heartRateMinBpm"
                    name="heartRateMinBpm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.heartRateMinBpm}
                    onChange={(event) =>
                        updateHealthMetric(
                            "heartRateMinBpm",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Heart Rate Max (bpm)"
                    id="heartRateMaxBpm"
                    name="heartRateMaxBpm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.heartRateMaxBpm}
                    onChange={(event) =>
                        updateHealthMetric(
                            "heartRateMaxBpm",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Resting Heart Rate (bpm)"
                    id="restingHeartRateBpm"
                    name="restingHeartRateBpm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.restingHeartRateBpm}
                    onChange={(event) =>
                        updateHealthMetric(
                            "restingHeartRateBpm",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Heart Rate Variability (ms)"
                    id="heartRateVariabilityMs"
                    name="heartRateVariabilityMs"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.heartRateVariabilityMs}
                    onChange={(event) =>
                        updateHealthMetric(
                            "heartRateVariabilityMs",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Cardio Recovery (bpm)"
                    id="cardioRecoveryBpm"
                    name="cardioRecoveryBpm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.cardioRecoveryBpm}
                    onChange={(event) =>
                        updateHealthMetric(
                            "cardioRecoveryBpm",
                            numericValue(event.target.value)
                        )
                    }
                />

                <div />


                {/* Respiratory / Cardiovascular */}

                <TextInput
                    label="Blood Oxygen Saturation (%)"
                    id="bloodOxygenSaturationPercent"
                    name="bloodOxygenSaturationPercent"
                    type="number"
                    min={0}
                    max={100}
                    step={0.1}
                    value={healthMetrics.bloodOxygenSaturationPercent}
                    onChange={(event) =>
                        updateHealthMetric(
                            "bloodOxygenSaturationPercent",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Respiratory Rate (breaths/min)"
                    id="respiratoryRateBpm"
                    name="respiratoryRateBpm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.respiratoryRateBpm}
                    onChange={(event) =>
                        updateHealthMetric(
                            "respiratoryRateBpm",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Breathing Disturbances"
                    id="breathingDisturbancesCount"
                    name="breathingDisturbancesCount"
                    type="number"
                    min={0}
                    step={0.1}
                    value={healthMetrics.breathingDisturbancesCount}
                    onChange={(event) =>
                        updateHealthMetric(
                            "breathingDisturbancesCount",
                            numericValue(event.target.value)
                        )
                    }
                />

                <TextInput
                    label="Atrial Fibrillation Burden (%)"
                    id="atrialFibrillationBurdenPercent"
                    name="atrialFibrillationBurdenPercent"
                    type="number"
                    min={0}
                    max={100}
                    step={0.1}
                    value={healthMetrics.atrialFibrillationBurdenPercent}
                    onChange={(event) =>
                        updateHealthMetric(
                            "atrialFibrillationBurdenPercent",
                            numericValue(event.target.value)
                        )
                    }
                />


                {/* Source */}

                <div className="md:col-span-2">

                    <TextInput
                        label="Source"
                        id="source"
                        name="source"
                        type="text"
                        value={healthMetrics.source}
                        onChange={(event) =>
                            updateHealthMetric(
                                "source",
                                event.target.value
                            )
                        }
                    />

                </div>

            </div>

        </section>

    );

}

export default HealthMetricsSection;