import { cleanup, render, screen } from "@testing-library/react";

import { afterEach, describe, expect, test } from "vitest";

import LoadingSpinner from "./LoadingSpinner";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    LoadingSpinner Tests

    Each test follows the same sequence:

    1. Render the LoadingSpinner component.
    2. Verify that the expected loading
       message is displayed.
*/

describe("LoadingSpinner", () => {

    // Verify that the loading message is displayed.
    test("renders loading message", () => {

        // -------------------------------------------------------------
        // Render the LoadingSpinner component.
        // -------------------------------------------------------------
        render(
            <LoadingSpinner />
        );

        // -------------------------------------------------------------
        // Verify that the loading text is displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Loading...")
        ).toBeInTheDocument();

    });


    // Verify that the loading message is rendered inside a paragraph.
    test("renders paragraph element", () => {

        // -------------------------------------------------------------
        // Render the LoadingSpinner component.
        // -------------------------------------------------------------
        render(
            <LoadingSpinner />
        );

        // -------------------------------------------------------------
        // Verify that the loading message is contained
        // within a paragraph element.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Loading...")
                .tagName
        ).toBe("P");

    });

});