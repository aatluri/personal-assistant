import { render, screen, cleanup } from "@testing-library/react";

import { afterEach, describe, expect, test } from "vitest";

import PageContainer from "./PageContainer";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    PageContainer Tests

    Each test follows the same sequence:

    1. Render the PageContainer component.
    2. Provide any required props.
    3. Verify that the PageContainer behaves as expected.
*/

describe("PageContainer", () => {

    // Verify that child content is rendered.
    test("renders child content", () => {

        // -------------------------------------------------------------
        // Render the PageContainer with some child content.
        // -------------------------------------------------------------
        render(
            <PageContainer>
                <p>Page Content</p>
            </PageContainer>
        );

        // -------------------------------------------------------------
        // Verify that the child content is displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Page Content")
        ).toBeInTheDocument();

    });

    // Verify that the component renders a main element.
    test("renders main element", () => {

        // -------------------------------------------------------------
        // Render the PageContainer.
        // -------------------------------------------------------------
        render(
            <PageContainer>
                <p>Content</p>
            </PageContainer>
        );

        // -------------------------------------------------------------
        // Verify that a semantic <main> element exists.
        // -------------------------------------------------------------
        expect(
            screen.getByRole("main")
        ).toBeInTheDocument();

    });

    // Verify that the component applies its layout classes.
    test("applies layout classes", () => {

        // -------------------------------------------------------------
        // Render the PageContainer.
        // -------------------------------------------------------------
        render(
            <PageContainer>
                <p>Content</p>
            </PageContainer>
        );

        const main = screen.getByRole("main");

        // -------------------------------------------------------------
        // Verify that the expected Tailwind layout
        // classes have been applied.
        // -------------------------------------------------------------
        expect(main).toHaveClass("min-h-screen");
        expect(main).toHaveClass("bg-slate-50");
        expect(main).toHaveClass("px-4");
        expect(main).toHaveClass("py-8");

    });

});