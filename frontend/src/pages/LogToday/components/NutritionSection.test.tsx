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

import NutritionSection from "./NutritionSection";

import type { DailyLog } from "../../../types/DailyLog";
import { createEmptyDailyLog } from "../../../utils/createEmptyDailyLog";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    NutritionSection Tests

    Each test follows the same sequence:

    1. Render the NutritionSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the NutritionSection behaves as expected.

    The tests verify:
    - All nutrition fields are rendered correctly.
    - Existing values are displayed correctly.
    - Updating a field calls setDailyLog().
    - Only the relevant nutrition field is updated while
      the rest of the DailyLog is preserved.
*/

describe("NutritionSection", () => {

    // Verify that all Nutrition fields are displayed.
    test("renders nutrition fields", () => {

        // -------------------------------------------------------------
        // Create an empty DailyLog object.
        //
        // This supplies the NutritionSection with the
        // data it expects from the page.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        // -------------------------------------------------------------
        // Render the NutritionSection using the
        // empty DailyLog.
        // -------------------------------------------------------------
        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        // -------------------------------------------------------------
        // Verify that every Nutrition field is rendered.
        //
        // If any field is missing, this test will fail.
        // -------------------------------------------------------------
        expect(
            screen.getByLabelText("Breakfast")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Lunch")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Dinner")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Snacks")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Protein (g)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Carbs (g)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Fat (g)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Fibre (g)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Sugar (g)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Calories Consumed")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Nutrition values are displayed.
    test("renders supplied values", () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.nutrition.breakfast = "Eggs";
        dailyLog.nutrition.lunch = "Chicken";
        dailyLog.nutrition.dinner = "Fish";
        dailyLog.nutrition.snacks = "Almonds";
        dailyLog.nutrition.protein = 120;
        dailyLog.nutrition.carbs = 150;
        dailyLog.nutrition.fat = 60;
        dailyLog.nutrition.fibre = 30;
        dailyLog.nutrition.sugar = 20;
        dailyLog.nutrition.caloriesConsumed = 2200;

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("Eggs")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("Chicken")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("Fish")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("Almonds")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("120")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("150")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("60")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("30")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("20")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("2200")
        ).toBeInTheDocument();

    });


    // Verify that changing Breakfast updates the DailyLog.
    test("updates breakfast", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Breakfast"),
            {
                target: {
                    value: "Eggs",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.breakfast
        ).toBe("Eggs");

    });


    // Verify that changing Lunch updates the DailyLog.
    test("updates lunch", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Lunch"),
            {
                target: {
                    value: "Chicken",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.lunch
        ).toBe("Chicken");

    });


    // Verify that changing Dinner updates the DailyLog.
    test("updates dinner", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Dinner"),
            {
                target: {
                    value: "Fish",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.dinner
        ).toBe("Fish");

    });


    // Verify that changing Snacks updates the DailyLog.
    test("updates snacks", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Snacks"),
            {
                target: {
                    value: "Almonds",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.snacks
        ).toBe("Almonds");

    });

    // Verify that changing Protein updates the DailyLog.
    test("updates protein", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Protein (g)"),
            {
                target: {
                    value: "120",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.protein
        ).toBe(120);

    });


    // Verify that changing Carbs updates the DailyLog.
    test("updates carbs", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Carbs (g)"),
            {
                target: {
                    value: "150",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.carbs
        ).toBe(150);

    });


    // Verify that changing Fat updates the DailyLog.
    test("updates fat", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Fat (g)"),
            {
                target: {
                    value: "60",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.fat
        ).toBe(60);

    });


    // Verify that changing Fibre updates the DailyLog.
    test("updates fibre", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Fibre (g)"),
            {
                target: {
                    value: "30",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.fibre
        ).toBe(30);

    });


    // Verify that changing Sugar updates the DailyLog.
    test("updates sugar", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Sugar (g)"),
            {
                target: {
                    value: "20",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.sugar
        ).toBe(20);

    });


    // Verify that changing Calories Consumed updates the DailyLog.
    test("updates calories consumed", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Calories Consumed"),
            {
                target: {
                    value: "2200",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.nutrition.caloriesConsumed
        ).toBe(2200);

    });

});