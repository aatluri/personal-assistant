import { useEffect, useState } from "react";

import { getDailyLog, saveDailyLog } from "../../api/health";
import type { DailyLog } from "../../types/DailyLog";
import type { SetStateAction } from "react";
import LoadingSpinner from "../../components/LoadingSpinner";

import AchievementBanner from "./components/AchievementBanner";
import BodySection from "./components/BodySection";
import HydrationSection from "./components/HydrationSection";
import LogTodayHeader from "./components/LogTodayHeader";
import MealTimingSection from "./components/MealTimingSection";
import NotesSection from "./components/NotesSection";
import NutritionSection from "./components/NutritionSection";
import SaveButton from "./components/SaveButton";
import Scoreboard from "./components/Scoreboard";
import SleepSection from "./components/SleepSection";
import WorkoutSection from "./components/WorkoutSection";
import ActivitySection from "./components/ActivitySection";
import DateSection from "./components/DateSection";
import { createEmptyDailyLog } from "../../utils/createEmptyDailyLog";

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
        try {
            console.log(dailyLog);
            await saveDailyLog(selectedDate, dailyLog);
            setIsDirty(false);
            alert("Daily Log saved successfully.");
        } catch (error) {
            console.error(error);
            alert("Failed to save Daily Log.");
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
        setDailyLog(action);
    }

    if (isLoading) {

        return (
            <LoadingSpinner />
        );

    }

    return (
        <div>

            <LogTodayHeader
                selectedDate={selectedDate}
                isDirty={isDirty}
            />

            <DateSection
                selectedDate={selectedDate}
                setSelectedDate={setSelectedDate}
            />

            <AchievementBanner
                dailyLog={dailyLog}
            />

            <Scoreboard
                dailyLog={dailyLog}
            />

            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <BodySection
                weight={dailyLog.body.weight}
                setDailyLog={updateDailyLog}
            />

            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <HydrationSection
                water={dailyLog.hydration.water}
                setDailyLog={updateDailyLog}
            />

            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <NotesSection
                dailyLog={dailyLog}
                setDailyLog={updateDailyLog}
            />

            <SaveButton
                onClick={handleSaveDailyLog}
            />

        </div>
    );
}

export default LogToday;