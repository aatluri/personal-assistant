/*
    Creates a new empty Daily Log.

    Used when:
    1. The page first loads.
    2. No Daily Log exists for a date.
*/

import type { DailyLog } from "../types/DailyLog";

export function createEmptyDailyLog(): DailyLog {
    return {

        /* ------------------------------ */
        /* Workout                        */
        /* ------------------------------ */

        workout: {
            workoutType: "",
            workoutDuration: 0,
            workoutCalories: 0,
            workoutVolume: 0,
            workoutSets: 0,
            averageHeartRate: 0,
            workoutSummary: "",
        },

        /* ------------------------------ */
        /* Body                           */
        /* ------------------------------ */

        body: {
            weight: 0,
        },

        /* ------------------------------ */
        /* Activity                       */
        /* ------------------------------ */

        activity: {
            steps: 0,
            totalCaloriesBurnt: 0,
        },

        /* ------------------------------ */
        /* Meal Timing                    */
        /* ------------------------------ */

        mealTiming: {
            firstMealTime: "",
            lastMealTime: "",
        },

        /* ------------------------------ */
        /* Nutrition                      */
        /* ------------------------------ */

        nutrition: {
            breakfast: "",
            lunch: "",
            dinner: "",
            snacks: "",
            protein: 0,
            carbs: 0,
            fat: 0,
            fibre: 0,
            sugar: 0,
            caloriesConsumed: 0,
        },

        /* ------------------------------ */
        /* Hydration                      */
        /* ------------------------------ */

        hydration: {
            water: 0,
        },

        /* ------------------------------ */
        /* Sleep                          */
        /* ------------------------------ */

        sleep: {
            sleepStartTime: "",
            sleepEndTime: "",
        },

        /* ------------------------------ */
        /* Notes                          */
        /* ------------------------------ */

        notes: {
            notes: "",
        },

    };
}