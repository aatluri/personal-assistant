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

import MealTimingSection from "./MealTimingSection";

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
    MealTimingSection Tests

    Each test follows the same sequence:

    1. Render the MealTimingSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the MealTimingSection behaves as expected.

    The tests verify:
    - Both meal timing fields are rendered correctly.
    - Existing meal timing values are displayed correctly.
    - Updating a meal timing field calls setDailyLog().
    - Only the relevant meal timing field is updated while
      the rest of the DailyLog is preserved.
*/

describe("MealTimingSection", () => {

    // Verify that both Meal Timing fields are displayed.
    test("renders meal timing fields", () => {

        const dailyLog =
            createEmptyDailyLog();

        render(
            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("First Meal Time")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Last Meal Time")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Meal Timing values are displayed.
    test("renders supplied values", () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.mealTiming.firstMealTime = "08:30";
        dailyLog.mealTiming.lastMealTime = "20:00";

        render(
            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("08:30")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("20:00")
        ).toBeInTheDocument();

    });


    // Verify that changing the First Meal Time updates the DailyLog.
    test("updates first meal time", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("First Meal Time"),
            {
                target: {
                    value: "09:00",
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

        previousDailyLog.mealTiming.lastMealTime =
            "20:00";

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.mealTiming.firstMealTime
        ).toBe("09:00");

        expect(
            updatedDailyLog.mealTiming.lastMealTime
        ).toBe("20:00");

    });


    // Verify that changing the Last Meal Time updates the DailyLog.
    test("updates last meal time", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Last Meal Time"),
            {
                target: {
                    value: "21:00",
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

        previousDailyLog.mealTiming.firstMealTime =
            "08:30";

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.mealTiming.lastMealTime
        ).toBe("21:00");

        expect(
            updatedDailyLog.mealTiming.firstMealTime
        ).toBe("08:30");

    });

});