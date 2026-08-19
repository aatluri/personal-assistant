/*
    WorkoutSection

    Displays and updates the workout-related
    fields from the shared DailyLog state.

    The actual state is owned by LogToday.
    This component only reads values from dailyLog
    and updates them through setDailyLog.
*/

import type { Dispatch, SetStateAction } from "react";

import Select from "../../../components/Select";
import TextArea from "../../../components/TextArea";
import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent LogToday component.
*/
interface WorkoutSectionProps {
    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log state
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;
}

function WorkoutSection({
    dailyLog,
    setDailyLog,
}: WorkoutSectionProps) {

    return (
        <section>

            <div
                className="
                    space-y-6
                "
            >

                {/* Workout Type */}
                <Select
                    label="Workout Type"
                    id="workout-type"
                    name="workoutType"
                    value={dailyLog.workout.workoutType}
                    onChange={(event) => {
                        const newWorkoutType = event.target.value;

                        setDailyLog((previousDailyLog) => ({
                            ...previousDailyLog,
                            workout: {
                                ...previousDailyLog.workout,
                                workoutType: newWorkoutType,
                            },
                        }));
                    }}
                >
                    <option value="HIIT">HIIT</option>
                    <option value="Strength">Strength</option>
                    <option value="Cardio">Cardio</option>
                    <option value="Mobility">Mobility</option>
                    <option value="Rest">Rest</option>
                </Select>

                <div
                    className="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-4
                    "
                >

                    {/* Workout Duration */}
                    <TextInput
                        label="Duration (minutes)"
                        id="workout-duration"
                        name="workoutDuration"
                        type="number"
                        min={0}
                        value={dailyLog.workout.workoutDuration}
                        onChange={(event) => {
                            const newWorkoutDuration =
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value);

                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                workout: {
                                    ...previousDailyLog.workout,
                                    workoutDuration: newWorkoutDuration,
                                },
                            }));
                        }}
                    />

                    {/* Calories Burnt */}
                    <TextInput
                        label="Calories Burnt"
                        id="workout-calories"
                        name="workoutCalories"
                        type="number"
                        min={0}
                        value={dailyLog.workout.workoutCalories}
                        onChange={(event) => {
                            const newWorkoutCalories =
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value);

                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                workout: {
                                    ...previousDailyLog.workout,
                                    workoutCalories: newWorkoutCalories,
                                },
                            }));
                        }}
                    />

                </div>

                <div
                    className="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-4
                    "
                >

                    {/* Workout Volume */}
                    <TextInput
                        label="Volume (kg)"
                        id="workout-volume"
                        name="workoutVolume"
                        type="number"
                        min={0}
                        value={dailyLog.workout.workoutVolume}
                        onChange={(event) => {
                            const newWorkoutVolume =
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value);

                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                workout: {
                                    ...previousDailyLog.workout,
                                    workoutVolume: newWorkoutVolume,
                                },
                            }));
                        }}
                    />

                    {/* Number of Sets */}
                    <TextInput
                        label="Sets"
                        id="workout-sets"
                        name="workoutSets"
                        type="number"
                        min={0}
                        value={dailyLog.workout.workoutSets}
                        onChange={(event) => {
                            const newWorkoutSets =
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value);

                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                workout: {
                                    ...previousDailyLog.workout,
                                    workoutSets: newWorkoutSets,
                                },
                            }));
                        }}
                    />

                </div>

                {/* Average Heart Rate */}
                <div className="md:w-1/2">
                    <TextInput
                        label="Average Heart Rate (bpm)"
                        id="average-heart-rate"
                        name="averageHeartRate"
                        type="number"
                        min={0}
                        value={dailyLog.workout.averageHeartRate}
                        onChange={(event) => {
                            const newAverageHeartRate =
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value);

                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                workout: {
                                    ...previousDailyLog.workout,
                                    averageHeartRate: newAverageHeartRate,
                                },
                            }));
                        }}
                    />
                </div>

                {/* Workout Summary */}
                <TextArea
                    label="Workout Summary"
                    id="workout-summary"
                    name="workoutSummary"
                    rows={8}
                    value={dailyLog.workout.workoutSummary}
                    onChange={(event) => {
                        const newWorkoutSummary = event.target.value;

                        setDailyLog((previousDailyLog) => ({
                            ...previousDailyLog,
                            workout: {
                                ...previousDailyLog.workout,
                                workoutSummary: newWorkoutSummary,
                            },
                        }));
                    }}
                />

            </div>

        </section>
    );
}

export default WorkoutSection;