/*
    AchievementBanner

    Displays a summary of today's achievements.

    Some values are currently derived from
    the Daily Log, while others will be
    added as future features.
*/

import type { DailyLog } from "../../../types/DailyLog";

interface AchievementBannerProps {
    dailyLog: DailyLog;
}

function AchievementBanner({ dailyLog }: AchievementBannerProps) {

    /*
        Check whether today's protein
        goal has been achieved.
    */
    const proteinGoalAchieved = dailyLog.nutrition.protein !== "" && dailyLog.nutrition.protein >= 130;

    return (
        <div>

            {/* Section heading */}
            <h2>🔥 Achievement Banner</h2>

            {/* Motivational message */}
            <p>Great session today!</p>

            {/* Achievement summary */}
            <p>
                {dailyLog.workout.workoutCalories} Calories Burned • Day 24 / 90 • {proteinGoalAchieved ? "Protein Goal Achieved" : "Protein Goal Pending"}
            </p>

        </div>
    );

}

export default AchievementBanner;