import type {
    Dispatch,
    SetStateAction,
} from "react";

import type { WorkoutMetrics } from "../../../types/WorkoutMetrics";

import TextInput from "../../../components/TextInput";


interface WorkoutMetricsSectionProps {
    workoutMetrics: WorkoutMetrics;

    setWorkoutMetrics: Dispatch<
        SetStateAction<WorkoutMetrics>
    >;
}


export default function WorkoutMetricsSection({
    workoutMetrics,
    setWorkoutMetrics,
}: WorkoutMetricsSectionProps) {

    function updateText(
        key: keyof WorkoutMetrics,
        value: string,
    ) {
        setWorkoutMetrics((previous) => ({
            ...previous,
            [key]: value,
        }));
    }


    function updateNumber(
        key: keyof WorkoutMetrics,
        value: number | "",
    ) {
        setWorkoutMetrics((previous) => ({
            ...previous,
            [key]: value,
        }));
    }


    return (
        <div className="grid gap-6 md:grid-cols-2">

            <TextInput
                label="Workout Type"
                value={workoutMetrics.workoutType}
                onChange={(e) =>
                    updateText(
                        "workoutType",
                        e.target.value,
                    )
                }
            />

            <TextInput
                label="Workout Start Time"
                value={workoutMetrics.workoutStartTime}
                onChange={(e) =>
                    updateText(
                        "workoutStartTime",
                        e.target.value,
                    )
                }
            />

            <TextInput
                label="Workout End Time"
                value={workoutMetrics.workoutEndTime}
                onChange={(e) =>
                    updateText(
                        "workoutEndTime",
                        e.target.value,
                    )
                }
            />

            <TextInput
                label="Workout Duration"
                value={workoutMetrics.workoutDuration}
                onChange={(e) =>
                    updateText(
                        "workoutDuration",
                        e.target.value,
                    )
                }
            />

            <TextInput
                label="Total Energy (kcal)"
                value={workoutMetrics.totalEnergyKcal}
                onChange={(e) =>
                    updateNumber(
                        "totalEnergyKcal",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

            <TextInput
                label="Active Energy (kcal)"
                value={workoutMetrics.activeEnergyKcal}
                onChange={(e) =>
                    updateNumber(
                        "activeEnergyKcal",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

            <TextInput
                label="Max Heart Rate (bpm)"
                value={workoutMetrics.maxHeartRateBpm}
                onChange={(e) =>
                    updateNumber(
                        "maxHeartRateBpm",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

            <TextInput
                label="Average Heart Rate (bpm)"
                value={workoutMetrics.avgHeartRateBpm}
                onChange={(e) =>
                    updateNumber(
                        "avgHeartRateBpm",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

            <TextInput
                label="Distance (mi)"
                value={workoutMetrics.distanceMi}
                onChange={(e) =>
                    updateNumber(
                        "distanceMi",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

            <TextInput
                label="Average Speed (mi/hr)"
                value={workoutMetrics.avgSpeedMph}
                onChange={(e) =>
                    updateNumber(
                        "avgSpeedMph",
                        e.target.value === ""
                            ? ""
                            : Number(e.target.value),
                    )
                }
            />

        </div>
    );
}