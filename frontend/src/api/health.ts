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
    Saves a Daily Log to the backend.
*/
export async function saveDailyLog(dailyLog: DailyLog): Promise<void> {

    /*
        Convert the frontend DailyLog model
        into the format expected by the API.
    */
    const request = {

        date: dailyLog.date,

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
            dailyLog.date,
            dailyLog.mealTiming.firstMealTime
        ),

        last_meal_time: buildDateTime(
            dailyLog.date,
            dailyLog.mealTiming.lastMealTime
        ),

        sleep_start_time: buildDateTime(
            dailyLog.date,
            dailyLog.sleep.sleepStartTime
        ),

        sleep_end_time: buildDateTime(
            dailyLog.date,
            dailyLog.sleep.sleepEndTime
        ),

        notes: dailyLog.notes.notes,

    };

    console.log("API Request", request);

    const response = await fetch(
        "http://localhost:8000/health/daily-logs",
        {
            method: "POST",
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