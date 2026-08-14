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

            {/* Section Heading */}
            <h2>Workout</h2>

            {/* Workout Type */}
            <Select
                label="Workout Type"
                id="workout-type"
                name="workoutType"
                value={dailyLog.workout.workoutType}
                onChange={(event) => {
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutType: event.target.value,
                    }));
                }}
            >
                <option value="HIIT">HIIT</option>
                <option value="Strength">Strength</option>
                <option value="Cardio">Cardio</option>
                <option value="Mobility">Mobility</option>
                <option value="Rest">Rest</option>
            </Select>

            {/* Workout Duration */}
            <TextInput
                label="Duration (minutes)"
                id="workout-duration"
                name="workoutDuration"
                type="number"
                min={0}
                value={dailyLog.workout.workoutDuration}
                onChange={(event) => {
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutDuration: Number(event.target.value),
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
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutCalories: Number(event.target.value),
                    }));
                }}
            />

            {/* Workout Volume */}
            <TextInput
                label="Volume (kg)"
                id="workout-volume"
                name="workoutVolume"
                type="number"
                min={0}
                value={dailyLog.workout.workoutVolume}
                onChange={(event) => {
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutVolume: Number(event.target.value),
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
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutSets: Number(event.target.value),
                    }));
                }}
            />

            {/* Average Heart Rate */}
            <TextInput
                label="Average Heart Rate (bpm)"
                id="average-heart-rate"
                name="averageHeartRate"
                type="number"
                min={0}
                value={dailyLog.workout.averageHeartRate}
                onChange={(event) => {
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        averageHeartRate: Number(event.target.value),
                    }));
                }}
            />

            {/* Workout Summary */}
            <TextArea
                label="Workout Summary"
                id="workout-summary"
                name="workoutSummary"
                rows={8}
                value={dailyLog.workout.workoutSummary}
                onChange={(event) => {
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        workoutSummary: event.target.value,
                    }));
                }}
            />

        </section>
    );
}

export default WorkoutSection;