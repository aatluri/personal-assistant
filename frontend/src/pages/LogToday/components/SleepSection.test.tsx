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

import SleepSection from "./SleepSection";

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
    SleepSection Tests

    Each test follows the same sequence:

    1. Render the SleepSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the SleepSection behaves as expected.
*/

describe("SleepSection", () => {

    // Verify that both Sleep fields are displayed.
    test("renders sleep fields", () => {

        const dailyLog =
            createEmptyDailyLog();

        render(
            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Sleep Start Time")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Sleep End Time")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Sleep values are displayed.
    test("renders supplied values", () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.sleep.sleepStartTime = "22:30";
        dailyLog.sleep.sleepEndTime = "06:45";

        render(
            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("22:30")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("06:45")
        ).toBeInTheDocument();

    });


    // Verify that changing Sleep Start Time updates the DailyLog.
    test("updates sleep start time", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Sleep Start Time"),
            {
                target: {
                    value: "23:00",
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

        previousDailyLog.sleep.sleepEndTime =
            "06:45";

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.sleep.sleepStartTime
        ).toBe("23:00");

        /*
            Verify that the other Sleep value
            was preserved.
        */
        expect(
            updatedDailyLog.sleep.sleepEndTime
        ).toBe("06:45");

    });


    // Verify that changing Sleep End Time updates the DailyLog.
    test("updates sleep end time", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Sleep End Time"),
            {
                target: {
                    value: "07:15",
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

        previousDailyLog.sleep.sleepStartTime =
            "22:30";

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.sleep.sleepEndTime
        ).toBe("07:15");

        /*
            Verify that the other Sleep value
            was preserved.
        */
        expect(
            updatedDailyLog.sleep.sleepStartTime
        ).toBe("22:30");

    });

});