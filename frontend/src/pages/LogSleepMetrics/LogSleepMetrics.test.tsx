
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

import LogSleepMetrics from "./LogSleepMetrics";

import {
    createEmptySleepMetrics,
} from "../../utils/createEmptySleepMetrics";

import * as sleepMetricsApi from "../../api/sleepMetrics";


/*
Clean up after every test.
*/
afterEach(() => {
    cleanup();
});


/*
Mock the Sleep Metrics API.

No real backend requests will be made
during these tests.
*/
vi.mock("../../api/sleepMetrics", () => ({
    getSleepMetric: vi.fn(),
    saveSleepMetric: vi.fn(),
}));


/*
Configure default API behaviour
before every test.
*/
beforeEach(() => {

    /*
    Remove previous mock call history.
    */
    vi.clearAllMocks();


    /*
    By default, loading succeeds and
    returns an empty Sleep Metrics record.
    */
    vi.mocked(
        sleepMetricsApi.getSleepMetric
    ).mockResolvedValue(
        createEmptySleepMetrics()
    );


    /*
    By default, saving succeeds.
    */
    vi.mocked(
        sleepMetricsApi.saveSleepMetric
    ).mockResolvedValue(undefined);

});


describe("LogSleepMetrics", () => {

    /*
    Verify that the loading spinner is shown
    while Sleep Metrics are loading.
    */
    test("shows loading spinner", () => {

        /*
        Return a Promise that never resolves
        so the page remains in loading state.
        */
        vi.mocked(
            sleepMetricsApi.getSleepMetric
        ).mockImplementation(
            () => new Promise(() => {})
        );


        render(
            <LogSleepMetrics />
        );


        expect(
            screen.getByText("Loading...")
        ).toBeInTheDocument();

    });


    /*
    Verify that the page renders after
    loading completes.
    */
    test("renders page after loading", async () => {

        render(
            <LogSleepMetrics />
        );


        expect(
            await screen.findByText("Log Today")
        ).toBeInTheDocument();


        expect(
            screen.getByText("Sleep Metrics")
        ).toBeInTheDocument();


        expect(
            screen.getByText("Date")
        ).toBeInTheDocument();

    });


    /*
    Verify that existing Sleep Metrics returned
    by the API are displayed correctly.
    */
    test("loads existing Sleep Metrics", async () => {

        const sleepMetrics =
            createEmptySleepMetrics();


        sleepMetrics.sleepStartTime =
            "2026-08-26T23:15";

        sleepMetrics.sleepEndTime =
            "2026-08-27T07:15";

        sleepMetrics.totalSleepDurationHr = 8;

        sleepMetrics.deepSleepHr = 1.5;

        sleepMetrics.source = "Apple Health";


        vi.mocked(
            sleepMetricsApi.getSleepMetric
        ).mockResolvedValue(
            sleepMetrics
        );


        render(
            <LogSleepMetrics />
        );


        expect(
            await screen.findByLabelText(
                "Sleep Start Time"
            )
        ).toHaveValue(
            "2026-08-26T23:15"
        );


        expect(
            screen.getByLabelText(
                "Sleep End Time"
            )
        ).toHaveValue(
            "2026-08-27T07:15"
        );


        expect(
            screen.getByLabelText(
                "Total Sleep Duration (hr)"
            )
        ).toHaveValue(8);


        expect(
            screen.getByLabelText(
                "Deep Sleep (hr)"
            )
        ).toHaveValue(1.5);


        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toHaveValue(
            "Apple Health"
        );

    });


    /*
    Verify that empty Sleep Metrics are
    created when no record exists.
    */
    test("creates empty Sleep Metrics when none exist", async () => {

        vi.mocked(
            sleepMetricsApi.getSleepMetric
        ).mockResolvedValue(null);


        render(
            <LogSleepMetrics />
        );


        await screen.findByText(
            "Sleep Metrics"
        );


        expect(
            screen.getByLabelText(
                "Sleep Start Time"
            )
        ).toHaveValue("");


        expect(
            screen.getByLabelText(
                "Total Sleep Duration (hr)"
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
            <LogSleepMetrics />
        );


        expect(
            await screen.findByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that changing a Sleep Metric
    marks the page as dirty.
    */
    test("marks page dirty when Sleep Metrics change", async () => {

        render(
            <LogSleepMetrics />
        );


        const totalSleepDuration =
            await screen.findByLabelText(
                "Total Sleep Duration (hr)"
            );


        fireEvent.change(
            totalSleepDuration,
            {
                target: {
                    value: "8",
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
    Verify that the Save button starts disabled
    and becomes enabled after a change.
    */
    test("enables save button", async () => {

        render(
            <LogSleepMetrics />
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
                "Total Sleep Duration (hr)"
            ),
            {
                target: {
                    value: "8",
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
    Verify that Sleep Metrics can
    be saved successfully.
    */
    test("saves successfully", async () => {

        render(
            <LogSleepMetrics />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Total Sleep Duration (hr)"
            ),
            {
                target: {
                    value: "8",
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
                sleepMetricsApi.saveSleepMetric
            ).toHaveBeenCalledTimes(1);

        });


        expect(
            screen.getByText(
                "✓ Saved"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that saveSleepMetric receives
    the selected date and the updated
    SleepMetrics object.
    */
    test("sends updated Sleep Metrics when saving", async () => {

        render(
            <LogSleepMetrics />
        );


        /*
        Change the sleep start time.

        This is particularly useful for Sleep
        because the full datetime must be
        preserved rather than rebuilding it
        from the selected date.
        */
        fireEvent.change(
            await screen.findByLabelText(
                "Sleep Start Time"
            ),
            {
                target: {
                    value: "2026-08-26T23:15",
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
                sleepMetricsApi.saveSleepMetric
            ).toHaveBeenCalledTimes(1);

        });


        const saveCall =
            vi.mocked(
                sleepMetricsApi.saveSleepMetric
            ).mock.calls[0];


        /*
        First argument should contain
        the selected date.
        */
        expect(
            saveCall[0]
        ).toMatch(
            /^\d{4}-\d{2}-\d{2}$/
        );


        /*
        Second argument should preserve
        the full sleep-start datetime.
        */
        expect(
            saveCall[1].sleepStartTime
        ).toBe(
            "2026-08-26T23:15"
        );

    });


    /*
    Verify that a failed save displays
    the save failure state.
    */
    test("handles save failure", async () => {

        vi.mocked(
            sleepMetricsApi.saveSleepMetric
        ).mockRejectedValue(
            new Error("Save failed")
        );


        render(
            <LogSleepMetrics />
        );


        fireEvent.change(
            await screen.findByLabelText(
                "Total Sleep Duration (hr)"
            ),
            {
                target: {
                    value: "8",
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
    Verify that changing the selected date
    reloads Sleep Metrics.
    */
    test("reloads when date changes", async () => {

        render(
            <LogSleepMetrics />
        );


        await screen.findByText(
            "Sleep Metrics"
        );


        /*
        Initial page load should make
        one API request.
        */
        expect(
            sleepMetricsApi.getSleepMetric
        ).toHaveBeenCalledTimes(1);


        /*
        Find the selected date input.
        */
        const dateInput =
            screen.getByDisplayValue(
                /^\d{4}-\d{2}-\d{2}$/
            );


        /*
        Change the selected date.
        */
        fireEvent.change(
            dateInput,
            {
                target: {
                    value: "2026-08-20",
                },
            }
        );


        /*
        Changing selectedDate should trigger
        the useEffect again.
        */
        await waitFor(() => {

            expect(
                sleepMetricsApi.getSleepMetric
            ).toHaveBeenCalledTimes(2);

        });


        /*
        Verify that Sleep Metrics were requested
        for the new selected date.
        */
        expect(
            sleepMetricsApi.getSleepMetric
        ).toHaveBeenLastCalledWith(
            "2026-08-20"
        );

    });


    /*
    Verify that an API loading failure
    displays the load error message.
    */
    test("shows load error when Sleep Metrics fail to load", async () => {

        vi.mocked(
            sleepMetricsApi.getSleepMetric
        ).mockRejectedValue(
            new Error("Load failed")
        );


        render(
            <LogSleepMetrics />
        );


        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

    });

});