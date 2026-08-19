/*
    MealTimingSection

    Displays and updates the meal timing
    information for the current day.

    The actual state is owned by LogToday.
    This component receives the current
    DailyLog object and the function used
    to update it.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent
    LogToday component.
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

        <section>

            {/* First Meal Time */}
            <TextInput
                label="First Meal Time"
                id="first-meal-time"
                name="firstMealTime"
                type="time"
                value={dailyLog.mealTiming.firstMealTime}
                onChange={(event) => {

                    /*
                        Triggered whenever the user changes
                        the First Meal Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Meal Timing object.
                        4. Update only the First Meal Time.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */

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
                onChange={(event) => {

                    /*
                        Triggered whenever the user changes
                        the Last Meal Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Meal Timing object.
                        4. Update only the Last Meal Time.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */
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