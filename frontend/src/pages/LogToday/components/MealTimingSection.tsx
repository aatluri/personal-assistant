/*
    MealTimingSection

    Displays and updates the user's
    meal timing information.

    Responsibilities:
    - Display meal timing fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on meal timing data.

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
interface MealTimingSectionProps {

    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function MealTimingSection({

    dailyLog,

    setDailyLog,

}: MealTimingSectionProps) {

    return (

        /*
            Display the Meal Timing section.
        */
        <section>

            {/* First Meal Time */}
            <TextInput
                label="First Meal Time"
                id="first-meal-time"
                name="firstMealTime"
                type="time"
                value={dailyLog.mealTiming.firstMealTime}
                /*
                        Triggered whenever the user changes
                        the First Meal Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Meal Timing object.
                        4.Update only the First Meal Time while preserving the rest of the DailyLog.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                */

                onChange={(event) => {

                    const newFirstMealTime = event.target.value;
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        mealTiming: {
                            ...previousDailyLog.mealTiming,
                            firstMealTime: newFirstMealTime,

                        },

                    }));

                }}
            />

            {/* Last Meal Time */}
            <TextInput
                label="Last Meal Time"
                id="last-meal-time"
                name="lastMealTime"
                type="time"
                value={dailyLog.mealTiming.lastMealTime}
                /*
                        Triggered whenever the user changes
                        the Last Meal Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Meal Timing object.
                        4. Update only the Last Meal Time while preserving the rest ofthe DailyLog.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */
                onChange={(event) => {
                    const newLastMealTime = event.target.value;
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        mealTiming: {
                            ...previousDailyLog.mealTiming,
                            lastMealTime: newLastMealTime,
                        },

                    }));

                }}
            />

        </section>

    );

}

export default MealTimingSection;