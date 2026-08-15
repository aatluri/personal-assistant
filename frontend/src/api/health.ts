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
function buildDateTime(date: string, time: string): string {
    return `${date}T${time}:00`;
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
            workoutType: apiResponse.workout_type,
            workoutDuration: apiResponse.workout_duration_min,
            workoutCalories: apiResponse.workout_calories_burnt,
            workoutVolume: 0,
            workoutSets: 0,
            averageHeartRate: 0,
            workoutSummary: apiResponse.workout_summary,
        },

        body: {
            weight: apiResponse.weight_kg,
        },

        activity: {
            steps: apiResponse.steps,
            totalCaloriesBurnt: apiResponse.total_calories_burnt,
        },

        mealTiming: {
            firstMealTime: apiResponse.first_meal_time.substring(11, 16),
            lastMealTime: apiResponse.last_meal_time.substring(11, 16),
        },

        nutrition: {
            breakfast: apiResponse.breakfast ?? "",
            lunch: apiResponse.lunch ?? "",
            dinner: apiResponse.dinner ?? "",
            snacks: apiResponse.snacks ?? "",
            protein: apiResponse.protein_g,
            carbs: apiResponse.carbs_g,
            fat: apiResponse.fat_g,
            fibre: apiResponse.fibre_g,
            sugar: apiResponse.sugar_g,
            caloriesConsumed: apiResponse.calories_consumed,
        },

        hydration: {
            water: apiResponse.water_ml,
        },

        sleep: {
            sleepStartTime: apiResponse.sleep_start_time.substring(11, 16),
            sleepEndTime: apiResponse.sleep_end_time.substring(11, 16),
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

        weight_kg: dailyLog.body.weight,

        workout_type: dailyLog.workout.workoutType,
        workout_summary: dailyLog.workout.workoutSummary,
        workout_duration_min: dailyLog.workout.workoutDuration,
        workout_calories_burnt: dailyLog.workout.workoutCalories,

        steps: dailyLog.activity.steps,
        total_calories_burnt: dailyLog.activity.totalCaloriesBurnt,

        breakfast: dailyLog.nutrition.breakfast,
        lunch: dailyLog.nutrition.lunch,
        dinner: dailyLog.nutrition.dinner,
        snacks: dailyLog.nutrition.snacks,

        protein_g: dailyLog.nutrition.protein,
        carbs_g: dailyLog.nutrition.carbs,
        fibre_g: dailyLog.nutrition.fibre,
        fat_g: dailyLog.nutrition.fat,
        sugar_g: dailyLog.nutrition.sugar,
        calories_consumed: dailyLog.nutrition.caloriesConsumed,

        water_ml: dailyLog.hydration.water,

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