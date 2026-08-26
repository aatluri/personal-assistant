/*
    DailyLog

    Defines the structure of the Daily Log
    object used throughout the frontend.

    This interface represents the page state and is
    shared between:
    - API layer
    - Page components
    - Utility functions
*/

export interface DailyLog {


    /* ------------------------------ */
    /* Workout                        */
    /* ------------------------------ */

    workout: {

        workoutType: string;
        workoutDuration: number | "";
        workoutCalories: number | "";
        workoutVolume: number | "";
        workoutSets: number | "";
        averageHeartRate: number | "";
        workoutSummary: string;

    };

    /* ------------------------------ */
    /* Body                           */
    /* ------------------------------ */

    body: {

        weight: number | "";

    };

    /* ------------------------------ */
    /* Activity                       */
    /* ------------------------------ */

    activity: {

        steps: number | "";
        totalCaloriesBurnt: number | "";

    };

    /* ------------------------------ */
    /* Meal Timing                    */
    /* ------------------------------ */

    mealTiming: {

        firstMealTime: string;
        lastMealTime: string;

    };

    /* ------------------------------ */
    /* Nutrition                      */
    /* ------------------------------ */

    nutrition: {

        breakfast: string;
        lunch: string;
        dinner: string;
        snacks: string;

        protein: number | "";
        carbs: number | "";
        fat: number | "";
        fibre: number | "";
        sugar: number | "";

        caloriesConsumed: number | "";

    };

    /* ------------------------------ */
    /* Hydration                      */
    /* ------------------------------ */

    hydration: {

        water: number | "";

    };

    /* ------------------------------ */
    /* Sleep                          */
    /* ------------------------------ */

    sleep: {

        sleepStartTime: string;
        sleepEndTime: string;

    };

    /* ------------------------------ */
    /* Notes                          */
    /* ------------------------------ */

    notes: {

        notes: string;

    };

}