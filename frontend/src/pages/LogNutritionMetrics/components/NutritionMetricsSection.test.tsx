import {
    cleanup,
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import NutritionMetricsSection from "./NutritionMetricsSection";

import type {
    NutritionMetrics,
} from "../../../types/NutritionMetrics";

import {
    createEmptyNutritionMetrics,
} from "../../../utils/createEmptyNutritionMetrics";


/*
Clean up the rendered components after each test.

This ensures each test starts with
a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});


/*
NutritionMetricsSection Tests

The tests verify:

- All Nutrition Metrics fields are rendered correctly.
- Existing Nutrition Metrics values are displayed correctly.
- Updating each numeric field calls setNutritionMetrics().
- The correct Nutrition Metrics property is updated.
- Source is updated correctly.
*/
describe("NutritionMetricsSection", () => {

    /*
    Verify that all Nutrition Metrics fields
    are displayed.
    */
    test("renders Nutrition Metrics fields", () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();


        render(
            <NutritionMetricsSection
                nutritionMetrics={nutritionMetrics}
                setNutritionMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText(
                "Dietary Energy (kcal)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Protein (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Carbohydrates (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Fiber (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Sugar (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Total Fat (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Saturated Fat (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Polyunsaturated Fat (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Monounsaturated Fat (g)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Water (fl oz)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Cholesterol (mg)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that supplied Nutrition Metrics
    values are displayed correctly.
    */
    test("renders supplied values", () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();


        nutritionMetrics.dietaryEnergyKcal = 1800;

        nutritionMetrics.proteinG = 110.5;

        nutritionMetrics.carbohydratesG = 190.2;

        nutritionMetrics.fiberG = 28.5;

        nutritionMetrics.sugarG = 35.4;

        nutritionMetrics.totalFatG = 60.5;

        nutritionMetrics.saturatedFatG = 18.2;

        nutritionMetrics.polyunsaturatedFatG = 12.4;

        nutritionMetrics.monounsaturatedFatG = 20.6;

        nutritionMetrics.waterFlOzUs = 100.5;

        nutritionMetrics.cholesterolMg = 220.5;

        nutritionMetrics.source = "FoodNoms";


        render(
            <NutritionMetricsSection
                nutritionMetrics={nutritionMetrics}
                setNutritionMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText(
                "Dietary Energy (kcal)"
            )
        ).toHaveValue(1800);

        expect(
            screen.getByLabelText(
                "Protein (g)"
            )
        ).toHaveValue(110.5);

        expect(
            screen.getByLabelText(
                "Carbohydrates (g)"
            )
        ).toHaveValue(190.2);

        expect(
            screen.getByLabelText(
                "Fiber (g)"
            )
        ).toHaveValue(28.5);

        expect(
            screen.getByLabelText(
                "Sugar (g)"
            )
        ).toHaveValue(35.4);

        expect(
            screen.getByLabelText(
                "Total Fat (g)"
            )
        ).toHaveValue(60.5);

        expect(
            screen.getByLabelText(
                "Saturated Fat (g)"
            )
        ).toHaveValue(18.2);

        expect(
            screen.getByLabelText(
                "Polyunsaturated Fat (g)"
            )
        ).toHaveValue(12.4);

        expect(
            screen.getByLabelText(
                "Monounsaturated Fat (g)"
            )
        ).toHaveValue(20.6);

        expect(
            screen.getByLabelText(
                "Water (fl oz)"
            )
        ).toHaveValue(100.5);

        expect(
            screen.getByLabelText(
                "Cholesterol (mg)"
            )
        ).toHaveValue(220.5);

        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toHaveValue("FoodNoms");

    });


    /*
    Helper used by the numeric field tests.

    Every numeric field uses the same update
    behaviour:

    1. Render the component.
    2. Change the selected input.
    3. Capture the state updater function.
    4. Apply the updater to the previous state.
    5. Verify that the correct property changed.

    Although this logic is shared, every call to
    testNumericField() creates a separate Vitest test.
    */
    function testNumericField(
        testName: string,
        label: string,
        field: keyof NutritionMetrics,
        inputValue: string,
        expectedValue: number,
    ) {

        test(testName, () => {

            const nutritionMetrics =
                createEmptyNutritionMetrics();

            const setNutritionMetrics =
                vi.fn();


            render(
                <NutritionMetricsSection
                    nutritionMetrics={nutritionMetrics}
                    setNutritionMetrics={setNutritionMetrics}
                />
            );


            fireEvent.change(
                screen.getByLabelText(label),
                {
                    target: {
                        value: inputValue,
                    },
                }
            );


            expect(
                setNutritionMetrics
            ).toHaveBeenCalled();


            /*
            NutritionMetricsSection passes a
            state updater function to
            setNutritionMetrics().
            */
            const updateFunction =
                setNutritionMetrics.mock.calls[0][0] as (
                    nutritionMetrics: NutritionMetrics
                ) => NutritionMetrics;


            const previousNutritionMetrics =
                createEmptyNutritionMetrics();


            const updatedNutritionMetrics =
                updateFunction(
                    previousNutritionMetrics
                );


            expect(
                updatedNutritionMetrics[field]
            ).toBe(expectedValue);

        });

    }


    testNumericField(
        "updates dietary energy",
        "Dietary Energy (kcal)",
        "dietaryEnergyKcal",
        "1800",
        1800
    );


    testNumericField(
        "updates protein",
        "Protein (g)",
        "proteinG",
        "110.5",
        110.5
    );


    testNumericField(
        "updates carbohydrates",
        "Carbohydrates (g)",
        "carbohydratesG",
        "190.2",
        190.2
    );


    testNumericField(
        "updates fiber",
        "Fiber (g)",
        "fiberG",
        "28.5",
        28.5
    );


    testNumericField(
        "updates sugar",
        "Sugar (g)",
        "sugarG",
        "35.4",
        35.4
    );


    testNumericField(
        "updates total fat",
        "Total Fat (g)",
        "totalFatG",
        "60.5",
        60.5
    );


    testNumericField(
        "updates saturated fat",
        "Saturated Fat (g)",
        "saturatedFatG",
        "18.2",
        18.2
    );


    testNumericField(
        "updates polyunsaturated fat",
        "Polyunsaturated Fat (g)",
        "polyunsaturatedFatG",
        "12.4",
        12.4
    );


    testNumericField(
        "updates monounsaturated fat",
        "Monounsaturated Fat (g)",
        "monounsaturatedFatG",
        "20.6",
        20.6
    );


    testNumericField(
        "updates water",
        "Water (fl oz)",
        "waterFlOzUs",
        "100.5",
        100.5
    );


    testNumericField(
        "updates cholesterol",
        "Cholesterol (mg)",
        "cholesterolMg",
        "220.5",
        220.5
    );


    /*
    Verify that changing Source updates
    the source property as text.
    */
    test("updates source", () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();

        const setNutritionMetrics =
            vi.fn();


        render(
            <NutritionMetricsSection
                nutritionMetrics={nutritionMetrics}
                setNutritionMetrics={setNutritionMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText(
                "Source"
            ),
            {
                target: {
                    value: "FoodNoms",
                },
            }
        );


        expect(
            setNutritionMetrics
        ).toHaveBeenCalled();


        const updateFunction =
            setNutritionMetrics.mock.calls[0][0] as (
                nutritionMetrics: NutritionMetrics
            ) => NutritionMetrics;


        const previousNutritionMetrics =
            createEmptyNutritionMetrics();


        const updatedNutritionMetrics =
            updateFunction(
                previousNutritionMetrics
            );


        expect(
            updatedNutritionMetrics.source
        ).toBe("FoodNoms");

    });


    /*
    Verify that clearing a numeric field
    stores an empty string.

    Empty strings are important because they
    allow the UI to represent a numeric field
    that currently has no value.
    */
    test("keeps cleared numeric field empty", () => {

        const nutritionMetrics =
            createEmptyNutritionMetrics();

        nutritionMetrics.proteinG = 110.5;

        const setNutritionMetrics =
            vi.fn();


        render(
            <NutritionMetricsSection
                nutritionMetrics={nutritionMetrics}
                setNutritionMetrics={setNutritionMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText(
                "Protein (g)"
            ),
            {
                target: {
                    value: "",
                },
            }
        );


        const updateFunction =
            setNutritionMetrics.mock.calls[0][0] as (
                nutritionMetrics: NutritionMetrics
            ) => NutritionMetrics;


        const updatedNutritionMetrics =
            updateFunction(
                nutritionMetrics
            );


        expect(
            updatedNutritionMetrics.proteinG
        ).toBe("");

    });

});