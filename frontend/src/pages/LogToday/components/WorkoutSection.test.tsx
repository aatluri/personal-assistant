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

import WorkoutSection from "./WorkoutSection";

import type { DailyLog } from "../../../types/DailyLog";
import { createEmptyDailyLog } from "../../../utils/createEmptyDailyLog";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    WorkoutSection Tests

    Each test follows the same sequence:

    1. Render the WorkoutSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the WorkoutSection behaves as expected.
*/

describe("WorkoutSection", () => {

    // Verify that all Workout fields are displayed.
    test("renders workout fields", () => {

        // -------------------------------------------------------------
        // Create an empty DailyLog object.
        //
        // This supplies the WorkoutSection with the
        // data it expects from the page.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        // -------------------------------------------------------------
        // Render the WorkoutSection using the
        // empty DailyLog.
        // -------------------------------------------------------------
        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        // -------------------------------------------------------------
        // Verify that every Workout field is displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByLabelText("Workout Type")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Duration (minutes)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Calories Burnt")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Volume (kg)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Sets")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Average Heart Rate (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Workout Summary")
        ).toBeInTheDocument();

    });


    // Verify that the supplied Workout values are displayed.
    test("renders supplied values", () => {

        // -------------------------------------------------------------
        // Create a DailyLog containing workout data.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        dailyLog.workout.workoutType = "HIIT";
        dailyLog.workout.workoutDuration = 75;
        dailyLog.workout.workoutCalories = 900;
        dailyLog.workout.workoutVolume = 12000;
        dailyLog.workout.workoutSets = 90;
        dailyLog.workout.averageHeartRate = 145;
        dailyLog.workout.workoutSummary =
            "Push-ups and Deadlifts";

        // -------------------------------------------------------------
        // Render the WorkoutSection using
        // the populated DailyLog.
        // -------------------------------------------------------------
        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={vi.fn()}
            />
        );

        // -------------------------------------------------------------
        // Verify that every supplied value
        // is displayed.
        // -------------------------------------------------------------
        expect(
            screen.getByDisplayValue("HIIT")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("75")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("900")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("12000")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("90")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("145")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue(
                "Push-ups and Deadlifts"
            )
        ).toBeInTheDocument();

    });

    // Verify that changing the Workout Type updates the DailyLog.
    test("updates workout type", () => {

        // -------------------------------------------------------------
        // Create a DailyLog and a mock version of setDailyLog.
        //
        // The component should call setDailyLog whenever
        // the Workout Type changes.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        // -------------------------------------------------------------
        // Simulate the user selecting a different
        // Workout Type.
        // -------------------------------------------------------------
        fireEvent.change(
            screen.getByLabelText("Workout Type"),
            {
                target: {
                    value: "Strength",
                },
            }
        );

        // -------------------------------------------------------------
        // Verify that the component requested
        // an update to the DailyLog.
        // -------------------------------------------------------------
        expect(setDailyLog).toHaveBeenCalled();

        // -------------------------------------------------------------
        // Extract the updater function that was passed
        // to setDailyLog.
        //
        // React stores state updates as functions:
        //
        // setDailyLog(previous => ({ ... }))
        //
        // so we execute that function ourselves.
        // -------------------------------------------------------------
        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        // -------------------------------------------------------------
        // Verify that only the Workout Type
        // was updated.
        // -------------------------------------------------------------
        expect(
            updatedDailyLog.workout.workoutType
        ).toBe("Strength");

    });

    // Verify that changing the Workout Duration updates the DailyLog.
    test("updates workout duration", () => {

        // -------------------------------------------------------------
        // Create a DailyLog and a mock version of setDailyLog.
        //
        // The component should call setDailyLog whenever
        // the Workout Duration changes.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        // -------------------------------------------------------------
        // Simulate the user changing the
        // Workout Duration.
        // -------------------------------------------------------------
        fireEvent.change(
            screen.getByLabelText("Duration (minutes)"),
            {
                target: {
                    value: "75",
                },
            }
        );

        // -------------------------------------------------------------
        // Verify that the component requested
        // an update to the DailyLog.
        // -------------------------------------------------------------
        expect(setDailyLog).toHaveBeenCalled();

        // -------------------------------------------------------------
        // Extract the updater function that was passed
        // to setDailyLog.
        //
        // React stores state updates as functions:
        //
        // setDailyLog(previous => ({ ... }))
        //
        // so we execute that function ourselves.
        // -------------------------------------------------------------
        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        // -------------------------------------------------------------
        // Verify that only the Workout Duration
        // was updated.
        // -------------------------------------------------------------
        expect(
            updatedDailyLog.workout.workoutDuration
        ).toBe(75);

    });

    // Verify that changing the Workout Calories updates the DailyLog.
    test("updates workout calories", () => {

        // -------------------------------------------------------------
        // Create a DailyLog and a mock version of setDailyLog.
        //
        // The component should call setDailyLog whenever
        // the Workout Calories changes.
        // -------------------------------------------------------------
        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        // -------------------------------------------------------------
        // Simulate the user changing the
        // Workout Calories.
        // -------------------------------------------------------------
        fireEvent.change(
            screen.getByLabelText("Calories Burnt"),
            {
                target: {
                    value: "900",
                },
            }
        );

        // -------------------------------------------------------------
        // Verify that the component requested
        // an update to the DailyLog.
        // -------------------------------------------------------------
        expect(setDailyLog).toHaveBeenCalled();

        // -------------------------------------------------------------
        // Extract the updater function that was passed
        // to setDailyLog.
        //
        // React stores state updates as functions:
        //
        // setDailyLog(previous => ({ ... }))
        //
        // so we execute that function ourselves.
        // -------------------------------------------------------------
        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        // -------------------------------------------------------------
        // Verify that only the Workout Calories
        // was updated.
        // -------------------------------------------------------------
        expect(
            updatedDailyLog.workout.workoutCalories
        ).toBe(900);

    });

    // Verify that changing the Workout Volume updates the DailyLog.
    test("updates workout volume", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Volume (kg)"),
            {
                target: {
                    value: "12000",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.workout.workoutVolume
        ).toBe(12000);

    });


    // Verify that changing the Workout Sets updates the DailyLog.
    test("updates workout sets", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Sets"),
            {
                target: {
                    value: "90",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.workout.workoutSets
        ).toBe(90);

    });


    // Verify that changing the Average Heart Rate updates the DailyLog.
    test("updates average heart rate", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Average Heart Rate (bpm)"),
            {
                target: {
                    value: "145",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.workout.averageHeartRate
        ).toBe(145);

    });


    // Verify that changing the Workout Summary updates the DailyLog.
    test("updates workout summary", () => {

        const dailyLog =
            createEmptyDailyLog();

        const setDailyLog = vi.fn();

        render(
            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Workout Summary"),
            {
                target: {
                    value: "Push-ups and Deadlifts",
                },
            }
        );

        expect(setDailyLog).toHaveBeenCalled();

        const updateFunction =
            setDailyLog.mock.calls[0][0] as (
                dailyLog: DailyLog
            ) => DailyLog;

        const previousDailyLog =
            createEmptyDailyLog();

        const updatedDailyLog =
            updateFunction(previousDailyLog);

        expect(
            updatedDailyLog.workout.workoutSummary
        ).toBe("Push-ups and Deadlifts");

    });

});