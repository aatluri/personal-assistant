/*
    ActivitySection

    Displays and updates the user's
    daily activity information.

    The actual state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

interface ActivitySectionProps {
    dailyLog: DailyLog;
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;
}

function ActivitySection({
    dailyLog,
    setDailyLog,
}: ActivitySectionProps) {

    return (
        <section>

            <div
                className="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    gap-4
                "
            >

                <TextInput
                    label="Steps"
                    id="steps"
                    name="steps"
                    type="number"
                    min={0}
                    value={dailyLog.activity.steps}
                    onChange={(event) => {
                        const newSteps =
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value);

                        setDailyLog((previousDailyLog) => ({
                            ...previousDailyLog,
                            activity: {
                                ...previousDailyLog.activity,
                                steps: newSteps,
                            },
                        }));
                    }}
                />

                <TextInput
                    label="Total Calories Burnt"
                    id="total-calories-burnt"
                    name="totalCaloriesBurnt"
                    type="number"
                    min={0}
                    value={dailyLog.activity.totalCaloriesBurnt}
                    onChange={(event) => {
                        const newCalories =
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value);

                        setDailyLog((previousDailyLog) => ({
                            ...previousDailyLog,
                            activity: {
                                ...previousDailyLog.activity,
                                totalCaloriesBurnt: newCalories,
                            },
                        }));
                    }}
                />

            </div>

        </section>
    );
}

export default ActivitySection;