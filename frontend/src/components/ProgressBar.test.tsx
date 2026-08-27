import { cleanup, render, screen } from "@testing-library/react";

import { afterEach, describe, expect, test } from "vitest";

import ProgressBar from "./ProgressBar";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    ProgressBar Tests

    Each test follows the same sequence:

    1. Render the ProgressBar component.
    2. Provide any required props.
    3. Verify that the ProgressBar behaves as expected.
*/

describe("ProgressBar", () => {

    // Verify that the label is displayed.
    test("renders label", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar component.
        // -------------------------------------------------------------
        render(
            <ProgressBar
                label="Protein"
                current={80}
                goal={100}
            />
        );

        // -------------------------------------------------------------
        // Verify that the label is displayed.
        // searches the rendered virtual screen (DOM) for an element whose visible text is "Protein".
        // -------------------------------------------------------------
        expect(
            screen.getByText("Protein")
        ).toBeInTheDocument();

    });


    // Verify that the current and goal values are displayed.
    test("renders current and goal values", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar.
        // -------------------------------------------------------------
        render(
            <ProgressBar
                label="Protein"
                current={80}
                goal={100}
                unit="g"
            />
        );

        // -------------------------------------------------------------
        // Verify that the formatted values are displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByText("80g / 100g")
        ).toBeInTheDocument();

    });


    // Verify that the progress width is calculated correctly.
    test("calculates progress width", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar.
        // -------------------------------------------------------------
        const { container } = render(
            <ProgressBar
                label="Protein"
                current={75}
                goal={100}
            />
        );

        // -------------------------------------------------------------
        // The inner progress bar is the second div with
        // an inline width style.
        // -------------------------------------------------------------
        const progress =
            container.querySelector(
                '[style*="width"]'
            );

        expect(progress).toHaveStyle({
            width: "75%",
        });

    });


    // Verify that progress never exceeds 100%.
    test("caps progress at 100 percent", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar with a value
        // greater than the goal.
        // -------------------------------------------------------------
        const { container } = render(
            <ProgressBar
                label="Protein"
                current={150}
                goal={100}
            />
        );

        const progress =
            container.querySelector(
                '[style*="width"]'
            );

        // -------------------------------------------------------------
        // Verify that the width is capped at 100%.
        // -------------------------------------------------------------
        expect(progress).toHaveStyle({
            width: "100%",
        });

    });


    // Verify that a custom colour class is applied.
    test("supports custom colour", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar with a custom colour.
        // -------------------------------------------------------------
        const { container } = render(
            <ProgressBar
                label="Protein"
                current={80}
                goal={100}
                color="bg-green-600"
            />
        );

        const progress =
            container.querySelector(
                '[style*="width"]'
            );

        // -------------------------------------------------------------
        // Verify that the custom Tailwind class
        // has been applied.
        // -------------------------------------------------------------
        expect(progress).toHaveClass(
            "bg-green-600"
        );

    });


    // Verify that custom display values override
    // the automatically generated values.
    test("supports custom display values", () => {

        // -------------------------------------------------------------
        // Render the ProgressBar with custom
        // display values.
        // -------------------------------------------------------------
        render(
            <ProgressBar
                label="Protein"
                current={80}
                goal={100}
                displayCurrent="80 / 130"
                displayGoal="Target"
            />
        );

        // -------------------------------------------------------------
        // Verify that the custom display values
        // are shown instead of the defaults.
        // -------------------------------------------------------------
        expect(
            screen.getByText(
                "80 / 130 / Target"
            )
        ).toBeInTheDocument();

    });

});