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
            workoutDuration: "",
            workoutCalories: "",
            workoutVolume: "",
            workoutSets: "",
            averageHeartRate: "",
            workoutSummary: "",
        },

        /* ------------------------------ */
        /* Body                           */
        /* ------------------------------ */

        body: {
            weight: "",
        },

        /* ------------------------------ */
        /* Activity                       */
        /* ------------------------------ */

        activity: {
            steps: "",
            totalCaloriesBurnt: "",
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
            protein: "",
            carbs: "",
            fat: "",
            fibre: "",
            sugar: "",
            caloriesConsumed: "",
        },

        /* ------------------------------ */
        /* Hydration                      */
        /* ------------------------------ */

        hydration: {
            water: "",
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