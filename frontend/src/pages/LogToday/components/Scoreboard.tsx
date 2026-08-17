/*
    Scoreboard

    Displays today's key metrics.

    All values are read from the
    current Daily Log.
*/

import type { DailyLog } from "../../../types/DailyLog";
import { calculateSleepDuration } from "../../../utils/calculateSleepDuration";

interface ScoreboardProps {
    dailyLog: DailyLog;
}

function Scoreboard({ dailyLog }: ScoreboardProps) {

    /*
        Convert water from ml to litres.
    */
    const waterLitres =dailyLog.hydration.water === ""? "-": (dailyLog.hydration.water / 1000).toFixed(1);

    return (
        <div>

            <h2>Today's Scoreboard</h2>

            <p>Weight: {dailyLog.body.weight} kg</p>

            <p>
                Protein: {dailyLog.nutrition.protein} / 130 g
            </p>

            <p>
                Water: {waterLitres} / 3.0 L
            </p>

            <p>
                Sleep:{" "}
                {calculateSleepDuration(
                    dailyLog.sleep.sleepStartTime,
                    dailyLog.sleep.sleepEndTime
                )}
            </p>

            <p>
                Steps: {(dailyLog.activity.steps ?? 0).toLocaleString()}
            </p>

            <p>
                Calories: {dailyLog.workout.workoutCalories} / {dailyLog.activity.totalCaloriesBurnt}
            </p>

        </div>
    );

}

export default Scoreboard;