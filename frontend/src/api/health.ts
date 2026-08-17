/*
    Health API

    Contains all API calls related to
    the Health module.
*/

import type { DailyLog } from "../types/DailyLog";

/*
    Converts a HH:mm time into the format
    expected by the backend.

    Example:
    08:30 -> 2026-08-14T08:30:00
*/
function buildDateTime(
    date: string,
    time: string
): string | null {

    /*
        If no time was entered,
        return null.
    */
    if (!time) {
        return null;
    }

    return `${date}T${time}:00`;

}

/*
    Converts an empty numeric field into null
    before sending it to the backend.
*/
function buildNumber(
    value: number | ""
): number | null {

    return value === "" ? null : value;

}

/*
    Retrieves a Daily Log for the
    specified date.

    Returns null if no Daily Log exists.
*/
export async function getDailyLog(date: string): Promise<DailyLog | null> {

    const response = await fetch(
        `http://localhost:8000/health/daily-logs/${date}`
    );

    /*
        No Daily Log exists for this date.
    */
    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error("Failed to load Daily Log");
    }

    const apiResponse = await response.json();
    console.log("Date passed", date);
    console.log("GET API Response", apiResponse);

    /*
        Convert the backend model into
        the frontend DailyLog model.
    */
    const dailyLog: DailyLog = {


        workout: {
            workoutType: apiResponse.workout_type ?? "",
            workoutDuration: apiResponse.workout_duration_min ?? 0,
            workoutCalories: apiResponse.workout_calories_burnt ?? 0,
            /*
                These fields are currently not stored by
                the backend, so they remain 0 for now.
            */
            workoutVolume: 0,
            workoutSets: 0,
            averageHeartRate: 0,

            workoutSummary: apiResponse.workout_summary ?? "",
        },

        body: {
             weight: apiResponse.weight_kg ?? 0,
        },

        activity: {
            steps: apiResponse.steps ?? 0,
            totalCaloriesBurnt: apiResponse.total_calories_burnt ?? 0,
        },

        mealTiming: {
            firstMealTime: apiResponse.first_meal_time? apiResponse.first_meal_time.substring(11, 16): "",
            lastMealTime: apiResponse.last_meal_time? apiResponse.last_meal_time.substring(11, 16): "",
        },

        nutrition: {
            breakfast: apiResponse.breakfast ?? "",
            lunch: apiResponse.lunch ?? "",
            dinner: apiResponse.dinner ?? "",
            snacks: apiResponse.snacks ?? "",
            protein: apiResponse.protein_g ?? 0,
            carbs: apiResponse.carbs_g ?? 0,
            fat: apiResponse.fat_g ?? 0,
            fibre: apiResponse.fibre_g ?? 0,
            sugar: apiResponse.sugar_g ?? 0,
            caloriesConsumed: apiResponse.calories_consumed ?? 0,
        },

        hydration: {
            water: apiResponse.water_ml ?? 0,
        },

        sleep: {
            sleepStartTime: apiResponse.sleep_start_time? apiResponse.sleep_start_time.substring(11, 16): "",
            sleepEndTime: apiResponse.sleep_end_time? apiResponse.sleep_end_time.substring(11, 16): "",
        },

        notes: {
            notes: apiResponse.notes ?? "",
        },

    };

    return dailyLog;
}


/*
    Saves a Daily Log to the backend.
*/
export async function saveDailyLog(selectedDate: string, dailyLog: DailyLog): Promise<void> {

    /*
        Convert the frontend DailyLog model
        into the format expected by the API.
    */
    const request = {

        date: selectedDate,

        weight_kg: buildNumber(dailyLog.body.weight),

        workout_type: dailyLog.workout.workoutType,
        workout_summary: dailyLog.workout.workoutSummary,
        workout_duration_min: buildNumber(dailyLog.workout.workoutDuration),
        workout_calories_burnt: buildNumber(dailyLog.workout.workoutCalories),

        steps: buildNumber(dailyLog.activity.steps),
        total_calories_burnt: buildNumber(dailyLog.activity.totalCaloriesBurnt),

        breakfast: dailyLog.nutrition.breakfast,
        lunch: dailyLog.nutrition.lunch,
        dinner: dailyLog.nutrition.dinner,
        snacks: dailyLog.nutrition.snacks,

        protein_g: buildNumber(dailyLog.nutrition.protein),
        carbs_g: buildNumber(dailyLog.nutrition.carbs),
        fibre_g: buildNumber(dailyLog.nutrition.fibre),
        fat_g: buildNumber(dailyLog.nutrition.fat),
        sugar_g: buildNumber(dailyLog.nutrition.sugar),
        calories_consumed: buildNumber(dailyLog.nutrition.caloriesConsumed),

        water_ml: buildNumber(dailyLog.hydration.water),

        first_meal_time: buildDateTime(
            selectedDate,
            dailyLog.mealTiming.firstMealTime
        ),

        last_meal_time: buildDateTime(
            selectedDate,
            dailyLog.mealTiming.lastMealTime
        ),

        sleep_start_time: buildDateTime(
            selectedDate,
            dailyLog.sleep.sleepStartTime
        ),

        sleep_end_time: buildDateTime(
            selectedDate,
            dailyLog.sleep.sleepEndTime
        ),

        notes: dailyLog.notes.notes,

    };

    console.log("API Request", request);

    const response = await fetch(
        `http://localhost:8000/health/daily-logs/${selectedDate}`,
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

        throw new Error("Failed to save Daily Log");

    }

}