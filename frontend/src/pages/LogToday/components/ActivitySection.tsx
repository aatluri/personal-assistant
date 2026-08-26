/*
    ActivitySection

    Displays and updates the user's
    daily activity information.

    Responsibilities:
    - Display activity-related fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on activity data.

    The page state is owned by LogToday.
*/
import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    dailyLog
        The current Daily Log displayed on the page.

    setDailyLog
        Callback used to update the page state.
*/
interface ActivitySectionProps {
    dailyLog: DailyLog;
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;
}

function ActivitySection({
    dailyLog,
    setDailyLog,
}: ActivitySectionProps) {

    return (
        /*
            Display the Activity section.

            The section is arranged as a responsive
            two-column grid on larger screens.
        */
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

                    /*
                        Update only the Steps value while
                        preserving the rest of the DailyLog.
                    */
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
                     /*
                        Update only the Total Calories Burnt
                        value while preserving the rest of
                        the DailyLog.
                    */
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