import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { afterEach, describe, expect, test, vi } from "vitest";

import SaveButton from "./SaveButton";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    SaveButton Tests

    Each test follows the same sequence:

    1. Render the SaveButton component.
    2. Provide any required props.
    3. Simulate user interaction if needed.
    4. Verify that the SaveButton behaves as expected.
*/

describe("SaveButton", () => {

    // Verify that the default button text is displayed.
    test("renders default button text", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={true}
                saveStatus="idle"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "Save Changes" }
            )
        ).toBeInTheDocument();

    });


    // Verify that the saving text is displayed.
    test("renders saving text", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={true}
                saveStatus="saving"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "Saving..." }
            )
        ).toBeInTheDocument();

    });


    // Verify that the saved text is displayed.
    test("renders saved text", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={false}
                saveStatus="saved"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "✓ All Changes Saved" }
            )
        ).toBeInTheDocument();

    });


    // Verify that the failed text is displayed.
    test("renders failed text", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={false}
                saveStatus="failed"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "⚠ Save Failed - Try Again" }
            )
        ).toBeInTheDocument();

    });


    // Verify that clicking the button calls the supplied callback.
    test("calls onClick", async () => {

        const onClick = vi.fn();

        render(
            <SaveButton
                onClick={onClick}
                isDirty={true}
                saveStatus="idle"
            />
        );

        await userEvent.click(
            screen.getByRole(
                "button",
                { name: "Save Changes" }
            )
        );

        expect(onClick).toHaveBeenCalledTimes(1);

    });


    // Verify that the button is disabled while saving.
    test("disables button while saving", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={true}
                saveStatus="saving"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "Saving..." }
            )
        ).toBeDisabled();

    });


    // Verify that the button is disabled when there are no unsaved changes.
    test("disables button when there are no unsaved changes", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={false}
                saveStatus="saved"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "✓ All Changes Saved" }
            )
        ).toBeDisabled();

    });


    // Verify that the user can retry after a failed save.
    test("allows retry after failed save", () => {

        render(
            <SaveButton
                onClick={() => {}}
                isDirty={false}
                saveStatus="failed"
            />
        );

        expect(
            screen.getByRole(
                "button",
                { name: "⚠ Save Failed - Try Again" }
            )
        ).not.toBeDisabled();

    });

});