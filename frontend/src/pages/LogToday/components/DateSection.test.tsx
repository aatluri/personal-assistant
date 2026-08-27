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

import userEvent from "@testing-library/user-event";

import DateSection from "./DateSection";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    DateSection Tests

    Each test follows the same sequence:

    1. Render the DateSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the DateSection behaves as expected.

    The tests verify:
    - The formatted date is displayed.
    - The selected date is displayed in the date picker.
    - Clicking the previous and next buttons updates the date.
    - Selecting a date from the date picker updates the date.
*/

describe("DateSection", () => {

    // Verify that the formatted date is displayed.
    test("renders formatted date", () => {

        render(
            <DateSection
                selectedDate="2026-08-27"
                setSelectedDate={vi.fn()}
            />
        );

        expect(
            screen.getByText(/2026/)
        ).toBeInTheDocument();

    });


    // Verify that the selected date is displayed in the date picker.
    test("renders selected date", () => {

        render(
            <DateSection
                selectedDate="2026-08-27"
                setSelectedDate={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("2026-08-27")
        ).toBeInTheDocument();

    });


    // Verify that clicking the Previous button updates the date.
    test("goes to previous day", async () => {

        const setSelectedDate = vi.fn();

        const { container } = render(
            <DateSection
                selectedDate="2026-08-27"
                setSelectedDate={setSelectedDate}
            />
        );

        const buttons =
            container.querySelectorAll("button");

        await userEvent.click(buttons[0]);

        expect(setSelectedDate)
            .toHaveBeenCalledWith("2026-08-26");

    });


    // Verify that clicking the Next button updates the date.
    test("goes to next day", async () => {

        const setSelectedDate = vi.fn();

        const { container } = render(
            <DateSection
                selectedDate="2026-08-27"
                setSelectedDate={setSelectedDate}
            />
        );

        const buttons =
            container.querySelectorAll("button");

        await userEvent.click(buttons[1]);

        expect(setSelectedDate)
            .toHaveBeenCalledWith("2026-08-28");

    });


    // Verify that selecting a new date updates the date.
    test("updates selected date", () => {

        const setSelectedDate = vi.fn();

        render(
            <DateSection
                selectedDate="2026-08-27"
                setSelectedDate={setSelectedDate}
            />
        );

        fireEvent.change(
            screen.getByDisplayValue("2026-08-27"),
            {
                target: {
                    value: "2026-08-30",
                },
            }
        );

        expect(setSelectedDate)
            .toHaveBeenCalledWith("2026-08-30");

    });

});