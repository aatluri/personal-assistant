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

function LogToday() {
    return (
        <div>

            <LogTodayHeader />
            <AchievementBanner />
            <Scoreboard />
            <WorkoutSection />
            <BodySection />
            <MealTimingSection />
            <NutritionSection />
            <HydrationSection />
            <SleepSection />
            <NotesSection />
            <SaveButton />

        </div>
    );
}

export default LogToday;