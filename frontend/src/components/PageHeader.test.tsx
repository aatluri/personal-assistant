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

import PageHeader from "./PageHeader";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    PageHeader Tests

    Each test follows the same sequence:

    1. Render the PageHeader component.
    2. Provide the required props.
    3. Verify that the component behaves as expected.

    The tests verify:
    - The supplied page title is displayed.
    - The correct save status text is displayed.
    - The correct colour is applied based on the save status.
*/

describe("PageHeader", () => {

    // Verify that the supplied page title is displayed.
    test("renders title", () => {

        render(
            <PageHeader
                title="Nutrition Metrics"
                isDirty={false}
            />
        );

        expect(
            screen.getByRole("heading", {
                name: "Nutrition Metrics",
            })
        ).toBeInTheDocument();

    });


    // Verify that the saved status is displayed.
    test("renders saved status", () => {

        render(
            <PageHeader
                title="Nutrition Metrics"
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
            <PageHeader
                title="Nutrition Metrics"
                isDirty
            />
        );

        const status = screen.getByText("● Unsaved Changes");

        expect(status).toBeInTheDocument();
        expect(status).toHaveClass("text-amber-600");

    });

});
