import LogTodayHeader from "./components/LogTodayHeader";
import AchievementBanner from "./components/AchievementBanner";
import Scoreboard from "./components/Scoreboard";
import WorkoutSection from "./components/WorkoutSection";
import BodySection from "./components/BodySection";
import MealTimingSection from "./components/MealTimingSection";
import NutritionSection from "./components/NutritionSection";
import HydrationSection from "./components/HydrationSection";
import SleepSection from "./components/SleepSection";
import NotesSection from "./components/NotesSection";
import SaveButton from "./components/SaveButton";
import type { DailyLog } from "../../types/DailyLog";

import { useState } from "react";

function LogToday() {

    /*
    Daily Log State

    This object contains all the data
    entered on the Log Today page.

    We'll gradually add more fields as
    we build the application.
    */
   const [dailyLog, setDailyLog] = useState<DailyLog>({

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

    body: {
        weight: 80.3,
    },
    mealTiming: {
        firstMealTime: "08:30",
        lastMealTime: "20:45",
    },

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
        caloriesConsumed: 21000,

    },

    hydration: {
        water: 30000
    },

    sleep: {
        sleepStartTime: "23:15",
        sleepEndTime: "07:57",
    },

    notes: {
        notes: "sss",
    },
});


    console.log("Weight in LogToday:", dailyLog.body.weight);
    console.log("Water in LogToday:", dailyLog.hydration.water);
    return (
        <div>

            <LogTodayHeader />
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
            <SaveButton />

        </div>
    );
}

export default LogToday;