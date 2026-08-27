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

import App from "./App";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    App Tests

    Each test follows the same sequence:

    1. Set the browser URL.
    2. Render the App.
    3. Verify that the correct page is displayed.

    The tests verify:
    - Each route renders the correct page.
*/

describe("App", () => {

    // Verify that navigating to the Dashboard route
    // displays the Dashboard page.
    test("renders Dashboard route", () => {

        window.history.pushState(
            {},
            "",
            "/"
        );

        render(<App />);

        expect(
            screen.getByRole(
                "heading",
                {
                    name: /Dashboard/,
                }
            )
        ).toBeInTheDocument();

    });


    // Verify that navigating to the Log Today route
    // displays the Log Today page.
    test("renders Log Today route", () => {

        window.history.pushState(
            {},
            "",
            "/log-today"
        );

        render(<App />);

        expect(
            screen.getByText("Log Today")
        ).toBeInTheDocument();

    });


    // Verify that navigating to the Body Measurements
    // route displays the Body Measurements page.
    test("renders Body Measurements route", () => {

        window.history.pushState(
            {},
            "",
            "/body-measurements"
        );

        render(<App />);

        expect(
            screen.getByText("Body Measurements")
        ).toBeInTheDocument();

    });


    // Verify that navigating to the History route
    // displays the History page.
    test("renders History route", () => {

        window.history.pushState(
            {},
            "",
            "/history"
        );

        render(<App />);

        expect(
            screen.getByRole(
                "heading",
                {
                    name: /History/,
                }
            )
        ).toBeInTheDocument();

    });


    // Verify that navigating to the Settings route
    // displays the Settings page.
    test("renders Settings route", () => {

        window.history.pushState(
            {},
            "",
            "/settings"
        );

        render(<App />);

        expect(
            screen.getByText("Settings")
        ).toBeInTheDocument();

    });

});