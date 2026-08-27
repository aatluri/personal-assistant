import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";
import Select from "./Select";

afterEach(() => {
    cleanup();
});

/*
    Select Tests

    Each test follows the same sequence:

    1. Render the Select component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify that the Select behaves as expected.
*/

describe("Select", () => {

    // Verify that the label is displayed.
    test("renders label", () => {

        render(
            <Select
                label="Workout Type"
                id="workout-type"
            >
                <option value="HIIT">HIIT</option>
            </Select>
        );

        expect(
            screen.getByText("Workout Type")
        ).toBeInTheDocument();

    });


    // Verify that the supplied options are displayed.
    test("renders options", () => {

        render(
            <Select
                label="Workout Type"
                id="workout-type"
            >
                <option value="HIIT">HIIT</option>
                <option value="Strength">Strength</option>
            </Select>
        );

        expect(
            screen.getByRole("option", { name: "HIIT" })
        ).toBeInTheDocument();

        expect(
            screen.getByRole("option", { name: "Strength" })
        ).toBeInTheDocument();

    });


    // Verify that the supplied value is selected.
    test("renders selected value", () => {

        render(
            <Select
                label="Workout Type"
                id="workout-type"
                value="Strength"
                onChange={() => {}}
            >
                <option value="HIIT">HIIT</option>
                <option value="Strength">Strength</option>
            </Select>
        );

        expect(
            screen.getByDisplayValue("Strength")
        ).toBeInTheDocument();

    });


    // Verify that the onChange callback is called.
    test("calls onChange", async () => {

        const onChange = vi.fn();

        render(
            <Select
                label="Workout Type"
                id="workout-type"
                onChange={onChange}
            >
                <option value="HIIT">HIIT</option>
                <option value="Strength">Strength</option>
            </Select>
        );

        await userEvent.selectOptions(
            screen.getByLabelText("Workout Type"),
            "Strength"
        );

        expect(onChange).toHaveBeenCalled();

    });


    // Verify that the disabled prop is applied.
    test("supports disabled", () => {

        render(
            <Select
                label="Workout Type"
                id="workout-type"
                disabled
            >
                <option value="HIIT">HIIT</option>
            </Select>
        );

        expect(
            screen.getByLabelText("Workout Type")
        ).toBeDisabled();

    });


    // Verify that standard HTML select props are passed through.
    test("supports required", () => {

        render(
            <Select
                label="Workout Type"
                id="workout-type"
                required
            >
                <option value="HIIT">HIIT</option>
            </Select>
        );

        expect(
            screen.getByLabelText("Workout Type")
        ).toBeRequired();

    });

});