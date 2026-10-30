/*
Nutrition Metrics API

Acts as the communication layer between the
Nutrition Metrics frontend and backend.

Responsibilities:
- Retrieve Nutrition Metrics from the backend.
- Convert backend models into frontend models.
- Convert frontend models into backend request models.
- Save Nutrition Metrics to the backend.
*/

import type { NutritionMetrics } from "../types/NutritionMetrics";


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
Retrieves Nutrition Metrics for the specified date.

Returns null if no Nutrition Metrics record
exists for the selected date.
*/
export async function getNutritionMetric(
    date: string,
): Promise<NutritionMetrics | null> {

    const response = await fetch(
        `http://localhost:8000/health/nutrition-metrics/${date}`
    );

    /*
    No Nutrition Metrics record exists
    for this date.
    */
    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error(
            "Failed to load Nutrition Metrics"
        );
    }

    const apiResponse = await response.json();

    /*
    Convert the backend API model into
    the frontend NutritionMetrics model.
    */
    const nutritionMetrics: NutritionMetrics = {

        date: apiResponse.date,

        dietaryEnergyKcal:
            apiResponse.dietary_energy_kcal ?? "",

        proteinG:
            apiResponse.protein_g ?? "",

        carbohydratesG:
            apiResponse.carbohydrates_g ?? "",

        fiberG:
            apiResponse.fiber_g ?? "",

        sugarG:
            apiResponse.sugar_g ?? "",

        totalFatG:
            apiResponse.total_fat_g ?? "",

        saturatedFatG:
            apiResponse.saturated_fat_g ?? "",

        polyunsaturatedFatG:
            apiResponse.polyunsaturated_fat_g ?? "",

        monounsaturatedFatG:
            apiResponse.monounsaturated_fat_g ?? "",

        waterMl:
            apiResponse.water_ml ?? "",

        cholesterolMg:
            apiResponse.cholesterol_mg ?? "",

        source:
            apiResponse.source ?? "",

    };

    return nutritionMetrics;

}


/*
Saves Nutrition Metrics.

The backend performs an upsert using
the date as the unique key.
*/
export async function saveNutritionMetric(
    selectedDate: string,
    nutritionMetrics: NutritionMetrics,
): Promise<void> {

    /*
    Convert the frontend model into
    the format expected by the backend.
    */
    const request = {

        date: selectedDate,

        dietary_energy_kcal:
            buildNumber(
                nutritionMetrics.dietaryEnergyKcal
            ),

        protein_g:
            buildNumber(
                nutritionMetrics.proteinG
            ),

        carbohydrates_g:
            buildNumber(
                nutritionMetrics.carbohydratesG
            ),

        fiber_g:
            buildNumber(
                nutritionMetrics.fiberG
            ),

        sugar_g:
            buildNumber(
                nutritionMetrics.sugarG
            ),

        total_fat_g:
            buildNumber(
                nutritionMetrics.totalFatG
            ),

        saturated_fat_g:
            buildNumber(
                nutritionMetrics.saturatedFatG
            ),

        polyunsaturated_fat_g:
            buildNumber(
                nutritionMetrics.polyunsaturatedFatG
            ),

        monounsaturated_fat_g:
            buildNumber(
                nutritionMetrics.monounsaturatedFatG
            ),

        water_ml:
            buildNumber(
                nutritionMetrics.waterMl
            ),

        cholesterol_mg:
            buildNumber(
                nutritionMetrics.cholesterolMg
            ),

        source:
            nutritionMetrics.source || null,

    };

    const response = await fetch(
        "http://localhost:8000/health/nutrition-metrics",
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

        throw new Error(
            "Failed to save Nutrition Metrics"
        );

    }

}