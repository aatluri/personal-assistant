import { useState } from "react";

import { saveDailyLog } from "../../api/health";
import type { DailyLog } from "../../types/DailyLog";

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
import LogDateSection from "./components/DateSection";

function LogToday() {


    /*
    Today's date in YYYY-MM-DD format.
    This matches the format required
    by the HTML date input.
    */
    const today = new Date().toLocaleDateString("en-CA");
    /*
        Daily Log State

        This object contains all the data
        entered on the Log Today page.

        Eventually these values will come
        from the backend instead of being
        hardcoded.
    */
    const [dailyLog, setDailyLog] = useState<DailyLog>({

        /* ------------------------------ */
        /* General                        */
        /* ------------------------------ */

        date: today,

        /* ------------------------------ */
        /* Workout                        */
        /* ------------------------------ */

        workout: {
            workoutType: "HIIT",
            workoutDuration: 58,
            workoutCalories: 620,
            workoutVolume: 5975,
            workoutSets: 50,
            averageHeartRate: 140,
            workoutSummary: `Battle Rope - 5 min
                            Row - 1.25 km
                            Push-ups - 70
                            Kettlebell Swings - 50`,
        },

        /* ------------------------------ */
        /* Body                           */
        /* ------------------------------ */

        body: {
            weight: 80.3,
        },

        /* ------------------------------ */
        /* Activity                       */
        /* ------------------------------ */

        activity: {
            steps: 8500,
            totalCaloriesBurnt: 2450,
        },

        /* ------------------------------ */
        /* Meal Timing                    */
        /* ------------------------------ */

        mealTiming: {
            firstMealTime: "08:30",
            lastMealTime: "20:45",
        },

        /* ------------------------------ */
        /* Nutrition                      */
        /* ------------------------------ */

        nutrition: {
            breakfast: "",
            lunch: "",
            dinner: "",
            snacks: "",
            protein: 110,
            carbs: 130,
            fat: 65,
            fibre: 30,
            sugar: 12,
            caloriesConsumed: 2100,
        },

        /* ------------------------------ */
        /* Hydration                      */
        /* ------------------------------ */

        hydration: {
            water: 3000,
        },

        /* ------------------------------ */
        /* Sleep                          */
        /* ------------------------------ */

        sleep: {
            sleepStartTime: "23:15",
            sleepEndTime: "07:57",
        },

        /* ------------------------------ */
        /* Notes                          */
        /* ------------------------------ */

        notes: {
            notes: "sss",
        },

    });

    /*
        Saves the current Daily Log
        to the backend.
    */
    async function handleSaveDailyLog() {
        try {
            console.log(dailyLog);
            await saveDailyLog(dailyLog);
            alert("Daily Log saved successfully.");
        } catch (error) {
            console.error(error);
            alert("Failed to save Daily Log.");
        }
    }

    return (
        <div>

            <LogTodayHeader />

            <LogDateSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <AchievementBanner />

            <Scoreboard />

            <WorkoutSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <BodySection
                weight={dailyLog.body.weight}
                setDailyLog={setDailyLog}
            />

            <ActivitySection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <MealTimingSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <NutritionSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <HydrationSection
                water={dailyLog.hydration.water}
                setDailyLog={setDailyLog}
            />

            <SleepSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <NotesSection
                dailyLog={dailyLog}
                setDailyLog={setDailyLog}
            />

            <SaveButton
                onClick={handleSaveDailyLog}
            />

        </div>
    );
}

export default LogToday;