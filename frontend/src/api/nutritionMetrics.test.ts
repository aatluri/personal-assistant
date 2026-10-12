import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getNutritionMetric,
    saveNutritionMetric,
} from "./nutritionMetrics";

import {
    createEmptyNutritionMetrics,
} from "../utils/createEmptyNutritionMetrics";


/*
Mock the browser's fetch() function.

No real HTTP requests are made during
these API unit tests.
*/
globalThis.fetch = vi.fn();


/*
Clean up mock call history after each test.
*/
afterEach(() => {

    vi.clearAllMocks();

});


/*
Configure the default fetch response.

Individual tests can override this response
when required.
*/
beforeEach(() => {

    vi.mocked(fetch).mockResolvedValue({

        ok: true,

        status: 200,

        json: vi.fn().mockResolvedValue({}),

        text: vi.fn(),

    } as unknown as Response);

});


describe("Nutrition Metrics API", () => {

    /*
    Verify that Nutrition Metrics are correctly
    retrieved and converted from the backend
    snake_case model into the frontend model.
    */
    test("returns Nutrition Metrics", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                date: "2026-08-27",

                dietary_energy_kcal: 2100,

                protein_g: 120,
                carbohydrates_g: 220,

                fiber_g: 30,
                sugar_g: 35,

                total_fat_g: 70,
                saturated_fat_g: 20,
                polyunsaturated_fat_g: 15,
                monounsaturated_fat_g: 25,

                water_fl_oz_us: 100,

                cholesterol_mg: 250,

                source: "Foodnoms",

            }),

        } as unknown as Response);


        const nutritionMetrics =
            await getNutritionMetric(
                "2026-08-27"
            );


        expect(nutritionMetrics).toEqual({

            date: "2026-08-27",

            dietaryEnergyKcal: 2100,

            proteinG: 120,
            carbohydratesG: 220,

            fiberG: 30,
            sugarG: 35,

            totalFatG: 70,
            saturatedFatG: 20,
            polyunsaturatedFatG: 15,
            monounsaturatedFatG: 25,

            waterFlOzUs: 100,

            cholesterolMg: 250,

            source: "Foodnoms",

        });


        /*
        Verify that the selected date is
        included in the GET endpoint.
        */
        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/nutrition-metrics/2026-08-27"

        );

    });


    /*
    Verify that null is returned when no
    Nutrition Metrics record exists for the date.
    */
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);


        const nutritionMetrics =
            await getNutritionMetric(
                "2026-08-27"
            );


        expect(nutritionMetrics).toBeNull();

    });


    /*
    Verify that an unexpected backend error
    causes the API function to throw.
    */
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);


        await expect(

            getNutritionMetric(
                "2026-08-27"
            )

        ).rejects.toThrow(

            "Failed to load Nutrition Metrics"

        );

    });


    /*
    Verify that saveNutritionMetric converts
    the frontend model into the correct
    backend request model.
    */
    test("sends correct Nutrition Metrics request", async () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();


        nutritionMetrics.dietaryEnergyKcal = 2100;

        nutritionMetrics.proteinG = 120;
        nutritionMetrics.carbohydratesG = 220;

        nutritionMetrics.fiberG = 30;
        nutritionMetrics.sugarG = 35;

        nutritionMetrics.totalFatG = 70;
        nutritionMetrics.saturatedFatG = 20;
        nutritionMetrics.polyunsaturatedFatG = 15;
        nutritionMetrics.monounsaturatedFatG = 25;

        nutritionMetrics.waterFlOzUs = 100;

        nutritionMetrics.cholesterolMg = 250;

        nutritionMetrics.source = "Foodnoms";


        await saveNutritionMetric(
            "2026-08-27",
            nutritionMetrics
        );


        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/nutrition-metrics",

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    dietary_energy_kcal: 2100,

                    protein_g: 120,
                    carbohydrates_g: 220,

                    fiber_g: 30,
                    sugar_g: 35,

                    total_fat_g: 70,
                    saturated_fat_g: 20,
                    polyunsaturated_fat_g: 15,
                    monounsaturated_fat_g: 25,

                    water_fl_oz_us: 100,

                    cholesterol_mg: 250,

                    source: "Foodnoms",

                }),
            }
        );

    });


    /*
    Verify that empty numeric and source
    values are converted to null before
    being sent to the backend.
    */
    test("converts empty Nutrition Metrics values to null", async () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();


        await saveNutritionMetric(
            "2026-08-27",
            nutritionMetrics
        );


        expect(fetch).toHaveBeenCalledTimes(1);


        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];


        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );


        expect(
            requestBody.dietary_energy_kcal
        ).toBeNull();

        expect(
            requestBody.protein_g
        ).toBeNull();

        expect(
            requestBody.carbohydrates_g
        ).toBeNull();

        expect(
            requestBody.fiber_g
        ).toBeNull();

        expect(
            requestBody.sugar_g
        ).toBeNull();

        expect(
            requestBody.total_fat_g
        ).toBeNull();

        expect(
            requestBody.saturated_fat_g
        ).toBeNull();

        expect(
            requestBody.polyunsaturated_fat_g
        ).toBeNull();

        expect(
            requestBody.monounsaturated_fat_g
        ).toBeNull();

        expect(
            requestBody.water_fl_oz_us
        ).toBeNull();

        expect(
            requestBody.cholesterol_mg
        ).toBeNull();

        expect(
            requestBody.source
        ).toBeNull();

    });


    /*
    Verify that an error is thrown when
    saving Nutrition Metrics fails.
    */
    test("throws on Nutrition Metrics save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);


        const nutritionMetrics =
            createEmptyNutritionMetrics();


        await expect(

            saveNutritionMetric(
                "2026-08-27",
                nutritionMetrics
            )

        ).rejects.toThrow(

            "Failed to save Nutrition Metrics"

        );

    });

});