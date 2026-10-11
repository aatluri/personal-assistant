/*
SleepMetricsSection

Displays and updates the user's
Sleep Metrics.

Responsibilities:
- Display Sleep Metrics fields.
- Update the SleepMetrics state when values change.
- Keep the UI focused only on Sleep Metrics data.

The page state is owned by LogSleepMetrics.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { SleepMetrics } from "../../../types/SleepMetrics";


interface SleepMetricsSectionProps {

    sleepMetrics: SleepMetrics;

    setSleepMetrics: Dispatch<
        SetStateAction<SleepMetrics>
    >;

}


function SleepMetricsSection({

    sleepMetrics,
    setSleepMetrics,

}: SleepMetricsSectionProps) {


    /*
    Update a single Sleep Metrics field.
    */
    function updateSleepMetric(
        key: keyof SleepMetrics,
        value: string | number | "",
    ) {

        setSleepMetrics((previous) => ({

            ...previous,

            [key]: value,

        }));

    }


    return (

        <section>

            <div
                className="
                    grid
                    gap-6
                    md:grid-cols-2
                "
            >

                {/* Sleep Start Time */}
                <TextInput
                    label="Sleep Start Time"
                    id="sleepStartTime"
                    name="sleepStartTime"
                    type="datetime-local"
                    value={sleepMetrics.sleepStartTime}
                    onChange={(event) =>
                        updateSleepMetric(
                            "sleepStartTime",
                            event.target.value
                        )
                    }
                />

                {/* Sleep End Time */}
                <TextInput
                    label="Sleep End Time"
                    id="sleepEndTime"
                    name="sleepEndTime"
                    type="datetime-local"
                    value={sleepMetrics.sleepEndTime}
                    onChange={(event) =>
                        updateSleepMetric(
                            "sleepEndTime",
                            event.target.value
                        )
                    }
                />


                {/* Total Sleep Duration */}
                <div className="md:col-span-2">

                    <TextInput
                        label="Total Sleep Duration (hr)"
                        id="totalSleepDurationHr"
                        name="totalSleepDurationHr"
                        type="number"
                        min={0}
                        step={0.1}
                        value={sleepMetrics.totalSleepDurationHr}
                        onChange={(event) =>
                            updateSleepMetric(
                                "totalSleepDurationHr",
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value)
                            )
                        }
                    />

                </div>


                {/* Core Sleep */}
                <TextInput
                    label="Core Sleep (hr)"
                    id="coreSleepHr"
                    name="coreSleepHr"
                    type="number"
                    min={0}
                    step={0.1}
                    value={sleepMetrics.coreSleepHr}
                    onChange={(event) =>
                        updateSleepMetric(
                            "coreSleepHr",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Deep Sleep */}
                <TextInput
                    label="Deep Sleep (hr)"
                    id="deepSleepHr"
                    name="deepSleepHr"
                    type="number"
                    min={0}
                    step={0.1}
                    value={sleepMetrics.deepSleepHr}
                    onChange={(event) =>
                        updateSleepMetric(
                            "deepSleepHr",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Awake */}
                <TextInput
                    label="Awake (hr)"
                    id="awakeHr"
                    name="awakeHr"
                    type="number"
                    min={0}
                    step={0.1}
                    value={sleepMetrics.awakeHr}
                    onChange={(event) =>
                        updateSleepMetric(
                            "awakeHr",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* REM Sleep */}
                <TextInput
                    label="REM Sleep (hr)"
                    id="remSleepHr"
                    name="remSleepHr"
                    type="number"
                    min={0}
                    step={0.1}
                    value={sleepMetrics.remSleepHr}
                    onChange={(event) =>
                        updateSleepMetric(
                            "remSleepHr",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
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
                        value={sleepMetrics.source}
                        onChange={(event) =>
                            updateSleepMetric(
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

export default SleepMetricsSection;