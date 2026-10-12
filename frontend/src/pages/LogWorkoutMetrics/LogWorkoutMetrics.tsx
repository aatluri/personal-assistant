/*
LogWorkoutMetrics
-----------------

This is the main page component for viewing, creating,
editing, and saving workouts for a selected date.

STATE MANAGEMENT

This component owns all Workout Metrics state.

1. selectedDate
   The date currently being viewed.

   When selectedDate changes, the useEffect runs again
   and loads all workouts belonging to that date from
   the backend.

2. workouts
   An array containing all workouts returned by the
   backend for selectedDate.

   Unlike most of our other health metrics, Workout
   Metrics can contain multiple records for the same date.

   Example:
       Morning Run
       Evening Strength Training

3. selectedWorkout
   The workout currently being displayed in
   WorkoutMetricsSection.

   This is separate from the workouts array because the
   user may be editing the selected workout before those
   changes have been saved to the backend.

   When workouts are loaded, the first workout is selected
   automatically.

   Clicking a workout card changes selectedWorkout.

   Clicking Add Workout creates a new empty WorkoutMetrics
   object and makes that the selectedWorkout.

4. isLoading
   Indicates whether workouts are currently being loaded
   from the backend.

   While true, the page displays LoadingSpinner.

5. isDirty
   Indicates whether selectedWorkout contains changes that
   have not yet been saved.

   Editing any field or creating a new workout sets this
   to true.

   Loading an existing workout or successfully saving a
   workout sets it back to false.

6. saveStatus
   Tracks the state of the save operation.

       "idle"   = unsaved changes exist
       "saving" = save request is running
       "saved"  = data is saved
       "failed" = previous save attempt failed

   SaveButton uses isDirty and saveStatus together to
   determine its label and whether it should be enabled.

7. loadError
   Indicates that loading workouts from the backend failed.
   When true, an error message is displayed.


LOADING WORKOUTS

The useEffect depends on selectedDate.

Whenever selectedDate changes:

    getWorkoutMetricsByDate(selectedDate)

is called.

The returned array is stored in workouts.

If at least one workout exists:
    selectedWorkout = first workout

If no workouts exist:
    selectedWorkout = null

Because the data has just come from the backend:
    isDirty = false
    saveStatus = "saved"


ADDING A WORKOUT

handleAddWorkout() creates a new object using:

    createEmptyWorkoutMetrics()

Its date is set to selectedDate and it becomes the
selectedWorkout.

It is NOT immediately added to the workouts array because
it has not been saved yet.

Instead:

    isDirty = true
    saveStatus = "idle"

The new workout appears in WorkoutMetricsSection where the
user can enter its details.


EDITING A WORKOUT

WorkoutMetricsSection receives:

    workoutMetrics={selectedWorkout}

and a setWorkoutMetrics callback.

WorkoutMetricsSection does not own the workout state.

Whenever one of its fields changes, it calls the callback
provided by this page.

The callback:

    1. Sets isDirty to true.
    2. Sets saveStatus to "idle".
    3. Updates selectedWorkout.

This keeps the actual state management in the page while
allowing WorkoutMetricsSection to behave like an editable
form.


SAVING A WORKOUT

handleSaveWorkout() first validates the required fields:

    workoutStartTime
    workoutEndTime
    workoutDuration

Workout Start Time is particularly important because it is
used as the unique key for a workout.

If validation succeeds:

    saveStatus = "saving"

The selected workout is sent to the backend using:

    saveWorkoutMetric(selectedWorkout)

After a successful save, we deliberately reload all workouts
for selectedDate from the backend instead of manually adding
or modifying the workouts array.

This ensures the frontend state reflects exactly what is
stored by the backend.

After reloading, the saved workout is found by matching its
workoutStartTime and is made selectedWorkout again.

Finally:

    isDirty = false
    saveStatus = "saved"

If saving fails:

    saveStatus = "failed"

isDirty remains true because the user's changes have not
actually been saved.


WORKOUT LIST VS SELECTED WORKOUT

The two pieces of state have different purposes:

    workouts
        = saved workouts loaded from the backend

    selectedWorkout
        = the workout currently being viewed/edited

This distinction is important when creating or editing a
workout.

Changes are made to selectedWorkout first. The workouts
array is refreshed from the backend only after a successful
save.


COMPONENT RESPONSIBILITIES

LogWorkoutMetrics handles:

    - loading data
    - backend API calls
    - selected date
    - list of workouts
    - selected workout
    - creating workouts
    - save validation
    - saving
    - dirty state
    - save status
    - load errors

WorkoutMetricsSection handles:

    - displaying the workout form
    - converting input changes into WorkoutMetrics updates

SaveButton handles:

    - displaying the appropriate save status
    - enabling/disabling the save action
*/

import { useEffect, useState } from "react";

import {
    getWorkoutMetricsByDate,
    saveWorkoutMetric,
} from "../../api/workoutMetrics";

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
    const [isDirty, setIsDirty] =
        useState(false);


    /*
    Tracks the current save status.

    idle:
        There are unsaved changes.

    saving:
        A save request is in progress.

    saved:
        All changes have been saved.

    failed:
        The previous save failed.
    */
    const [saveStatus, setSaveStatus] =
        useState<
            "idle" |
            "saving" |
            "saved" |
            "failed"
        >("saved");


    /*
    Tracks whether loading Workout Metrics
    failed.
    */
    const [loadError, setLoadError] =
        useState(false);


    /*
    Load Workout Metrics whenever the
    selected date changes.
    */
    useEffect(() => {

        async function loadWorkoutMetrics() {

            setIsLoading(true);
            setLoadError(false);

            try {

                const data =
                    await getWorkoutMetricsByDate(
                        selectedDate
                    );

                setWorkouts(data);


                /*
                If workouts exist for the selected date,
                select the first one automatically.

                If there are no workouts,
                nothing is selected.
                */
                if (data.length > 0) {

                    setSelectedWorkout(
                        data[0]
                    );

                } else {

                    setSelectedWorkout(
                        null
                    );
                }


                /*
                The data has just been loaded from
                the backend, so there are no
                unsaved changes.
                */
                setIsDirty(false);
                setSaveStatus("saved");

            } catch (error) {

                console.error(
                    "Failed to load Workout Metrics:",
                    error
                );

                setLoadError(true);

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

        const newWorkout =
            createEmptyWorkoutMetrics();

        newWorkout.date =
            selectedDate;

        setSelectedWorkout(
            newWorkout
        );


        /*
        The new workout has not been saved yet.
        */
        setIsDirty(true);
        setSaveStatus("idle");
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

            alert(
                "Please enter a Workout Start Time."
            );

            return;
        }


        /*
        Workout End Time is required by the
        backend WorkoutMetrics model.
        */
        if (!selectedWorkout.workoutEndTime) {

            alert(
                "Please enter a Workout End Time."
            );

            return;
        }


        /*
        Workout Duration is required by the
        backend WorkoutMetrics model.
        */
        if (!selectedWorkout.workoutDuration) {

            alert(
                "Please enter a Workout Duration."
            );

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

                setSelectedWorkout(
                    savedWorkout
                );
            }


            /*
            The save completed successfully.
            */
            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {

            /*
            Keep the workout dirty because the
            changes have not been saved.

            Mark the save as failed so the
            SaveButton allows the user to retry.
            */
            setSaveStatus("failed");


            console.error(
                "Failed to save Workout Metrics:",
                error
            );


            alert(
                "Failed to save Workout Metrics."
            );
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


            {loadError && (
                <div
                    className="
                        rounded-xl
                        border
                        border-red-200
                        bg-red-50
                        px-4
                        py-3
                        text-sm
                        text-red-700
                    "
                >
                    Unable to load data. Please check your connection and try again.
                </div>
            )}


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

                                            setSelectedWorkout(
                                                workout
                                            );

                                            /*
                                            This workout came from the backend,
                                            so it has no unsaved changes.
                                            */
                                            setIsDirty(false);
                                            setSaveStatus("saved");
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

                            /*
                            Any edit creates an unsaved change.

                            Reset saveStatus to idle so the
                            SaveButton displays "Save Changes".
                            */
                            setIsDirty(true);
                            setSaveStatus("idle");


                            setSelectedWorkout((previous) => {

                                if (previous === null) {
                                    return null;
                                }


                                if (typeof action === "function") {

                                    return action(
                                        previous
                                    );
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