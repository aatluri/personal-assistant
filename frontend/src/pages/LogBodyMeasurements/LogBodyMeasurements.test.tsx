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

import {
    createEmptyBodyMeasurements,
} from "../../utils/createEmptyBodyMeasurements";

import * as bodyMeasurementApi from "../../api/bodyMeasurements";


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
- The Save button responds correctly to changes.
- Saving calls the backend correctly.
- Success and failure states are handled correctly.
- Changing the selected date reloads the measurements.
- Load failures display an error message.
*/


/*
Mock the Body Measurements API module.

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
vi.mock("../../api/bodyMeasurements", () => ({
    getBodyMeasurement: vi.fn(),
    saveBodyMeasurement: vi.fn(),
}));


/*
Runs before every individual test.

Each test should start with a completely clean
environment so that one test cannot affect another.

The steps performed are:

1. Clear all mock history.

2. Configure getBodyMeasurement().

   By default, whenever the page requests Body
   Measurements, return an empty
   BodyMeasurements object.

3. Configure saveBodyMeasurement().

   By default, saving succeeds.

Individual tests can override these defaults.
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
        bodyMeasurementApi.getBodyMeasurement
    ).mockResolvedValue(
        createEmptyBodyMeasurements()
    );


    /*
    By default, saving Body Measurements
    succeeds.
    */
    vi.mocked(
        bodyMeasurementApi.saveBodyMeasurement
    ).mockResolvedValue(undefined);

});


describe("LogBodyMeasurements", () => {

    /*
    Verify that the loading spinner is displayed
    while Body Measurements are loading.
    */
    test("shows loading spinner", () => {

        /*
        Return a Promise that never resolves.

        This keeps the page permanently in its
        loading state for this test.
        */
        vi.mocked(
            bodyMeasurementApi.getBodyMeasurement
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


    /*
    Verify that the page is rendered after
    loading completes.
    */
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


    /*
    Verify that existing Body Measurements returned
    by the API are displayed on the page.
    */
    test("loads existing measurements", async () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();


        bodyMeasurements.weight = 80.2;

        bodyMeasurements.bodyMassIndex = 26.8;

        bodyMeasurements.bodyFat = 18.5;

        bodyMeasurements.chest = 102;

        bodyMeasurements.notes = "Feeling stronger";


        vi.mocked(
            bodyMeasurementApi.getBodyMeasurement
        ).mockResolvedValue(
            bodyMeasurements
        );


        render(
            <LogBodyMeasurements />
        );


        expect(
            await screen.findByLabelText(
                "Weight (kg)"
            )
        ).toHaveValue(80.2);


        expect(
            screen.getByLabelText(
                "Body Mass Index (BMI)"
            )
        ).toHaveValue(26.8);


        expect(
            screen.getByLabelText(
                "Body Fat (%)"
            )
        ).toHaveValue(18.5);


        expect(
            screen.getByLabelText(
                "Chest (cm)"
            )
        ).toHaveValue(102);


        expect(
            screen.getByLabelText(
                "Notes"
            )
        ).toHaveValue("Feeling stronger");

    });


    /*
    Verify that empty Body Measurements are created
    when no record exists for the selected date.
    */
    test("creates empty measurements when none exist", async () => {

        vi.mocked(
            bodyMeasurementApi.getBodyMeasurement
        ).mockResolvedValue(null);


        render(
            <LogBodyMeasurements />
        );


        await screen.findByText(
            "Body Measurements"
        );


        expect(
            screen.getByLabelText(
                "Body Fat (%)"
            )
        ).toHaveValue(null);


        expect(
            screen.getByLabelText(
                "Notes"
            )
        ).toHaveValue("");

    });


    /*
    Verify that the page initially shows
    the saved status.
    */
    test("shows save status", async () => {

        render(
            <LogBodyMeasurements />
        );


        expect(
            await screen.findByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that changing a measurement
    marks the page as having unsaved changes.
    */
    test("marks page dirty when measurements change", async () => {

        render(
            <LogBodyMeasurements />
        );


        const bodyFat =
            await screen.findByLabelText(
                "Body Fat (%)"
            );


        fireEvent.change(
            bodyFat,
            {
                target: {
                    value: "18.5",
                },
            }
        );


        expect(
            screen.getByText(
                "● Unsaved Changes"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that the Save button is disabled
    when there are no changes and becomes
    enabled after a measurement changes.
    */
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


        expect(
            saveButton
        ).toBeDisabled();


        fireEvent.change(
            screen.getByLabelText(
                "Body Fat (%)"
            ),
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


    /*
    Verify that Body Measurements are saved
    successfully after the user makes a change.
    */
    test("saves successfully", async () => {

        render(
            <LogBodyMeasurements />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Body Fat (%)"
            ),
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
                bodyMeasurementApi.saveBodyMeasurement
            ).toHaveBeenCalledTimes(1);

        });


        expect(
            screen.getByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that saveBodyMeasurement receives
    the selected date and the updated
    BodyMeasurements object.
    */
    test("sends updated Body Measurements when saving", async () => {

        render(
            <LogBodyMeasurements />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Body Fat (%)"
            ),
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
                bodyMeasurementApi.saveBodyMeasurement
            ).toHaveBeenCalledTimes(1);

        });


        const saveCall =
            vi.mocked(
                bodyMeasurementApi.saveBodyMeasurement
            ).mock.calls[0];


        /*
        First argument should be the
        currently selected date.
        */
        expect(
            saveCall[0]
        ).toMatch(
            /^\d{4}-\d{2}-\d{2}$/
        );


        /*
        Second argument should contain
        the updated Body Measurements state.
        */
        expect(
            saveCall[1].bodyFat
        ).toBe(18.5);

    });


    /*
    Verify that a failed save displays
    the failure state.
    */
    test("handles save failure", async () => {

        vi.mocked(
            bodyMeasurementApi.saveBodyMeasurement
        ).mockRejectedValue(
            new Error("Save failed")
        );


        render(
            <LogBodyMeasurements />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Body Fat (%)"
            ),
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


    /*
    Verify that selecting a different date
    reloads Body Measurements for that date.
    */
    test("reloads when date changes", async () => {

        render(
            <LogBodyMeasurements />
        );


        await screen.findByText(
            "Body Measurements"
        );


        expect(
            bodyMeasurementApi.getBodyMeasurement
        ).toHaveBeenCalledTimes(1);


        /*
        The DateSection contains a date input.

        Its value is initially today's date.
        */
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
                bodyMeasurementApi.getBodyMeasurement
            ).toHaveBeenCalledTimes(2);

        });


        /*
        Verify that the second request uses
        the newly selected date.
        */
        expect(
            bodyMeasurementApi.getBodyMeasurement
        ).toHaveBeenLastCalledWith(
            "2026-08-20"
        );

    });


    /*
    Verify that a loading failure displays
    the load error message.

    This is different from a no-record response.

    A no-record response returns null and displays
    empty fields.

    A load failure means the API request itself
    failed.
    */
    test("shows load error when Body Measurements fail to load", async () => {

        vi.mocked(
            bodyMeasurementApi.getBodyMeasurement
        ).mockRejectedValue(
            new Error("Load failed")
        );


        render(
            <LogBodyMeasurements />
        );


        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

    });

});