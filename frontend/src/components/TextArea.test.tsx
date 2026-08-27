import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";

import TextArea from "./TextArea";

afterEach(() => {
    cleanup();
});

/*
    TextArea Tests

    Each test follows the same sequence:

    1. Render the TextArea component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify that the TextArea behaves as expected.
*/

describe("TextArea", () => {

    // Verify that the label is displayed.
    test("renders label", () => {

        render(
            <TextArea
                label="Notes"
                id="notes"
            />
        );

        expect(
            screen.getByText("Notes")
        ).toBeInTheDocument();

    });


    // Verify that the textarea displays the supplied value.
    test("renders value", () => {

        render(
            <TextArea
                label="Notes"
                id="notes"
                value="Test notes"
                onChange={() => {}}
            />
        );

        expect(
            screen.getByDisplayValue("Test notes")
        ).toBeInTheDocument();

    });


    // Verify that the onChange callback is called when the user types.
    test("calls onChange", async () => {

        const onChange = vi.fn();

        render(
            <TextArea
                label="Notes"
                id="notes"
                onChange={onChange}
            />
        );

        const textArea =
            screen.getByLabelText("Notes");

        await userEvent.type(
            textArea,
            "Hello"
        );

        expect(onChange).toHaveBeenCalled();

    });


    // Verify that the placeholder prop is passed to the textarea.
    test("supports placeholder", () => {

        render(
            <TextArea
                label="Notes"
                id="notes"
                placeholder="Enter notes"
            />
        );

        expect(
            screen.getByPlaceholderText(
                "Enter notes"
            )
        ).toBeInTheDocument();

    });


    // Verify that the rows prop is passed to the textarea.
    test("supports rows", () => {

        render(
            <TextArea
                label="Notes"
                id="notes"
                rows={6}
            />
        );

        expect(
            screen.getByLabelText("Notes")
        ).toHaveAttribute(
            "rows",
            "6"
        );

    });


    // Verify that the disabled prop is applied.
    test("supports disabled", () => {

        render(
            <TextArea
                label="Notes"
                id="notes"
                disabled
            />
        );

        expect(
            screen.getByLabelText("Notes")
        ).toBeDisabled();

    });

});