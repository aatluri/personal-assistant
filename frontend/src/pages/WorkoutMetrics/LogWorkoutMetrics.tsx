import { useEffect, useState } from "react";

import {
    getWorkoutMetricsByDate,
    saveWorkoutMetric,
} from "../../api/health";

import type { WorkoutMetrics } from "../../types/WorkoutMetrics";

import LoadingSpinner from "../../components/LoadingSpinner";
import PageContainer from "../../components/PageContainer";

import LogTodayHeader from "../LogToday/components/LogTodayHeader";
import DateSection from "../LogToday/components/DateSection";

import WorkoutMetricsSection from "./components/WorkoutMetricsSection";

import SaveButton from "../../components/SaveButton";

import { createEmptyWorkoutMetrics } from "../../utils/createEmptyWorkoutMetrics";

import { Dumbbell, Plus } from "lucide-react";


export default function LogWorkoutMetrics() {

    /*
    Get today's date in YYYY-MM-DD format.
    */
    const today = new Date().toLocaleDateString("en-CA");


    /*
    Date currently selected by the user.
    */
    const [selectedDate, setSelectedDate] =
        useState(today);


    /*
    All workouts belonging to the selected date.
    */
    const [workouts, setWorkouts] =
        useState<WorkoutMetrics[]>([]);

    /*
    Workout currently selected for
    viewing or editing.
    */
    const [selectedWorkout, setSelectedWorkout] =
        useState<WorkoutMetrics | null>(null);

    /*
    Tracks whether Workout Metrics are
    currently being loaded.
    */
    const [isLoading, setIsLoading] =
        useState(true);


    /*
    Tracks whether the selected workout
    has unsaved changes.
    */
    const [isDirty, setIsDirty] = useState(false);

    /*
    Tracks the current save status.

    Used by SaveButton to show whether
    the workout is saved or saving.
    */
    const [saveStatus, setSaveStatus] =
        useState<"saved" | "saving">("saved");

    /*
    Load Workout Metrics whenever the
    selected date changes.
    */
    useEffect(() => {

        async function loadWorkoutMetrics() {

            setIsLoading(true);

            try {

                const data =
                    await getWorkoutMetricsByDate(
                        selectedDate
                    );

                setWorkouts(data);
                /*
                If workouts exist for the selected date,
                select the first one automatically.

                If there are no workouts, nothing is selected.
                */
                if (data.length > 0) {
                    setSelectedWorkout(data[0]);
                } else {
                    setSelectedWorkout(null);
                }
                setIsDirty(false);

            } finally {

                setIsLoading(false);

            }
        }

        loadWorkoutMetrics();

    }, [selectedDate]);


    /*
    Show the loading spinner while
    Workout Metrics are loading.
    */
    if (isLoading) {
        return <LoadingSpinner />;
    }

    /*
    Creates a new empty workout for
    the currently selected date.
    */
    function handleAddWorkout() {

        const newWorkout = createEmptyWorkoutMetrics();

        newWorkout.date = selectedDate;

        setSelectedWorkout(newWorkout);

        setIsDirty(true);
    }

    async function handleSaveWorkout() {

        if (selectedWorkout === null) {
            return;
        }

        /*
        Workout Start Time is required because
        it is the unique key for a workout.
        */
        if (!selectedWorkout.workoutStartTime) {
            alert("Please enter a Workout Start Time.");
            return;
        }

        /*
        Workout End Time is required by the
        backend WorkoutMetrics model.
        */
        if (!selectedWorkout.workoutEndTime) {
            alert("Please enter a Workout End Time.");
            return;
        }

        /*
        Workout Duration is required by the
        backend WorkoutMetrics model.
        */
        if (!selectedWorkout.workoutDuration) {
            alert("Please enter a Workout Duration.");
            return;
        }

        setSaveStatus("saving");

        try {

            await saveWorkoutMetric(
                selectedWorkout
            );

            /*
            Reload the workouts for this date.

            This is important after creating a new
            workout because it adds the newly saved
            workout to the workouts array.
            */
            const data =
                await getWorkoutMetricsByDate(
                    selectedDate
                );

            setWorkouts(data);

            /*
            Find the workout that was just saved
            and keep it selected.
            */
            const savedWorkout =
                data.find(
                    (workout) =>
                        workout.workoutStartTime ===
                        selectedWorkout.workoutStartTime
                );

            if (savedWorkout) {
                setSelectedWorkout(savedWorkout);
            }

            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {

            setSaveStatus("saved");

            console.error(
                "Failed to save Workout Metrics:",
                error
            );

            alert("Failed to save Workout Metrics.");
        }
    }

    return (
        <PageContainer>

            <LogTodayHeader
                isDirty={isDirty}
            />

            <DateSection
                selectedDate={selectedDate}
                setSelectedDate={setSelectedDate}
            />

            <div>
                <div className="mt-8 mb-8">

                    {/* Section heading and Add Workout action */}
                    <div className="mb-4 flex items-center justify-between px-1">

                        <h2 className="text-lg font-semibold text-slate-900">
                            Workouts
                        </h2>

                        <button
                            type="button"
                            onClick={handleAddWorkout}
                            className="
                                flex h-10 items-center gap-2
                                rounded-xl border border-slate-200
                                bg-white px-4
                                text-sm font-medium text-slate-700
                                transition-colors
                                hover:bg-slate-50
                            "
                        >
                            <Plus size={16} />

                            Add Workout
                        </button>

                    </div>


                    {/* Existing workouts */}
                    {workouts.length > 0 ? (

                        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

                            {workouts.map((workout) => {

                                const isSelected =
                                    selectedWorkout?.workoutStartTime ===
                                    workout.workoutStartTime;

                                return (
                                    <button
                                        key={workout.workoutStartTime}
                                        type="button"
                                        onClick={() => {
                                            setSelectedWorkout(workout);
                                            setIsDirty(false);
                                        }}
                                        className={`
                                            rounded-2xl border p-4
                                            text-left
                                            transition-all
                                            ${
                                                isSelected
                                                    ? "border-blue-500 bg-blue-50"
                                                    : "border-slate-200 bg-white hover:border-slate-300"
                                            }
                                        `}
                                    >
                                        <div className="flex items-start gap-3">

                                            <div
                                                className="
                                                    flex h-10 w-10 shrink-0
                                                    items-center justify-center
                                                    rounded-xl bg-slate-100
                                                "
                                            >
                                                <Dumbbell
                                                    size={20}
                                                    className="text-slate-600"
                                                />
                                            </div>

                                            <div className="min-w-0">

                                                <div
                                                    className="
                                                        truncate
                                                        text-sm font-semibold
                                                        text-slate-900
                                                    "
                                                >
                                                    {workout.workoutType ||
                                                        "Workout"}
                                                </div>

                                                <div
                                                    className="
                                                        mt-1 text-sm
                                                        text-slate-500
                                                    "
                                                >
                                                    {workout.workoutStartTime}
                                                </div>

                                                <div
                                                    className="
                                                        mt-1 text-xs
                                                        text-slate-400
                                                    "
                                                >
                                                    {workout.workoutDuration}
                                                </div>

                                            </div>

                                        </div>

                                    </button>
                                );
                            })}

                        </div>

                    ) : (

                        <div
                            className="
                                rounded-2xl border border-dashed
                                border-slate-300 bg-white
                                px-6 py-8 text-center
                            "
                        >
                            <Dumbbell
                                size={24}
                                className="mx-auto mb-2 text-slate-400"
                            />

                            <p className="text-sm text-slate-500">
                                No workouts recorded for this date.
                            </p>

                        </div>

                    )}

                </div>

                {selectedWorkout && (
                    <WorkoutMetricsSection
                        workoutMetrics={selectedWorkout}

                        setWorkoutMetrics={(action) => {

                            setIsDirty(true);

                            setSelectedWorkout((previous) => {

                                if (previous === null) {
                                    return null;
                                }

                                if (typeof action === "function") {
                                    return action(previous);
                                }

                                return action;
                            });
                        }}
                    />
                )}
                {selectedWorkout && (
                <SaveButton
                    onClick={handleSaveWorkout}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />
                )}
            </div>
        </PageContainer>
    );
}