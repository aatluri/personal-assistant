/*
WorkoutMetricsSection
---------------------

This component is the editable form for ONE workout.

It does not load data, save data, or own the workout state.
Those responsibilities belong to LogWorkoutMetrics.

The parent passes two props:

    workoutMetrics
        The currently selected WorkoutMetrics object.

    setWorkoutMetrics
        A state-update function supplied by the parent.


CONTROLLED INPUTS

Every TextInput is a controlled input.

For example:

    value={workoutMetrics.workoutType}

means the displayed value always comes from the
workoutMetrics object supplied by the parent.

When the user types something, the component does not
directly modify workoutMetrics.

Instead it calls setWorkoutMetrics with an updater function:

    setWorkoutMetrics((previous) => ({
        ...previous,
        workoutType: newValue,
    }));

The spread:

    ...previous

copies all existing WorkoutMetrics fields.

We then replace only the field that changed.

For example, changing workoutType keeps start time,
duration, calories, heart rate, etc. unchanged.


PARENT / CHILD STATE FLOW

The state flow is:

    LogWorkoutMetrics
            |
            | selectedWorkout
            v
    WorkoutMetricsSection
            |
            | user edits a field
            v
    setWorkoutMetrics(...)
            |
            v
    LogWorkoutMetrics updates selectedWorkout
            |
            v
    React re-renders WorkoutMetricsSection
            |
            v
    input displays the new value

This is called "lifting state up".

WorkoutMetricsSection displays and edits the data, but the
actual state remains owned by LogWorkoutMetrics.


TEXT FIELD UPDATES

Text-based fields use updateText.

These include fields such as:

    workoutType
    workoutStartTime
    workoutEndTime
    workoutDuration

updateText receives:

    field
    value

and creates a new WorkoutMetrics object with only that
field changed.


NUMERIC FIELD UPDATES

Numeric fields use updateNumber.

These include:

    totalEnergyKcal
    activeEnergyKcal
    maxHeartRateBpm
    avgHeartRateBpm
    distanceMi
    avgSpeedMph

The WorkoutMetrics type allows these values to be:

    number | ""

The empty string is useful because an HTML input needs to
be able to represent an empty field.

Therefore updateNumber converts:

    ""

to:

    ""

and converts a value such as:

    "650"

to:

    650

This means the UI can display an empty field while populated
numeric values remain numbers in our application state.


WHY THIS COMPONENT DOES NOT MANAGE isDirty

WorkoutMetricsSection does not need to know whether the page
has unsaved changes.

It simply reports changes through setWorkoutMetrics.

LogWorkoutMetrics wraps that update function and also does:

    setIsDirty(true);
    setSaveStatus("idle");

Therefore every field change automatically marks the page
as having unsaved changes without WorkoutMetricsSection
needing to understand save behaviour.


WHY id AND name ARE PROVIDED

Each TextInput has an id and name.

The id allows the input's label to be correctly associated
with the underlying HTML input.

This improves accessibility and also allows tests to locate
fields using:

    screen.getByLabelText(...)

The name identifies the field represented by the input.


COMPONENT RESPONSIBILITY

WorkoutMetricsSection should remain focused on:

    WorkoutMetrics data
            ↓
    displaying form fields
            ↓
    converting user input
            ↓
    requesting state updates

It should NOT contain:

    - API calls
    - backend logic
    - date loading
    - save logic
    - dirty-state logic
    - workout-list management

Those responsibilities remain in LogWorkoutMetrics.
*/

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
                id="workoutType"
                name="workoutType"
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
                id="workoutStartTime"
                name="workoutStartTime"
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
                id="workoutEndTime"
                name="workoutEndTime"
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
                id="workoutDuration"
                name="workoutDuration"
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
                id="totalEnergyKcal"
                name="totalEnergyKcal"
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
                id="activeEnergyKcal"
                name="activeEnergyKcal"
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
                id="maxHeartRateBpm"
                name="maxHeartRateBpm"
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
                id="avgHeartRateBpm"
                name="avgHeartRateBpm"
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
                id="distanceMi"
                name="distanceMi"
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
                id="avgSpeedMph"
                name="avgSpeedMph"
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