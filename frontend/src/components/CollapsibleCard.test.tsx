import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, test } from "vitest";
import { Dumbbell } from "lucide-react";
import CollapsibleCard from "./CollapsibleCard";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    CollapsibleCard Tests

    Each test follows the same sequence:

    1. Render the CollapsibleCard component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify that the CollapsibleCard behaves as expected.
*/

describe("CollapsibleCard", () => {

    // Verify that the title is displayed.
    test("renders title", () => {

        // -------------------------------------------------------------
        // Render the CollapsibleCard component with a title,
        // icon and some child content.
        // -------------------------------------------------------------
        render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Verify that the supplied title is displayed
        // in the card header.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Workout")
        ).toBeInTheDocument();

    });


    // Verify that the supplied child content is displayed.
    test("renders child content", () => {

        // -------------------------------------------------------------
        // Render the CollapsibleCard with some content.
        //
        // The card starts in the expanded state, so the
        // content should immediately be visible.
        // -------------------------------------------------------------
        render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Verify that the child content is displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Card Content")
        ).toBeInTheDocument();

    });


    // Verify that the supplied icon is rendered.
    test("renders icon", () => {

        // -------------------------------------------------------------
        // Render the component.
        //
        // The render() function returns the container,
        // which gives us access to the generated HTML.
        // -------------------------------------------------------------
        const { container } = render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Verify that an SVG element exists.
        //
        // Lucide icons are rendered as SVG elements.
        // -------------------------------------------------------------
        expect(
            container.querySelector("svg")
        ).toBeInTheDocument();

    });


    // Verify that the card starts in the expanded state.
    test("starts expanded", () => {

        // -------------------------------------------------------------
        // Render the component.
        // -------------------------------------------------------------
        render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Find the container that wraps the card content.
        //
        // When the card is expanded, this container should
        // contain the "max-h-[2000px]" class.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Card Content")
                .parentElement
        ).toHaveClass("max-h-[2000px]");

    });


    // Verify that clicking the header collapses the card.
    test("collapses when clicked", async () => {

        // -------------------------------------------------------------
        // Render the component.
        // -------------------------------------------------------------
        render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Simulate the user clicking the card header.
        //
        // This toggles the expanded state from
        // expanded -> collapsed.
        // -------------------------------------------------------------
        await userEvent.click(
            screen.getByRole(
                "button",
                { name: /Workout/i }
            )
        );

        // -------------------------------------------------------------
        // Verify that the content container now has
        // the collapsed CSS class.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Card Content")
                .parentElement
        ).toHaveClass("max-h-0");

    });


    // Verify that clicking the header twice expands the card again.
    test("expands again when clicked twice", async () => {

        // -------------------------------------------------------------
        // Render the component.
        // -------------------------------------------------------------
        render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-blue-600"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Locate the header button.
        // -------------------------------------------------------------
        const button = screen.getByRole(
            "button",
            { name: /Workout/i }
        );

        // -------------------------------------------------------------
        // Click once to collapse the card.
        // Click again to expand it.
        // -------------------------------------------------------------
        await userEvent.click(button);
        await userEvent.click(button);

        // -------------------------------------------------------------
        // Verify that the expanded CSS class has
        // been restored.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Card Content")
                .parentElement
        ).toHaveClass("max-h-[2000px]");

    });


    // Verify that the supplied icon colour class is applied.
    test("applies icon colour", () => {

        // -------------------------------------------------------------
        // Render the component with a custom icon colour.
        // -------------------------------------------------------------
        const { container } = render(
            <CollapsibleCard
                title="Workout"
                icon={Dumbbell}
                iconColor="text-red-500"
            >
                Card Content
            </CollapsibleCard>
        );

        // -------------------------------------------------------------
        // Locate the rendered SVG icon.
        // -------------------------------------------------------------
        const svg = container.querySelector("svg");

        // -------------------------------------------------------------
        // Verify that the custom Tailwind class has
        // been applied to the icon.
        // -------------------------------------------------------------
        expect(svg).toHaveClass("text-red-500");

    });

});