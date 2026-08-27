import {
    cleanup,
    render,
    screen,
} from "@testing-library/react";

import {
    afterEach,
    describe,
    expect,
    test,
} from "vitest";

import LogTodayHeader from "./LogTodayHeader";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    LogTodayHeader Tests

    Each test follows the same sequence:

    1. Render the LogTodayHeader component.
    2. Provide the required props.
    3. Verify that the component behaves as expected.

    The tests verify:
    - The page heading is displayed.
    - The correct save status text is displayed.
    - The correct colour is applied based on the save status.
*/

describe("LogTodayHeader", () => {

    // Verify that the page heading is displayed.
    test("renders heading", () => {

        render(
            <LogTodayHeader
                isDirty={false}
            />
        );

        expect(
            screen.getByText("Log Today")
        ).toBeInTheDocument();

    });


    // Verify that the saved status is displayed.
    test("renders saved status", () => {

        render(
            <LogTodayHeader
                isDirty={false}
            />
        );

        const status = screen.getByText("✓ Saved");

        expect(status).toBeInTheDocument();
        expect(status).toHaveClass("text-green-600");

    });


    // Verify that the unsaved status is displayed.
    test("renders unsaved status", () => {

        render(
            <LogTodayHeader
                isDirty
            />
        );

        const status = screen.getByText("● Unsaved Changes");

        expect(status).toBeInTheDocument();
        expect(status).toHaveClass("text-amber-600");

    });

});