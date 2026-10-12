/*
WorkoutMetricsSection
---------------------

This component is the editable form for ONE workout.

It does not load data, save data, or own the workout state.
Those responsibilities belong to LogWorkoutMetrics.

The parent passes two props:

    workoutMetrics
        The currently selected WorkoutMetrics object.

    setWorkoutMetrics
        A state-update function supplied by the parent.


CONTROLLED INPUTS

Every TextInput is a controlled input.

For example:

    value={workoutMetrics.workoutType}

means the displayed value always comes from the
workoutMetrics object supplied by the parent.

When the user types something, the component does not
directly modify workoutMetrics.

Instead it calls setWorkoutMetrics with an updater function:

    setWorkoutMetrics((previous) => ({
        ...previous,
        workoutType: newValue,
    }));

The spread:

    ...previous

copies all existing WorkoutMetrics fields.

We then replace only the field that changed.

For example, changing workoutType keeps start time,
duration, calories, heart rate, etc. unchanged.


PARENT / CHILD STATE FLOW

The state flow is:

    LogWorkoutMetrics
            |
            | selectedWorkout
            v
    WorkoutMetricsSection
            |
            | user edits a field
            v
    setWorkoutMetrics(...)
            |
            v
    LogWorkoutMetrics updates selectedWorkout
            |
            v
    React re-renders WorkoutMetricsSection
            |
            v
    input displays the new value

This is called "lifting state up".

WorkoutMetricsSection displays and edits the data, but the
actual state remains owned by LogWorkoutMetrics.


TEXT FIELD UPDATES

Text-based fields use updateText.

These include fields such as:

    workoutType
    workoutStartTime
    workoutEndTime
    workoutDuration

updateText receives:

    field
    value

and creates a new WorkoutMetrics object with only that
field changed.


NUMERIC FIELD UPDATES

Numeric fields use updateNumber.

These include:

    totalEnergyKcal
    activeEnergyKcal
    maxHeartRateBpm
    avgHeartRateBpm
    distanceMi
    avgSpeedMph

The WorkoutMetrics type allows these values to be:

    number | ""

The empty string is useful because an HTML input needs to
be able to represent an empty field.

Therefore updateNumber converts:

    ""

to:

    ""

and converts a value such as:

    "650"

to:

    650

This means the UI can display an empty field while populated
numeric values remain numbers in our application state.


WHY THIS COMPONENT DOES NOT MANAGE isDirty

WorkoutMetricsSection does not need to know whether the page
has unsaved changes.

It simply reports changes through setWorkoutMetrics.

LogWorkoutMetrics wraps that update function and also does:

    setIsDirty(true);
    setSaveStatus("idle");

Therefore every field change automatically marks the page
as having unsaved changes without WorkoutMetricsSection
needing to understand save behaviour.


WHY id AND name ARE PROVIDED

Each TextInput has an id and name.

The id allows the input's label to be correctly associated
with the underlying HTML input.

This improves accessibility and also allows tests to locate
fields using:

    screen.getByLabelText(...)

The name identifies the field represented by the input.


COMPONENT RESPONSIBILITY

WorkoutMetricsSection should remain focused on:

    WorkoutMetrics data
            ↓
    displaying form fields
            ↓
    converting user input
            ↓
    requesting state updates

It should NOT contain:

    - API calls
    - backend logic
    - date loading
    - save logic
    - dirty-state logic
    - workout-list management

Those responsibilities remain in LogWorkoutMetrics.
*/

import {
    cleanup,
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import WorkoutMetricsSection from "./WorkoutMetricsSection";

import type {
    WorkoutMetrics,
} from "../../../types/WorkoutMetrics";

import {
    createEmptyWorkoutMetrics,
} from "../../../utils/createEmptyWorkoutMetrics";


afterEach(() => {
    cleanup();
});


describe("WorkoutMetricsSection", () => {

    /*
    Verify that all Workout Metrics fields
    are displayed.
    */
    test("renders Workout Metrics fields", () => {

        const workoutMetrics =
            createEmptyWorkoutMetrics();


        render(
            <WorkoutMetricsSection
                workoutMetrics={workoutMetrics}
                setWorkoutMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText("Workout Type")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Workout Start Time")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Workout End Time")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Workout Duration")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Total Energy (kcal)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Active Energy (kcal)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Max Heart Rate (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Average Heart Rate (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Distance (mi)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Average Speed (mi/hr)")
        ).toBeInTheDocument();

    });


    /*
    Verify that supplied Workout Metrics
    values are displayed correctly.
    */
    test("renders supplied values", () => {

        const workoutMetrics =
            createEmptyWorkoutMetrics();


        workoutMetrics.workoutType = "Running";
        workoutMetrics.workoutStartTime = "07:00";
        workoutMetrics.workoutEndTime = "08:00";
        workoutMetrics.workoutDuration = "1:00:00";

        workoutMetrics.totalEnergyKcal = 650;
        workoutMetrics.activeEnergyKcal = 550;

        workoutMetrics.maxHeartRateBpm = 175;
        workoutMetrics.avgHeartRateBpm = 145;

        workoutMetrics.distanceMi = 5.2;
        workoutMetrics.avgSpeedMph = 6.5;


        render(
            <WorkoutMetricsSection
                workoutMetrics={workoutMetrics}
                setWorkoutMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText("Workout Type")
        ).toHaveValue("Running");

        expect(
            screen.getByLabelText("Workout Start Time")
        ).toHaveValue("07:00");

        expect(
            screen.getByLabelText("Workout End Time")
        ).toHaveValue("08:00");

        expect(
            screen.getByLabelText("Workout Duration")
        ).toHaveValue("1:00:00");

        expect(
            screen.getByLabelText("Total Energy (kcal)")
        ).toHaveValue("650");

        expect(
            screen.getByLabelText("Active Energy (kcal)")
        ).toHaveValue("550");

        expect(
            screen.getByLabelText("Max Heart Rate (bpm)")
        ).toHaveValue("175");

        expect(
            screen.getByLabelText("Average Heart Rate (bpm)")
        ).toHaveValue("145");

        expect(
            screen.getByLabelText("Distance (mi)")
        ).toHaveValue("5.2");

        expect(
            screen.getByLabelText("Average Speed (mi/hr)")
        ).toHaveValue("6.5");

    });


    /*
    Helper for testing text fields.

    Each call creates a separate test.
    */
    function testTextField(
        testName: string,
        label: string,
        field: keyof WorkoutMetrics,
        inputValue: string,
    ) {

        test(testName, () => {

            const workoutMetrics =
                createEmptyWorkoutMetrics();

            const setWorkoutMetrics =
                vi.fn();


            render(
                <WorkoutMetricsSection
                    workoutMetrics={workoutMetrics}
                    setWorkoutMetrics={setWorkoutMetrics}
                />
            );


            fireEvent.change(
                screen.getByLabelText(label),
                {
                    target: {
                        value: inputValue,
                    },
                }
            );


            expect(
                setWorkoutMetrics
            ).toHaveBeenCalled();


            const updateFunction =
                setWorkoutMetrics.mock.calls[0][0] as (
                    workoutMetrics: WorkoutMetrics
                ) => WorkoutMetrics;


            const previousWorkoutMetrics =
                createEmptyWorkoutMetrics();


            const updatedWorkoutMetrics =
                updateFunction(
                    previousWorkoutMetrics
                );


            expect(
                updatedWorkoutMetrics[field]
            ).toBe(inputValue);

        });

    }


    testTextField(
        "updates workout type",
        "Workout Type",
        "workoutType",
        "Running"
    );


    testTextField(
        "updates workout start time",
        "Workout Start Time",
        "workoutStartTime",
        "07:00"
    );


    testTextField(
        "updates workout end time",
        "Workout End Time",
        "workoutEndTime",
        "08:00"
    );


    testTextField(
        "updates workout duration",
        "Workout Duration",
        "workoutDuration",
        "1:00:00"
    );


    /*
    Helper for testing numeric fields.

    Each call creates a separate test.
    */
    function testNumericField(
        testName: string,
        label: string,
        field: keyof WorkoutMetrics,
        inputValue: string,
        expectedValue: number,
    ) {

        test(testName, () => {

            const workoutMetrics =
                createEmptyWorkoutMetrics();

            const setWorkoutMetrics =
                vi.fn();


            render(
                <WorkoutMetricsSection
                    workoutMetrics={workoutMetrics}
                    setWorkoutMetrics={setWorkoutMetrics}
                />
            );


            fireEvent.change(
                screen.getByLabelText(label),
                {
                    target: {
                        value: inputValue,
                    },
                }
            );


            expect(
                setWorkoutMetrics
            ).toHaveBeenCalled();


            const updateFunction =
                setWorkoutMetrics.mock.calls[0][0] as (
                    workoutMetrics: WorkoutMetrics
                ) => WorkoutMetrics;


            const previousWorkoutMetrics =
                createEmptyWorkoutMetrics();


            const updatedWorkoutMetrics =
                updateFunction(
                    previousWorkoutMetrics
                );


            expect(
                updatedWorkoutMetrics[field]
            ).toBe(expectedValue);

        });

    }


    testNumericField(
        "updates total energy",
        "Total Energy (kcal)",
        "totalEnergyKcal",
        "650",
        650
    );


    testNumericField(
        "updates active energy",
        "Active Energy (kcal)",
        "activeEnergyKcal",
        "550",
        550
    );


    testNumericField(
        "updates max heart rate",
        "Max Heart Rate (bpm)",
        "maxHeartRateBpm",
        "175",
        175
    );


    testNumericField(
        "updates average heart rate",
        "Average Heart Rate (bpm)",
        "avgHeartRateBpm",
        "145",
        145
    );


    testNumericField(
        "updates distance",
        "Distance (mi)",
        "distanceMi",
        "5.2",
        5.2
    );


    testNumericField(
        "updates average speed",
        "Average Speed (mi/hr)",
        "avgSpeedMph",
        "6.5",
        6.5
    );


    /*
    Verify that clearing a numeric field
    stores an empty string instead of 0.
    */
    test("keeps cleared numeric field empty", () => {

        const workoutMetrics =
            createEmptyWorkoutMetrics();

        workoutMetrics.totalEnergyKcal = 650;

        const setWorkoutMetrics =
            vi.fn();


        render(
            <WorkoutMetricsSection
                workoutMetrics={workoutMetrics}
                setWorkoutMetrics={setWorkoutMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText(
                "Total Energy (kcal)"
            ),
            {
                target: {
                    value: "",
                },
            }
        );


        const updateFunction =
            setWorkoutMetrics.mock.calls[0][0] as (
                workoutMetrics: WorkoutMetrics
            ) => WorkoutMetrics;


        const updatedWorkoutMetrics =
            updateFunction(
                workoutMetrics
            );


        expect(
            updatedWorkoutMetrics.totalEnergyKcal
        ).toBe("");

    });

});