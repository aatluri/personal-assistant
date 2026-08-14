/*
    DailyLog

    Defines the structure of all data stored
    for the Log Today page.

    The data is grouped by section so it
    matches the UI and is easier to maintain.
*/

export interface DailyLog {

    /* ------------------------------ */
    /* Body                           */
    /* ------------------------------ */

    body: {
        weight: number;
    };

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

    hydration: {
        water: number;
    };

    sleep: {

        sleepStartTime: string,

        sleepEndTime: string,

    },

    mealTiming: {

        firstMealTime: string,

        lastMealTime: string,

    },

    nutrition: {

        breakfast: string,

        lunch: string,

        dinner: string,

        snacks: string,

        protein: number,

        carbs: number,

        fat: number,

        fibre: number,

        sugar: number,

        caloriesConsumed: number,

    },

    notes: {

        notes: string,

    },

}