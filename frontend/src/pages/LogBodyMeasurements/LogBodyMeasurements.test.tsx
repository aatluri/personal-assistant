import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";

import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import LogBodyMeasurements from "./LogBodyMeasurements";

import { createEmptyBodyMeasurements } from "../../utils/createEmptyBodyMeasurements";

import * as healthApi from "../../api/health";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    LogBodyMeasurements Tests

    Each test follows the same sequence:

    1. Arrange the required mock data.
    2. Render the LogBodyMeasurements page.
    3. Simulate user interaction if needed.
    4. Verify that the page behaves as expected.

    The tests verify:
    - Body Measurements are loaded correctly.
    - Empty measurements are created when none exist.
    - Changes mark the page as dirty.
    - Saving calls the backend correctly.
    - Success and failure states are handled correctly.
    - Changing the selected date reloads the measurements.
*/

/*
    Mock the entire Health API module.

    Normally these functions would make real HTTP
    requests to the backend.

    During unit testing we don't want to call the
    real backend because:
    1. Tests should run quickly.
    2. Tests should be independent of the backend.
    3. We want complete control over the data that
       each API call returns.

    vi.mock() replaces the real implementations with
    mock functions (vi.fn()).

    These mock functions allow us to:
    - Choose what each API call returns.
    - Simulate failures.
    - Verify that the functions were called with
      the correct arguments.
*/
vi.mock("../../api/health", () => ({
    getBodyMeasurement: vi.fn(),
    saveBodyMeasurement: vi.fn(),
}));


/*
    Runs before every individual test.

    Each test should start with a completely clean
    environment so that one test cannot affect another.

    The steps performed are:

    1. Clear all mock history.

       This removes:
       - Previous function calls.
       - Previous call counts.
       - Previous arguments.

       It does NOT remove the mock implementation.

    2. Configure getBodyMeasurement().

       By default, whenever the page requests Body
       Measurements, return an empty
       BodyMeasurements object.

       Individual tests can override this default if
       they need different data.

    3. Configure saveBodyMeasurement().

       By default, saving succeeds.

       Returning a resolved Promise simulates a
       successful API request.

       Individual tests can override this behaviour
       to simulate failures using mockRejectedValue().
*/
beforeEach(() => {

    /*
        Reset all mock call history before
        every test.
    */
    vi.clearAllMocks();

    /*
        By default, loading Body Measurements
        returns an empty record.
    */
    vi.mocked(
        healthApi.getBodyMeasurement
    ).mockResolvedValue(
        createEmptyBodyMeasurements()
    );

    /*
        By default, saving Body Measurements
        succeeds.
    */
    vi.mocked(
        healthApi.saveBodyMeasurement
    ).mockResolvedValue(undefined);

});

describe("LogBodyMeasurements", () => {


    // Verify that the loading spinner is displayed while data is loading.
    test("shows loading spinner", () => {

        vi.mocked(
            healthApi.getBodyMeasurement
        ).mockImplementation(
            () => new Promise(() => {})
        );

        render(
            <LogBodyMeasurements />
        );

        expect(
            screen.getByText("Loading...")
        ).toBeInTheDocument();

    });


    // Verify that the page is rendered after loading completes.
    test("renders page after loading", async () => {

        render(
            <LogBodyMeasurements />
        );

        expect(
            await screen.findByText("Log Today")
        ).toBeInTheDocument();

        expect(
            screen.getByText("Body Measurements")
        ).toBeInTheDocument();

        expect(
            screen.getByText("Date")
        ).toBeInTheDocument();

    });


    // Verify that existing Body Measurements are loaded.
    test("loads existing measurements", async () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        bodyMeasurements.bodyFat = 18.5;
        bodyMeasurements.chest = 102;
        bodyMeasurements.notes = "Feeling stronger";

        vi.mocked(
            healthApi.getBodyMeasurement
        ).mockResolvedValue(
            bodyMeasurements
        );

        render(
            <LogBodyMeasurements />
        );

        expect(
            await screen.findByDisplayValue("18.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("102")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("Feeling stronger")
        ).toBeInTheDocument();

    });


    // Verify that empty measurements are created when none exist.
    test("creates empty measurements when none exist", async () => {

        vi.mocked(
            healthApi.getBodyMeasurement
        ).mockResolvedValue(null);

        render(
            <LogBodyMeasurements />
        );

        await screen.findByText("Body Measurements");

        expect(
            screen.getByLabelText("Body Fat (%)")
        ).toHaveValue(null);

        expect(
            screen.getByLabelText("Notes")
        ).toHaveValue("");

    });

    // Verify that the page initially shows the saved status.
    test("shows save status", async () => {

        render(
            <LogBodyMeasurements />
        );

        expect(
            await screen.findByText("✓ Saved")
        ).toBeInTheDocument();

    });


    // Verify that changing a measurement marks the page as dirty.
    test("marks page dirty when measurements change", async () => {

        render(
            <LogBodyMeasurements />
        );

        const bodyFat =
            await screen.findByLabelText("Body Fat (%)");

        fireEvent.change(
            bodyFat,
            {
                target: {
                    value: "18.5",
                },
            }
        );

        expect(
            screen.getByText("● Unsaved Changes")
        ).toBeInTheDocument();

    });


    // Verify that the Save button becomes enabled after a change.
    test("enables save button", async () => {

        render(
            <LogBodyMeasurements />
        );

        const saveButton =
            await screen.findByRole(
                "button",
                {
                    name: "✓ All Changes Saved",
                }
            );

        expect(saveButton).toBeDisabled();

        fireEvent.change(
            screen.getByLabelText("Body Fat (%)"),
            {
                target: {
                    value: "18.5",
                },
            }
        );

        expect(
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            )
        ).toBeEnabled();

    });

    // Verify that the page saves successfully.
    test("saves successfully", async () => {

        render(
            <LogBodyMeasurements />
        );

        fireEvent.change(
            await screen.findByLabelText("Body Fat (%)"),
            {
                target: {
                    value: "18.5",
                },
            }
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            )
        );

        await waitFor(() => {

            expect(
                healthApi.saveBodyMeasurement
            ).toHaveBeenCalledTimes(1);

        });

        expect(
            screen.getByText("✓ Saved")
        ).toBeInTheDocument();

    });


    // Verify that a failed save displays the failure state.
    test("handles save failure", async () => {

        vi.mocked(
            healthApi.saveBodyMeasurement
        ).mockRejectedValue(
            new Error("Save failed")
        );

        render(
            <LogBodyMeasurements />
        );

        fireEvent.change(
            await screen.findByLabelText("Body Fat (%)"),
            {
                target: {
                    value: "18.5",
                },
            }
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            )
        );

        expect(
            await screen.findByText(
                "⚠ Save Failed - Try Again"
            )
        ).toBeInTheDocument();

    });


    // Verify that selecting a different date reloads the measurements.
    test("reloads when date changes", async () => {

        render(
            <LogBodyMeasurements />
        );

        await screen.findByText("Body Measurements");

        expect(
            healthApi.getBodyMeasurement
        ).toHaveBeenCalledTimes(1);

        const dateInput =
            screen.getByDisplayValue(
                /\d{4}-\d{2}-\d{2}/
            );

        fireEvent.change(
            dateInput,
            {
                target: {
                    value: "2026-08-20",
                },
            }
        );

        await waitFor(() => {

            expect(
                healthApi.getBodyMeasurement
            ).toHaveBeenCalledTimes(2);

        });

    });

});