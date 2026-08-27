import { cleanup, render, screen } from "@testing-library/react";

import { afterEach, describe, expect, test } from "vitest";

import { Home } from "lucide-react";
import { MemoryRouter } from "react-router-dom";

import NavigationItem from "./NavigationItem";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    NavigationItem Tests

    Each test follows the same sequence:

    1. Render the NavigationItem component.
    2. Wrap it in a MemoryRouter.
    3. Provide any required props.
    4. Verify that the NavigationItem behaves as expected.
*/

describe("NavigationItem", () => {

    // Verify that the navigation label is displayed.
    test("renders label", () => {

        render(
            <MemoryRouter>
                <NavigationItem
                    to="/"
                    label="Dashboard"
                    icon={Home}
                />
            </MemoryRouter>
        );

        expect(
            screen.getByText("Dashboard")
        ).toBeInTheDocument();

    });


    // Verify that the navigation link points to the correct route.
    test("renders correct link", () => {

        render(
            <MemoryRouter>
                <NavigationItem
                    to="/history"
                    label="History"
                    icon={Home}
                />
            </MemoryRouter>
        );

        expect(
            screen.getByRole("link")
        ).toHaveAttribute(
            "href",
            "/history"
        );

    });


    // Verify that the supplied icon is rendered.
    test("renders icon", () => {

        const { container } = render(
            <MemoryRouter>
                <NavigationItem
                    to="/"
                    label="Dashboard"
                    icon={Home}
                />
            </MemoryRouter>
        );

        expect(
            container.querySelector("svg")
        ).toBeInTheDocument();

    });


    // Verify that the active desktop styling is applied.
    test("applies active desktop styling", () => {

        render(
            <MemoryRouter initialEntries={["/"]}>
                <NavigationItem
                    to="/"
                    label="Dashboard"
                    icon={Home}
                />
            </MemoryRouter>
        );

        expect(
            screen.getByRole("link")
        ).toHaveClass("bg-blue-50");

        expect(
            screen.getByRole("link")
        ).toHaveClass("text-blue-700");

    });


    // Verify that the inactive desktop styling is applied.
    test("applies inactive desktop styling", () => {

        render(
            <MemoryRouter initialEntries={["/history"]}>
                <NavigationItem
                    to="/"
                    label="Dashboard"
                    icon={Home}
                />
            </MemoryRouter>
        );

        expect(
            screen.getByRole("link")
        ).toHaveClass("text-slate-700");

    });


    // Verify that the mobile layout is applied.
    test("renders mobile layout", () => {

        render(
            <MemoryRouter>
                <NavigationItem
                    to="/"
                    label="Dashboard"
                    icon={Home}
                    mobile
                />
            </MemoryRouter>
        );

        expect(
            screen.getByRole("link")
        ).toHaveClass("flex-col");

        expect(
            screen.getByRole("link")
        ).toHaveClass("text-xs");

    });

});