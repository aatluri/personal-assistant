/*
WorkoutMetrics

Defines the structure of a Workout Metrics
object used throughout the frontend.

This interface represents a single workout
and is shared between:
- API layer
- Page components
- Utility functions
*/

export interface WorkoutMetrics {

    /*
    Workout date in YYYY-MM-DD format.
    */
    date: string;

    /*
    Type of workout.

    Examples:
    - HIIT
    - Running
    - Functional Strength Training
    */
    workoutType: string;

    /*
    Start and end time of the workout.

    Stored in the frontend as HH:mm.
    Example:
    06:30
    */
    workoutStartTime: string;
    workoutEndTime: string;

    /*
    Workout duration in HH:MM:SS format.

    Example:
    01:00:00
    */
    workoutDuration: string;

    /* ------------------------------ */
    /* Energy                         */
    /* ------------------------------ */

    totalEnergyKcal: number | "";
    activeEnergyKcal: number | "";

    /* ------------------------------ */
    /* Heart Rate                     */
    /* ------------------------------ */

    maxHeartRateBpm: number | "";
    avgHeartRateBpm: number | "";

    /* ------------------------------ */
    /* Distance / Speed               */
    /* ------------------------------ */

    distanceMi: number | "";
    avgSpeedMph: number | "";

}