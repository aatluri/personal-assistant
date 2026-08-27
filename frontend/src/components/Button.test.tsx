import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { describe, expect, test, vi } from "vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

import Button from "./Button";

afterEach(() => {
    cleanup();
});
/*
    Button Tests

    Each test follows the same sequence:

    1. Render the Button component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify that the Button behaves as expected.
*/

describe("Button", () => {

    // Verify that the button displays the supplied content.
    test("renders button text", () => {

        // -------------------------------------------------------------
        // Render the Button component with text inside it.
        //
        // The text is passed to the component through the
        // React children prop.
        // -------------------------------------------------------------
        render(
            <Button>
                Save Changes
            </Button>
        );

        // -------------------------------------------------------------
        // Verify that the button is present and displays
        // the supplied text.
        // -------------------------------------------------------------
        expect(
            screen.getByRole(
                "button",
                { name: "Save Changes" }
            )
        ).toBeInTheDocument();

    });


    // Verify that clicking the button calls the supplied onClick callback.
    test("calls onClick when clicked", async () => {

        // -------------------------------------------------------------
        // Create a mock function.
        //
        // This allows us to verify whether the Button calls
        // the onClick callback when the user clicks it.
        // -------------------------------------------------------------
        const onClick = vi.fn();

        // -------------------------------------------------------------
        // Render the Button using the mock callback.
        // -------------------------------------------------------------
        render(
            <Button
                onClick={onClick}
            >
                Save
            </Button>
        );

        // -------------------------------------------------------------
        // Simulate a real user clicking the button.
        // -------------------------------------------------------------
        await userEvent.click(
            screen.getByRole(
                "button",
                { name: "Save" }
            )
        );

        // -------------------------------------------------------------
        // Verify that the supplied onClick callback
        // was called exactly once.
        // -------------------------------------------------------------
        expect(onClick).toHaveBeenCalledTimes(1);

    });


    // Verify that the disabled prop is passed to the HTML button.
    test("supports disabled", () => {

        // -------------------------------------------------------------
        // Render the Button with the disabled prop.
        // -------------------------------------------------------------
        render(
            <Button disabled>
                Save
            </Button>
        );

        // -------------------------------------------------------------
        // Verify that the rendered HTML button is disabled.
        // -------------------------------------------------------------
        expect(
            screen.getByRole(
                "button",
                { name: "Save" }
            )
        ).toBeDisabled();

    });


    // Verify that clicking a disabled button does not call onClick.
    test("does not call onClick when disabled", async () => {

        // -------------------------------------------------------------
        // Create a mock onClick function.
        // -------------------------------------------------------------
        const onClick = vi.fn();

        // -------------------------------------------------------------
        // Render a disabled Button.
        // -------------------------------------------------------------
        render(
            <Button
                onClick={onClick}
                disabled
            >
                Save
            </Button>
        );

        // -------------------------------------------------------------
        // Attempt to click the disabled button.
        // -------------------------------------------------------------
        await userEvent.click(
            screen.getByRole(
                "button",
                { name: "Save" }
            )
        );

        // -------------------------------------------------------------
        // Verify that the callback was not called.
        // -------------------------------------------------------------
        expect(onClick).not.toHaveBeenCalled();

    });


    // Verify that standard HTML button props are passed through.
    test("supports button type", () => {

        // -------------------------------------------------------------
        // Render the Button with type="submit".
        //
        // Since Button forwards standard HTML button props,
        // the underlying HTML button should receive this value.
        // -------------------------------------------------------------
        render(
            <Button type="submit">
                Submit
            </Button>
        );

        // -------------------------------------------------------------
        // Verify that the rendered button has type="submit".
        // -------------------------------------------------------------
        expect(
            screen.getByRole(
                "button",
                { name: "Submit" }
            )
        ).toHaveAttribute(
            "type",
            "submit"
        );

    });


    // Verify that additional CSS classes supplied by the caller are applied.
    test("supports custom className", () => {

        // -------------------------------------------------------------
        // Render the Button with an additional CSS class.
        // -------------------------------------------------------------
        render(
            <Button className="custom-button">
                Save
            </Button>
        );

        // -------------------------------------------------------------
        // Verify that the custom class was added while
        // preserving the Button component's default classes.
        // -------------------------------------------------------------
        expect(
            screen.getByRole(
                "button",
                { name: "Save" }
            )
        ).toHaveClass("custom-button");

    });

});