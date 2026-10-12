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

import LogWorkoutMetrics from "./LogWorkoutMetrics";

import {
    createEmptyWorkoutMetrics,
} from "../../utils/createEmptyWorkoutMetrics";

import * as workoutMetricsApi from "../../api/workoutMetrics";


vi.mock("../../api/workoutMetrics", () => ({
    getWorkoutMetricsByDate: vi.fn(),
    saveWorkoutMetric: vi.fn(),
}));


afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
});


beforeEach(() => {

    vi.clearAllMocks();

    vi.mocked(
        workoutMetricsApi.getWorkoutMetricsByDate
    ).mockResolvedValue([]);

    vi.mocked(
        workoutMetricsApi.saveWorkoutMetric
    ).mockResolvedValue(undefined);

});


describe("LogWorkoutMetrics", () => {

    test("shows loading spinner", () => {

        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockImplementation(
            () => new Promise(() => {})
        );

        render(
            <LogWorkoutMetrics />
        );

        expect(
            screen.getByText("Loading...")
        ).toBeInTheDocument();

    });


    test("renders page after loading", async () => {

        render(
            <LogWorkoutMetrics />
        );

        expect(
            await screen.findByText("Log Today")
        ).toBeInTheDocument();

        expect(
            screen.getByText("Workouts")
        ).toBeInTheDocument();

        expect(
            screen.getByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            )
        ).toBeInTheDocument();

    });


    test("shows empty state when no workouts exist", async () => {

        render(
            <LogWorkoutMetrics />
        );

        expect(
            await screen.findByText(
                "No workouts recorded for this date."
            )
        ).toBeInTheDocument();

        expect(
            screen.queryByLabelText(
                "Workout Type"
            )
        ).not.toBeInTheDocument();

    });


    test("loads and selects an existing workout", async () => {

        const workout =
            createEmptyWorkoutMetrics();

        workout.date = "2026-08-27";
        workout.workoutType = "Running";
        workout.workoutStartTime = "07:00";
        workout.workoutEndTime = "08:00";
        workout.workoutDuration = "1:00:00";
        workout.totalEnergyKcal = 650;

        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockResolvedValue([
            workout,
        ]);

        render(
            <LogWorkoutMetrics />
        );

        expect(
            await screen.findByText(
                "Running"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Workout Type"
            )
        ).toHaveValue("Running");

        expect(
            screen.getByLabelText(
                "Workout Start Time"
            )
        ).toHaveValue("07:00");

        expect(
            screen.getByLabelText(
                "Total Energy (kcal)"
            )
        ).toHaveValue("650");

    });


    test("displays multiple workouts for the same date", async () => {

        const morningWorkout =
            createEmptyWorkoutMetrics();

        morningWorkout.date = "2026-08-27";
        morningWorkout.workoutType = "Running";
        morningWorkout.workoutStartTime = "07:00";
        morningWorkout.workoutEndTime = "08:00";
        morningWorkout.workoutDuration = "1:00:00";


        const eveningWorkout =
            createEmptyWorkoutMetrics();

        eveningWorkout.date = "2026-08-27";
        eveningWorkout.workoutType =
            "Strength Training";

        eveningWorkout.workoutStartTime =
            "18:00";

        eveningWorkout.workoutEndTime =
            "19:00";

        eveningWorkout.workoutDuration =
            "1:00:00";


        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockResolvedValue([
            morningWorkout,
            eveningWorkout,
        ]);

        render(
            <LogWorkoutMetrics />
        );

        expect(
            await screen.findByText(
                "Running"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByText(
                "Strength Training"
            )
        ).toBeInTheDocument();

    });


    test("selects another workout", async () => {

        const morningWorkout =
            createEmptyWorkoutMetrics();

        morningWorkout.workoutType = "Running";
        morningWorkout.workoutStartTime = "07:00";
        morningWorkout.workoutEndTime = "08:00";
        morningWorkout.workoutDuration = "1:00:00";


        const eveningWorkout =
            createEmptyWorkoutMetrics();

        eveningWorkout.workoutType =
            "Strength Training";

        eveningWorkout.workoutStartTime =
            "18:00";

        eveningWorkout.workoutEndTime =
            "19:00";

        eveningWorkout.workoutDuration =
            "1:00:00";


        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockResolvedValue([
            morningWorkout,
            eveningWorkout,
        ]);

        render(
            <LogWorkoutMetrics />
        );

        expect(
            await screen.findByLabelText(
                "Workout Type"
            )
        ).toHaveValue("Running");

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: /Strength Training/i,
                }
            )
        );

        expect(
            screen.getByLabelText(
                "Workout Type"
            )
        ).toHaveValue(
            "Strength Training"
        );

        expect(
            screen.getByLabelText(
                "Workout Start Time"
            )
        ).toHaveValue("18:00");

    });


    test("adds a new workout", async () => {

        render(
            <LogWorkoutMetrics />
        );

        const addButton =
            await screen.findByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            );

        fireEvent.click(
            addButton
        );

        expect(
            screen.getByLabelText(
                "Workout Type"
            )
        ).toHaveValue("");

        expect(
            screen.getByLabelText(
                "Workout Start Time"
            )
        ).toHaveValue("");

        expect(
            screen.getByText(
                "● Unsaved Changes"
            )
        ).toBeInTheDocument();

        /*
        Adding a workout should also move
        the Save button into its dirty state.
        */
        expect(
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            )
        ).toBeEnabled();

    });


    test("marks page dirty when workout changes", async () => {

        const workout =
            createEmptyWorkoutMetrics();

        workout.workoutType = "Running";
        workout.workoutStartTime = "07:00";
        workout.workoutEndTime = "08:00";
        workout.workoutDuration = "1:00:00";

        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockResolvedValue([
            workout,
        ]);

        render(
            <LogWorkoutMetrics />
        );

        fireEvent.change(
            await screen.findByLabelText(
                "Workout Type"
            ),
            {
                target: {
                    value: "Cycling",
                },
            }
        );

        expect(
            screen.getByText(
                "● Unsaved Changes"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            )
        ).toBeEnabled();

    });


    test("requires Workout Start Time before saving", async () => {

        const alertMock =
            vi.spyOn(
                window,
                "alert"
            ).mockImplementation(() => {});

        render(
            <LogWorkoutMetrics />
        );

        fireEvent.click(
            await screen.findByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            )
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
            alertMock
        ).toHaveBeenCalledWith(
            "Please enter a Workout Start Time."
        );

        expect(
            workoutMetricsApi.saveWorkoutMetric
        ).not.toHaveBeenCalled();

    });


    test("requires Workout End Time before saving", async () => {

        const alertMock =
            vi.spyOn(
                window,
                "alert"
            ).mockImplementation(() => {});

        render(
            <LogWorkoutMetrics />
        );

        fireEvent.click(
            await screen.findByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            )
        );

        fireEvent.change(
            screen.getByLabelText(
                "Workout Start Time"
            ),
            {
                target: {
                    value: "07:00",
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
            alertMock
        ).toHaveBeenCalledWith(
            "Please enter a Workout End Time."
        );

        expect(
            workoutMetricsApi.saveWorkoutMetric
        ).not.toHaveBeenCalled();

    });


    test("requires Workout Duration before saving", async () => {

        const alertMock =
            vi.spyOn(
                window,
                "alert"
            ).mockImplementation(() => {});

        render(
            <LogWorkoutMetrics />
        );

        fireEvent.click(
            await screen.findByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            )
        );

        fireEvent.change(
            screen.getByLabelText(
                "Workout Start Time"
            ),
            {
                target: {
                    value: "07:00",
                },
            }
        );

        fireEvent.change(
            screen.getByLabelText(
                "Workout End Time"
            ),
            {
                target: {
                    value: "08:00",
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
            alertMock
        ).toHaveBeenCalledWith(
            "Please enter a Workout Duration."
        );

        expect(
            workoutMetricsApi.saveWorkoutMetric
        ).not.toHaveBeenCalled();

    });


    test("saves workout and reloads workouts", async () => {

        /*
        The first API response is used when
        the page initially loads.

        The second API response is used when
        workouts are reloaded after saving.
        */
        const savedWorkout =
            createEmptyWorkoutMetrics();

        savedWorkout.workoutType = "Running";
        savedWorkout.workoutStartTime = "07:00";
        savedWorkout.workoutEndTime = "08:00";
        savedWorkout.workoutDuration = "1:00:00";


        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        )
            .mockResolvedValueOnce([])
            .mockResolvedValueOnce([
                savedWorkout,
            ]);


        render(
            <LogWorkoutMetrics />
        );


        fireEvent.click(
            await screen.findByRole(
                "button",
                {
                    name: /Add Workout/i,
                }
            )
        );


        fireEvent.change(
            screen.getByLabelText(
                "Workout Type"
            ),
            {
                target: {
                    value: "Running",
                },
            }
        );


        fireEvent.change(
            screen.getByLabelText(
                "Workout Start Time"
            ),
            {
                target: {
                    value: "07:00",
                },
            }
        );


        fireEvent.change(
            screen.getByLabelText(
                "Workout End Time"
            ),
            {
                target: {
                    value: "08:00",
                },
            }
        );


        fireEvent.change(
            screen.getByLabelText(
                "Workout Duration"
            ),
            {
                target: {
                    value: "1:00:00",
                },
            }
        );


        /*
        The workout is now dirty, so the
        Save button should be active.
        */
        const saveButton =
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            );

        expect(
            saveButton
        ).toBeEnabled();


        fireEvent.click(
            saveButton
        );


        await waitFor(() => {

            expect(
                workoutMetricsApi.saveWorkoutMetric
            ).toHaveBeenCalledTimes(1);

        });


        expect(
            workoutMetricsApi.saveWorkoutMetric
        ).toHaveBeenCalledWith(
            expect.objectContaining({
                workoutType: "Running",
                workoutStartTime: "07:00",
                workoutEndTime: "08:00",
                workoutDuration: "1:00:00",
            })
        );


        await waitFor(() => {

            expect(
                workoutMetricsApi.getWorkoutMetricsByDate
            ).toHaveBeenCalledTimes(2);

        });


        expect(
            screen.getByLabelText(
                "Workout Type"
            )
        ).toHaveValue("Running");


        /*
        A successful save should clear the
        dirty state.
        */
        expect(
            screen.queryByText(
                "● Unsaved Changes"
            )
        ).not.toBeInTheDocument();


        /*
        SaveButton uses this text when
        saveStatus is "saved".
        */
        expect(
            screen.getByRole(
                "button",
                {
                    name: "✓ All Changes Saved",
                }
            )
        ).toBeDisabled();

    });


    test("handles save failure", async () => {

        const alertMock =
            vi.spyOn(
                window,
                "alert"
            ).mockImplementation(() => {});


        const workout =
            createEmptyWorkoutMetrics();

        workout.workoutType = "Running";
        workout.workoutStartTime = "07:00";
        workout.workoutEndTime = "08:00";
        workout.workoutDuration = "1:00:00";


        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockResolvedValue([
            workout,
        ]);


        vi.mocked(
            workoutMetricsApi.saveWorkoutMetric
        ).mockRejectedValue(
            new Error("Save failed")
        );


        render(
            <LogWorkoutMetrics />
        );


        const workoutType =
            await screen.findByLabelText(
                "Workout Type"
            );


        fireEvent.change(
            workoutType,
            {
                target: {
                    value: "Morning Run",
                },
            }
        );


        /*
        Editing the workout should change
        saveStatus to "idle".
        */
        const saveButton =
            screen.getByRole(
                "button",
                {
                    name: "Save Changes",
                }
            );

        expect(
            saveButton
        ).toBeEnabled();


        fireEvent.click(
            saveButton
        );


        await waitFor(() => {

            expect(
                workoutMetricsApi.saveWorkoutMetric
            ).toHaveBeenCalledTimes(1);

        });


        await waitFor(() => {

            expect(
                alertMock
            ).toHaveBeenCalledWith(
                "Failed to save Workout Metrics."
            );

        });


        /*
        A failed save should use the failed
        state supported by SaveButton.
        */
        expect(
            screen.getByRole(
                "button",
                {
                    name: "⚠ Save Failed - Try Again",
                }
            )
        ).toBeEnabled();


        /*
        The data is still unsaved after
        the failed request.
        */
        expect(
            screen.getByText(
                "● Unsaved Changes"
            )
        ).toBeInTheDocument();

    });


    test("reloads when date changes", async () => {

        render(
            <LogWorkoutMetrics />
        );


        await screen.findByText(
            "Workouts"
        );


        expect(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).toHaveBeenCalledTimes(1);


        const dateInput =
            screen.getByDisplayValue(
                /^\d{4}-\d{2}-\d{2}$/
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
                workoutMetricsApi.getWorkoutMetricsByDate
            ).toHaveBeenCalledTimes(2);

        });


        expect(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).toHaveBeenLastCalledWith(
            "2026-08-20"
        );

    });


    test("shows load error when Workout Metrics fail to load", async () => {

        vi.mocked(
            workoutMetricsApi.getWorkoutMetricsByDate
        ).mockRejectedValue(
            new Error("Load failed")
        );


        render(
            <LogWorkoutMetrics />
        );


        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

    });

});