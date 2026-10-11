/*
Workout Metrics API

Communication layer between the Workout Metrics
frontend and backend.
*/

import type { WorkoutMetrics } from "../types/WorkoutMetrics";


/*
Converts a time into the datetime format
expected by the backend.

Example:
08:30 -> 2026-08-14T08:30
*/
function buildDateTime(
    date: string,
    time: string
): string | null {

    if (!time) {
        return null;
    }

    return `${date}T${time}`;
}


/*
Converts an empty numeric field into null.
*/
function buildNumber(
    value: number | ""
): number | null {

    return value === "" ? null : value;
}


/*
Retrieves all Workout Metrics records
for a specific date.
*/
export async function getWorkoutMetricsByDate(
    date: string,
): Promise<WorkoutMetrics[]> {

    const response = await fetch(
        `http://localhost:8000/health/workout-metrics?workout_date=${encodeURIComponent(date)}`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load Workout Metrics"
        );
    }

    const workouts = await response.json();

    return workouts.map(
        (workout: any): WorkoutMetrics => ({

            date:
                workout.date,

            workoutType:
                workout.workout_type ?? "",

            workoutStartTime:
                workout.workout_start_time
                    ? workout.workout_start_time.substring(11, 19)
                    : "",

            workoutEndTime:
                workout.workout_end_time
                    ? workout.workout_end_time.substring(11, 19)
                    : "",

            workoutDuration:
                workout.workout_duration ?? "",

            totalEnergyKcal:
                workout.total_energy_kcal ?? "",

            activeEnergyKcal:
                workout.active_energy_kcal ?? "",

            maxHeartRateBpm:
                workout.max_heart_rate_bpm ?? "",

            avgHeartRateBpm:
                workout.avg_heart_rate_bpm ?? "",

            distanceMi:
                workout.distance_mi ?? "",

            avgSpeedMph:
                workout.avg_speed_mph ?? "",

        })
    );
}


/*
Saves a Workout Metrics record.

The backend performs an upsert using
Workout Start Time as the unique key.
*/
export async function saveWorkoutMetric(
    workoutMetric: WorkoutMetrics,
): Promise<void> {

    const workoutStartDateTime =
        buildDateTime(
            workoutMetric.date,
            workoutMetric.workoutStartTime,
        );

    const workoutEndDateTime =
        buildDateTime(
            workoutMetric.date,
            workoutMetric.workoutEndTime,
        );


    const request = {

        date:
            workoutMetric.date,

        workout_type:
            workoutMetric.workoutType,

        workout_start_time:
            workoutStartDateTime,

        workout_end_time:
            workoutEndDateTime,

        workout_duration:
            workoutMetric.workoutDuration,

        total_energy_kcal:
            buildNumber(
                workoutMetric.totalEnergyKcal
            ),

        active_energy_kcal:
            buildNumber(
                workoutMetric.activeEnergyKcal
            ),

        max_heart_rate_bpm:
            buildNumber(
                workoutMetric.maxHeartRateBpm
            ),

        avg_heart_rate_bpm:
            buildNumber(
                workoutMetric.avgHeartRateBpm
            ),

        distance_mi:
            buildNumber(
                workoutMetric.distanceMi
            ),

        avg_speed_mph:
            buildNumber(
                workoutMetric.avgSpeedMph
            ),
    };


    const response = await fetch(
        "http://localhost:8000/health/workout-metrics",
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

        throw new Error(
            "Failed to save Workout Metrics"
        );
    }
}