import type { NutritionMetrics } from "../types/NutritionMetrics";

/*
Creates an empty Nutrition Metrics object.

Used when:
- No Nutrition Metrics exist for the selected date.
- The page needs an initial empty state.
*/

export function createEmptyNutritionMetrics(): NutritionMetrics {

    return {

        date: "",

        dietaryEnergyKcal: "",

        proteinG: "",
        carbohydratesG: "",
        fiberG: "",
        sugarG: "",

        totalFatG: "",
        saturatedFatG: "",
        polyunsaturatedFatG: "",
        monounsaturatedFatG: "",

        waterFlOzUs: "",
        cholesterolMg: "",

        source: "",

    };

}