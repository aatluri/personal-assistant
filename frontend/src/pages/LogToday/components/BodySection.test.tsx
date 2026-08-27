import {
    cleanup,
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import { afterEach, describe, expect, test, vi } from "vitest";

import BodySection from "./BodySection";
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
    BodySection Tests

    Each test follows the same sequence:

    1. Render the BodySection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the BodySection behaves as expected.
*/

describe("BodySection", () => {

    // Verify that the Weight field is displayed.
    test("renders weight field", () => {

        // -------------------------------------------------------------
        // Render the BodySection.
        //
        // Provide the current weight along with a mock
        // setDailyLog function.
        // -------------------------------------------------------------
        render(
            <BodySection
                weight={80}
                setDailyLog={vi.fn()}
            />
        );

        // -------------------------------------------------------------
        // Verify that the Weight input is rendered.
        // -------------------------------------------------------------
        expect(
            screen.getByLabelText("Weight (kg)")
        ).toBeInTheDocument();

    });


    // Verify that the supplied weight is displayed.
    test("renders supplied weight", () => {

        // -------------------------------------------------------------
        // Render the component with an initial weight.
        // -------------------------------------------------------------
        render(
            <BodySection
                weight={80.5}
                setDailyLog={vi.fn()}
            />
        );

        // -------------------------------------------------------------
        // Verify that the Weight input displays
        // the supplied value.
        // -------------------------------------------------------------
        expect(
            screen.getByDisplayValue("80.5")
        ).toBeInTheDocument();

    });


    // Verify that changing the Weight updates the DailyLog.
    test("updates weight", () => {

        // -------------------------------------------------------------
        // Create a mock version of setDailyLog.
        //
        // The component should call this whenever the
        // Weight value changes.
        // -------------------------------------------------------------
        const setDailyLog = vi.fn();

        render(
            <BodySection
                weight={80}
                setDailyLog={setDailyLog}
            />
        );

        // -------------------------------------------------------------
        // Simulate the user changing the Weight field.
        //
        // fireEvent.change() triggers the component's
        // onChange handler with the supplied value.
        // -------------------------------------------------------------
        fireEvent.change(
            screen.getByLabelText("Weight (kg)"),
            {
                target: {
                    value: "82",
                },
            }
        );

        // -------------------------------------------------------------
        // Verify that the component requested
        // an update to the DailyLog.
        // -------------------------------------------------------------
        expect(setDailyLog).toHaveBeenCalled();

        // -------------------------------------------------------------
        // Extract the updater function that was passed
        // to setDailyLog.
        //
        // React stores state updates as functions:
        //
        // setDailyLog(previous => ({ ... }))
        //
        // so we execute that function ourselves.
        // -------------------------------------------------------------
        const updateFunction =
            setDailyLog.mock.calls[0][0];

        const previousDailyLog =
            createEmptyDailyLog();

        previousDailyLog.body.weight = 80;

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        // -------------------------------------------------------------
        // Verify that only the Weight field
        // was updated.
        // -------------------------------------------------------------
        expect(
            updatedDailyLog.body.weight
        ).toBe(82);

    });

});