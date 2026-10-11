/*
NutritionMetrics

Defines the structure of the Nutrition Metrics
object used throughout the frontend.

This interface represents the page state and is
shared between:
- API layer
- Page components
- Utility functions
*/

export interface NutritionMetrics {

    /*
    Nutrition record date in YYYY-MM-DD format.
    */
    date: string;

    /* ------------------------------ */
    /* Energy                         */
    /* ------------------------------ */

    dietaryEnergyKcal: number | "";

    /* ------------------------------ */
    /* Macronutrients                 */
    /* ------------------------------ */

    proteinG: number | "";
    carbohydratesG: number | "";
    fiberG: number | "";
    sugarG: number | "";

    totalFatG: number | "";
    saturatedFatG: number | "";
    polyunsaturatedFatG: number | "";
    monounsaturatedFatG: number | "";

    /* ------------------------------ */
    /* Other Nutrition                */
    /* ------------------------------ */

    waterFlOzUs: number | "";
    cholesterolMg: number | "";

    /* ------------------------------ */
    /* Source                         */
    /* ------------------------------ */

    source: string;

}