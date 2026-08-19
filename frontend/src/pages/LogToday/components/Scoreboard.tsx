/*
    Scoreboard

    Displays today's key metrics.

    All values are read from the
    current Daily Log.
*/

import Card from "../../../components/Card";
import ProgressBar from "../../../components/ProgressBar";
import type { DailyLog } from "../../../types/DailyLog";

interface ScoreboardProps {
    dailyLog: DailyLog;
}

function Scoreboard({ dailyLog }: ScoreboardProps) {

    const startingWeight = 82;
    const goalWeight = 75;

    const currentWeight = dailyLog.body.weight === "" ? startingWeight : Number(dailyLog.body.weight);

    return (

        <Card>

            <h2
                className="
                    text-xl
                    font-semibold
                    text-slate-900
                    mb-6
                "
            >
                Summary
            </h2>

            <div
                className="
                    space-y-6
                "
            >

                <ProgressBar
                    label="Protein"
                    current={Number(dailyLog.nutrition.protein ?? 0)}
                    goal={130}
                    unit="g"
                />

                <ProgressBar
                    label="Water"
                    current={Number(dailyLog.hydration.water ?? 0)}
                    goal={3000}
                    unit="ml"
                />

                <ProgressBar
                    label="Steps"
                    current={Number(dailyLog.activity.steps ?? 0)}
                    goal={10000}
                />

                <ProgressBar
                    label="Weight"
                    current={startingWeight - currentWeight}
                    goal={startingWeight - goalWeight}
                    displayCurrent={`${currentWeight}kg`}
                    displayGoal={`${goalWeight}kg`}
                />

            </div>

        </Card>

    );

}

export default Scoreboard;