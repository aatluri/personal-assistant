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

import LogHealthMetrics from "./LogHealthMetrics";

import {
    createEmptyHealthMetrics,
} from "../../utils/createEmptyHealthMetrics";

import * as healthMetricsApi from "../../api/healthMetrics";


/*
Clean up the rendered components after each test.

This ensures each test starts with
a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});


/*
LogHealthMetrics Tests

Each test follows the same sequence:

1. Arrange the required mock data.
2. Render the LogHealthMetrics page.
3. Simulate user interaction if needed.
4. Verify that the page behaves as expected.

The tests verify:
- Health Metrics are loaded correctly.
- Empty Health Metrics are created when none exist.
- Changes mark the page as dirty.
- Saving calls the backend correctly.
- Success and failure states are handled correctly.
- Changing the selected date reloads Health Metrics.
- Load failures display an error message.
*/


/*
Mock the Health Metrics API module.

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
vi.mock("../../api/healthMetrics", () => ({
    getHealthMetric: vi.fn(),
    saveHealthMetric: vi.fn(),
}));


/*
Runs before every individual test.

Each test should start with a completely clean
environment so that one test cannot affect another.

The steps performed are:

1. Clear all mock history.

2. Configure getHealthMetric().

   By default, whenever the page requests Health
   Metrics, return an empty HealthMetrics object.

3. Configure saveHealthMetric().

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
    By default, loading Health Metrics
    returns an empty record.
    */
    vi.mocked(
        healthMetricsApi.getHealthMetric
    ).mockResolvedValue(
        createEmptyHealthMetrics()
    );


    /*
    By default, saving Health Metrics
    succeeds.
    */
    vi.mocked(
        healthMetricsApi.saveHealthMetric
    ).mockResolvedValue(undefined);

});


describe("LogHealthMetrics", () => {

    /*
    Verify that the loading spinner is displayed
    while Health Metrics are loading.
    */
    test("shows loading spinner", () => {

        /*
        Return a Promise that never resolves.

        This keeps the page permanently in its
        loading state for this test.
        */
        vi.mocked(
            healthMetricsApi.getHealthMetric
        ).mockImplementation(
            () => new Promise(() => {})
        );


        render(
            <LogHealthMetrics />
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
            <LogHealthMetrics />
        );


        expect(
            await screen.findByText("Log Today")
        ).toBeInTheDocument();


        expect(
            screen.getByText("Health Metrics")
        ).toBeInTheDocument();


        expect(
            screen.getByText("Date")
        ).toBeInTheDocument();

    });


    /*
    Verify that existing Health Metrics returned
    by the API are displayed on the page.
    */
    test("loads existing Health Metrics", async () => {

        const healthMetrics =
            createEmptyHealthMetrics();


        healthMetrics.stepCount = 10000;

        healthMetrics.activeEnergyKcal = 650;

        healthMetrics.restingHeartRateBpm = 52;

        healthMetrics.bloodOxygenSaturationPercent = 98;

        healthMetrics.source = "Apple Health";


        vi.mocked(
            healthMetricsApi.getHealthMetric
        ).mockResolvedValue(
            healthMetrics
        );


        render(
            <LogHealthMetrics />
        );


        expect(
            await screen.findByLabelText(
                "Step Count"
            )
        ).toHaveValue(10000);


        expect(
            screen.getByLabelText(
                "Active Energy (kcal)"
            )
        ).toHaveValue(650);


        expect(
            screen.getByLabelText(
                "Resting Heart Rate (bpm)"
            )
        ).toHaveValue(52);


        expect(
            screen.getByLabelText(
                "Blood Oxygen Saturation (%)"
            )
        ).toHaveValue(98);


        expect(
            screen.getByLabelText("Source")
        ).toHaveValue("Apple Health");

    });


    /*
    Verify that empty Health Metrics are created
    when no record exists for the selected date.
    */
    test("creates empty Health Metrics when none exist", async () => {

        vi.mocked(
            healthMetricsApi.getHealthMetric
        ).mockResolvedValue(null);


        render(
            <LogHealthMetrics />
        );


        await screen.findByText(
            "Health Metrics"
        );


        expect(
            screen.getByLabelText(
                "Step Count"
            )
        ).toHaveValue(null);


        expect(
            screen.getByLabelText(
                "Resting Heart Rate (bpm)"
            )
        ).toHaveValue(null);


        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toHaveValue("");

    });


    /*
    Verify that the page initially shows
    the saved status.
    */
    test("shows save status", async () => {

        render(
            <LogHealthMetrics />
        );


        expect(
            await screen.findByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that changing a Health Metric
    marks the page as having unsaved changes.
    */
    test("marks page dirty when Health Metrics change", async () => {

        render(
            <LogHealthMetrics />
        );


        const stepCount =
            await screen.findByLabelText(
                "Step Count"
            );


        fireEvent.change(
            stepCount,
            {
                target: {
                    value: "10000",
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
    enabled after a Health Metric changes.
    */
    test("enables save button", async () => {

        render(
            <LogHealthMetrics />
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
                "Step Count"
            ),
            {
                target: {
                    value: "10000",
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
    Verify that Health Metrics are saved
    successfully after the user makes a change.
    */
    test("saves successfully", async () => {

        render(
            <LogHealthMetrics />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Step Count"
            ),
            {
                target: {
                    value: "10000",
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
                healthMetricsApi.saveHealthMetric
            ).toHaveBeenCalledTimes(1);

        });


        expect(
            screen.getByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that saveHealthMetric receives
    the selected date and the updated
    HealthMetrics object.
    */
    test("sends updated Health Metrics when saving", async () => {

        render(
            <LogHealthMetrics />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Step Count"
            ),
            {
                target: {
                    value: "12000",
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
                healthMetricsApi.saveHealthMetric
            ).toHaveBeenCalledTimes(1);

        });


        const saveCall =
            vi.mocked(
                healthMetricsApi.saveHealthMetric
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
        the updated Health Metrics state.
        */
        expect(
            saveCall[1].stepCount
        ).toBe(12000);

    });


    /*
    Verify that a failed save displays
    the failure state.
    */
    test("handles save failure", async () => {

        vi.mocked(
            healthMetricsApi.saveHealthMetric
        ).mockRejectedValue(
            new Error("Save failed")
        );


        render(
            <LogHealthMetrics />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Step Count"
            ),
            {
                target: {
                    value: "10000",
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
    reloads Health Metrics for that date.
    */
    test("reloads when date changes", async () => {

        render(
            <LogHealthMetrics />
        );


        await screen.findByText(
            "Health Metrics"
        );


        expect(
            healthMetricsApi.getHealthMetric
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
                healthMetricsApi.getHealthMetric
            ).toHaveBeenCalledTimes(2);

        });


        /*
        Verify that the second request uses
        the newly selected date.
        */
        expect(
            healthMetricsApi.getHealthMetric
        ).toHaveBeenLastCalledWith(
            "2026-08-20"
        );

    });


    /*
    Verify that a loading failure displays
    the load error message.

    This is different from a 404/no-record
    response. A load failure means the API
    request itself failed.
    */
    test("shows load error when Health Metrics fail to load", async () => {

        vi.mocked(
            healthMetricsApi.getHealthMetric
        ).mockRejectedValue(
            new Error("Load failed")
        );


        render(
            <LogHealthMetrics />
        );


        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

    });

});