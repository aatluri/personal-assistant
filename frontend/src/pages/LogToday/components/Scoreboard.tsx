/*
    Scoreboard

    Displays today's key metrics.

    All values are read from the
    current Daily Log.
*/

import type { DailyLog } from "../../../types/DailyLog";

interface ScoreboardProps {
    dailyLog: DailyLog;
}

function Scoreboard({ dailyLog }: ScoreboardProps) {

    /*
        Convert water from ml to litres.
    */
    const waterLitres = (dailyLog.hydration.water / 1000).toFixed(1);

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
                Sleep: Coming Soon
            </p>

            <p>
                Steps: {dailyLog.activity.steps.toLocaleString()}
            </p>

            <p>
                Calories: {dailyLog.workout.workoutCalories} / {dailyLog.activity.totalCaloriesBurnt}
            </p>

        </div>
    );

}

export default Scoreboard;