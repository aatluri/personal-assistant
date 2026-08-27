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

import HydrationSection from "./HydrationSection";

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
    HydrationSection Tests

    Each test follows the same sequence:

    1. Render the HydrationSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the HydrationSection behaves as expected.

    The tests verify:
    - The Water field is rendered correctly.
    - The supplied water value is displayed correctly.
    - Updating the water value calls setDailyLog().
    - Only the water field is updated while the
      rest of the DailyLog is preserved.
*/

describe("HydrationSection", () => {

    // Verify that the Water field is displayed.
    test("renders water field", () => {

        render(
            <HydrationSection
                water={2500}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Water (ml)")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Water value is displayed.
    test("renders supplied water", () => {

        render(
            <HydrationSection
                water={2500}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("2500")
        ).toBeInTheDocument();

    });


    // Verify that changing the Water value updates the DailyLog.
    test("updates water", () => {

        const setDailyLog = vi.fn();

        render(
            <HydrationSection
                water={2500}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Water (ml)"),
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

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.hydration.water
        ).toBe(3000);

    });

});