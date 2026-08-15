/*
    DailyLog

    Defines the structure of all data stored
    for the Log Today page.

    The data is grouped by section so it
    matches the UI and is easier to maintain.
*/

export interface DailyLog {


    /* ------------------------------ */
    /* Workout                        */
    /* ------------------------------ */

    workout: {

        workoutType: string;
        workoutDuration: number;
        workoutCalories: number;
        workoutVolume: number;
        workoutSets: number;
        averageHeartRate: number;
        workoutSummary: string;

    };

    /* ------------------------------ */
    /* Body                           */
    /* ------------------------------ */

    body: {

        weight: number;

    };

    /* ------------------------------ */
    /* Activity                       */
    /* ------------------------------ */

    activity: {

        steps: number;
        totalCaloriesBurnt: number;

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

        protein: number;
        carbs: number;
        fat: number;
        fibre: number;
        sugar: number;

        caloriesConsumed: number;

    };

    /* ------------------------------ */
    /* Hydration                      */
    /* ------------------------------ */

    hydration: {

        water: number;

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