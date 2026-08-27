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

import ActivitySection from "./ActivitySection";

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
    ActivitySection Tests

    Each test follows the same sequence:

    1. Render the ActivitySection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the ActivitySection behaves as expected.

    The tests verify:
    - Both activity fields are rendered correctly.
    - Existing activity values are displayed correctly.
    - Updating an activity field calls setDailyLog().
    - Only the relevant activity field is updated while
      the rest of the DailyLog is preserved.
*/

describe("ActivitySection", () => {

    // Verify that both Activity fields are displayed.
    test("renders activity fields", () => {

        const dailyLog =
            createEmptyDailyLog();

        render(
            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Steps")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Total Calories Burnt")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Activity values are displayed.
    test("renders supplied values", () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.activity.steps = 12000;
        dailyLog.activity.totalCaloriesBurnt = 2800;

        render(
            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("12000")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("2800")
        ).toBeInTheDocument();

    });


    // Verify that changing Steps updates the DailyLog.
    test("updates steps", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Steps"),
            {
                target: {
                    value: "15000",
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

        previousDailyLog.activity.totalCaloriesBurnt =
            2800;

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.activity.steps
        ).toBe(15000);

        expect(
            updatedDailyLog.activity.totalCaloriesBurnt
        ).toBe(2800);

    });


    // Verify that changing Total Calories Burnt updates the DailyLog.
    test("updates total calories burnt", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Total Calories Burnt"),
            {
                target: {
                    value: "3000",
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

        previousDailyLog.activity.steps =
            12000;

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.activity.totalCaloriesBurnt
        ).toBe(3000);

        expect(
            updatedDailyLog.activity.steps
        ).toBe(12000);

    });

});