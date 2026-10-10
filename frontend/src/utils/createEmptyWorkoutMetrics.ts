/*
createEmptyWorkoutMetrics

Creates an empty WorkoutMetrics object.

Used when:
- Creating a new workout.
- No existing workout has been loaded.
- Resetting the Workout Metrics form.
*/

import type { WorkoutMetrics } from "../types/WorkoutMetrics";

export function createEmptyWorkoutMetrics(): WorkoutMetrics {

    return {

        date: "",

        workoutType: "",

        workoutStartTime: "",
        workoutEndTime: "",
        workoutDuration: "",

        totalEnergyKcal: "",
        activeEnergyKcal: "",

        maxHeartRateBpm: "",
        avgHeartRateBpm: "",

        distanceMi: "",
        avgSpeedMph: "",

    };

}