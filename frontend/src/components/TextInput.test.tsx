import { describe, expect, test, vi } from "vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import TextInput from "./TextInput";

afterEach(() => {
    cleanup();
});

/*
    TextInput Tests

    Each test follows the same sequence:

    1. Render the component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify the component behaves as expected.
*/

describe("TextInput", () => {

    // Verify that the label is displayed.
    test("renders label", () => {

        // -------------------------------------------------------------
        // Render the TextInput component.
        //
        // This creates the component in a virtual browser so it can
        // be tested without opening a real browser window.
        // -------------------------------------------------------------
        render(
            <TextInput
                label="Weight"
                id="weight"
            />
        );

        // -------------------------------------------------------------
        // Search the rendered page for the text "Weight".
        //
        // If the label was rendered correctly, the element will be
        // found. Otherwise, the test will fail.
        // -------------------------------------------------------------
        expect(
            screen.getByText("Weight")
        ).toBeInTheDocument();

    });

    // Verify that the input displays the supplied value.
test("renders value", () => {

    // -------------------------------------------------------------
    // Render the TextInput component with an initial value.
    //
    // This simulates a parent component passing a value into
    // the TextInput through its props.
    // -------------------------------------------------------------
    render(
        <TextInput
            label="Weight"
            id="weight"
            value={80}
            onChange={() => {}}
        />
    );

    // -------------------------------------------------------------
    // Verify that the input displays the supplied value.
    //
    // If the component correctly passes the value prop to the
    // underlying HTML input element, "80" should be visible.
    // -------------------------------------------------------------
    expect(
        screen.getByDisplayValue("80")
    ).toBeInTheDocument();

});


    // Verify that the onChange callback is called.
    test("calls onChange", async () => {

        // -------------------------------------------------------------
        // Create a mock function that will be passed to the TextInput
        // as its onChange handler.
        // -------------------------------------------------------------
        const onChange = vi.fn();

        render(
            <TextInput
                label="Weight"
                id="weight"
                onChange={onChange}
            />
        );

        // -------------------------------------------------------------
        // Simulate the user typing into the input.
        // -------------------------------------------------------------
        const input = screen.getByLabelText("Weight");

        await userEvent.type(input, "82");

        // -------------------------------------------------------------
        // Verify that the onChange callback was called.
        // Typing two characters ("8" and "2") will call onChange twice,
        // so we simply verify that it was called at least once.
        // -------------------------------------------------------------
        expect(onChange).toHaveBeenCalled();

    });


    // Verify that HTML input props are passed through.
    test("supports placeholder", () => {

        // -------------------------------------------------------------
        // Render the TextInput with a placeholder.
        //
        // Since TextInput forwards all standard HTML input props,
        // the placeholder should be applied automatically.
        // -------------------------------------------------------------
        render(
            <TextInput
                label="Weight"
                id="weight"
                placeholder="Enter weight"
            />
        );

        // -------------------------------------------------------------
        // Verify that the placeholder is displayed on the input.
        // -------------------------------------------------------------
        expect(
            screen.getByPlaceholderText(
                "Enter weight"
            )
        ).toBeInTheDocument();

    });



    // Verify that the disabled prop is applied.
    test("supports disabled", () => {

        // -------------------------------------------------------------
        // Render the TextInput with the disabled prop.
        //
        // The underlying HTML input should also become disabled.
        // -------------------------------------------------------------
        render(
            <TextInput
                label="Weight"
                id="weight"
                disabled
            />
        );

        // -------------------------------------------------------------
        // Verify that the rendered input is disabled.
        // -------------------------------------------------------------
        expect(
            screen.getByLabelText("Weight")
        ).toBeDisabled();

    });

});