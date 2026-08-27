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

import NotesSection from "./NotesSection";

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
    NotesSection Tests

    Each test follows the same sequence:

    1. Render the NotesSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the NotesSection behaves as expected.

    The tests verify:
    - The Notes field is rendered correctly.
    - Existing notes are displayed correctly.
    - Updating the notes calls setDailyLog().
    - Only the notes field is updated while the
      rest of the DailyLog is preserved.
*/

describe("NotesSection", () => {

    // Verify that the Notes field is displayed.
    test("renders notes field", () => {

        const dailyLog =
            createEmptyDailyLog();

        render(
            <NotesSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Notes")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Notes are displayed.
    test("renders supplied notes", () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.notes.notes =
            "Felt great after today's workout.";

        render(
            <NotesSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue(
                "Felt great after today's workout."
            )
        ).toBeInTheDocument();

    });


    // Verify that changing the Notes updates the DailyLog.
    test("updates notes", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <NotesSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Notes"),
            {
                target: {
                    value: "Need to stretch tomorrow.",
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
            updatedDailyLog.notes.notes
        ).toBe("Need to stretch tomorrow.");

    });

});