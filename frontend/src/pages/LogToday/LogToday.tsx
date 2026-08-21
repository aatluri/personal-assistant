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
import SaveButton from "./components/SaveButton";
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
    This matches the format required
    by the HTML date input.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Stores the currently selected date.

    Changing this value causes the
    corresponding Daily Log to be loaded.
    */
    const [selectedDate, setSelectedDate] = useState(today);


    /*
    Indicates whether the Daily Log
    is currently being loaded.
    */
    const [isLoading, setIsLoading] = useState(true);
    const [isDirty, setIsDirty] = useState(false);
    const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "failed">("saved");

    const [dailyLog, setDailyLog] = useState<DailyLog>(
    createEmptyDailyLog()
    );

    console.log("LogToday rendered");

    /*
        Runs whenever the selected date changes.

        When the page first loads, dailyLog.date
        contains today's date, so this also loads
        today's Daily Log automatically.
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

        loadDailyLog();
    }, [selectedDate]);

    /*
    Saves the current Daily Log
    to the backend.
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
    Updates the Daily Log and marks
    the page as having unsaved changes.
    */
    function updateDailyLog(
        action: React.SetStateAction<DailyLog>
    ) {
        setIsDirty(true);
        setSaveStatus("idle");
        setDailyLog(action);
    }

    if (isLoading) {

        return (
            <LoadingSpinner />
        );

    }

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