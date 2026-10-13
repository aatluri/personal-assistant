import { describe, expect, test } from "vitest";

import { createEmptyNutritionMetrics } from "./createEmptyNutritionMetrics";


describe("createEmptyNutritionMetrics", () => {

    // Verify that all Nutrition Metrics fields are initialized.
    test("creates empty Nutrition Metrics", () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();

        expect(nutritionMetrics.date).toBe("");

        expect(
            nutritionMetrics.dietaryEnergyKcal
        ).toBe("");

        expect(nutritionMetrics.proteinG).toBe("");
        expect(nutritionMetrics.carbohydratesG).toBe("");
        expect(nutritionMetrics.fiberG).toBe("");
        expect(nutritionMetrics.sugarG).toBe("");

        expect(nutritionMetrics.totalFatG).toBe("");
        expect(nutritionMetrics.saturatedFatG).toBe("");
        expect(
            nutritionMetrics.polyunsaturatedFatG
        ).toBe("");
        expect(
            nutritionMetrics.monounsaturatedFatG
        ).toBe("");

        expect(
            nutritionMetrics.waterFlOzUs
        ).toBe("");

        expect(
            nutritionMetrics.cholesterolMg
        ).toBe("");

        expect(nutritionMetrics.source).toBe("");

    });

});