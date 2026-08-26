/*
    LogToday

    Page responsible for viewing and editing
    the Daily Log for a selected date.

    Responsibilities:
    - Load the Daily Log from the backend.
    - Maintain the page state.
    - Pass state to the page sections.
    - Save changes back to the backend.
*/

import { useEffect, useState } from "react";
import {
    Activity,
    Apple,
    Bed,
    CalendarClock,
    Dumbbell,
    GlassWater,
    NotebookPen,
    User,
} from "lucide-react";

import { getDailyLog, saveDailyLog } from "../../api/health";
import type { DailyLog } from "../../types/DailyLog";
import LoadingSpinner from "../../components/LoadingSpinner";
import BodySection from "./components/BodySection";
import HydrationSection from "./components/HydrationSection";
import LogTodayHeader from "./components/LogTodayHeader";
import MealTimingSection from "./components/MealTimingSection";
import NotesSection from "./components/NotesSection";
import NutritionSection from "./components/NutritionSection";
import SaveButton from "../../components/SaveButton";
import SleepSection from "./components/SleepSection";
import WorkoutSection from "./components/WorkoutSection";
import ActivitySection from "./components/ActivitySection";
import DateSection from "./components/DateSection";
import { createEmptyDailyLog } from "../../utils/createEmptyDailyLog";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";

function LogToday() {


    /*
    Today's date in YYYY-MM-DD format.

    Used as the default date when the page
    is first opened.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Currently selected date.

    Changing this value automatically
    reloads the Daily Log for the
    selected date.
    */
    const [selectedDate, setSelectedDate] = useState(today);


   /*
    Page state.

    isLoading
        Indicates whether data is currently
        being loaded from the backend.

    isDirty
        Indicates whether the page contains
        unsaved changes.

    saveStatus
        Tracks the current save operation.
    */
    const [isLoading, setIsLoading] = useState(true);
    const [isDirty, setIsDirty] = useState(false);
    const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "failed">("saved");

    const [dailyLog, setDailyLog] = useState<DailyLog>(
    createEmptyDailyLog()
    );

    /*
    Whenever the selected date changes:

        1. Request the Daily Log from
        the backend.
        2. Populate the page state.
        3. If no record exists, create
        an empty DailyLog object.
    */

    useEffect(() => {
        async function loadDailyLog() {
            console.log("Loading Daily Log for:", selectedDate);
            setIsLoading(true);
            try {
                const existingDailyLog = await getDailyLog(selectedDate);

                if (existingDailyLog) {
                    setDailyLog(existingDailyLog);
                    setIsDirty(false);
                } else {
                    setDailyLog(createEmptyDailyLog());
                    setIsDirty(false);
                }
            } catch (error) {
                console.error("Failed to load Daily Log:", error);
            } finally {

                setIsLoading(false);

            }
        }
        /*
            Retrieve the Daily Log for
            the selected date.
        */
        loadDailyLog();
        /*
            The [selectedDate] is called the dependency array.
            It tells React to Run this effect whenever selectedDate changes
        */
    }, [selectedDate]);

   /*
        Save the current Daily Log
        to the backend.

        The Save button invokes
        this method.
    */
    async function handleSaveDailyLog() {

        setSaveStatus("saving");

        try {

            console.log(dailyLog);
            await saveDailyLog(selectedDate, dailyLog);
            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {
            console.error(error);
            setSaveStatus("failed");

        }

    }

    /*
        Update the page state whenever the
        user changes a value.

        Also marks the page as having
        unsaved changes.
    */
    function updateDailyLog(
        action: React.SetStateAction<DailyLog>
    ) {
        setIsDirty(true);
        setSaveStatus("idle");
        setDailyLog(action);
    }

    /*
        Display a loading indicator while
        the Daily Log is being retrieved
        from the backend.
    */
    if (isLoading) {

        return (
            <LoadingSpinner />
        );

    }

    /*
        Page Layout

        PageContainer
            Provides the standard page layout.

        LogTodayHeader
            Displays the page heading and
            save status.

        DateSection
            Allows the user to choose the
            log date.

        CollapsibleCard
            Groups each section of the Daily Log.

        SaveButton
            Saves the current Daily Log.
    */
    return (
        <PageContainer>

            <div
                className="
                    space-y-8
                "
            >

                <LogTodayHeader
                    isDirty={isDirty}
                />

                <DateSection
                    selectedDate={selectedDate}
                    setSelectedDate={setSelectedDate}
                />


                <CollapsibleCard
                    title="Workout"
                    icon={Dumbbell}
                    iconColor="text-blue-600"
                >

                    <WorkoutSection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Body"
                    icon={User}
                    iconColor="text-violet-600"
                >

                    <BodySection
                        weight={dailyLog.body.weight}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Activity"
                    icon={Activity}
                    iconColor="text-orange-500"
                >

                    <ActivitySection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Meal Timing"
                    icon={CalendarClock}
                    iconColor="text-amber-500"
                >

                    <MealTimingSection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Nutrition"
                    icon={Apple}
                    iconColor="text-green-600"
                >

                    <NutritionSection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Hydration"
                    icon={GlassWater}
                    iconColor="text-cyan-600"
                >

                    <HydrationSection
                        water={dailyLog.hydration.water}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Sleep"
                    icon={Bed}
                    iconColor="text-indigo-600"
                >

                    <SleepSection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <CollapsibleCard
                    title="Notes"
                    icon={NotebookPen}
                    iconColor="text-slate-600"
                >

                    <NotesSection
                        dailyLog={dailyLog}
                        setDailyLog={updateDailyLog}
                    />

                </CollapsibleCard>

                <SaveButton
                    onClick={handleSaveDailyLog}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />
            </div>
        </PageContainer>
    );
}

export default LogToday;