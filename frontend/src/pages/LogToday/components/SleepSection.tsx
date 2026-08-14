/*
    SleepSection

    Displays and updates the user's
    sleep start and end times.

    The actual state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent
    LogToday component.
*/
interface SleepSectionProps {

    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function SleepSection({
    dailyLog,
    setDailyLog,

}: SleepSectionProps) {

    return (
        <section>
            {/* Section Heading */}
            <h2>Sleep</h2>

            {/* Sleep Start Time */}
            <TextInput
                label="Sleep Start Time"
                id="sleep-start-time"
                name="sleepStartTime"
                type="time"
                value={dailyLog.sleep.sleepStartTime}
                onChange={(event) => {

                    /*
                        Triggered whenever the user changes
                        the Sleep Start Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Sleep object.
                        4. Update only the Sleep Start Time.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */

                    const newSleepStartTime = event.target.value;

                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        sleep: {
                            ...previousDailyLog.sleep,
                            sleepStartTime: newSleepStartTime,

                        },

                    }));

                }}
            />

            {/* Sleep End Time */}
            <TextInput
                label="Sleep End Time"
                id="sleep-end-time"
                name="sleepEndTime"
                type="time"
                value={dailyLog.sleep.sleepEndTime}
                onChange={(event) => {

                    /*
                        Triggered whenever the user changes
                        the Sleep End Time.

                        Steps:
                        1. Read the new time.
                        2. Copy the existing DailyLog.
                        3. Copy the Sleep object.
                        4. Update only the Sleep End Time.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */

                    const newSleepEndTime = event.target.value;
                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        sleep: {
                            ...previousDailyLog.sleep,
                            sleepEndTime: newSleepEndTime,
                        },

                    }));

                }}
            />

        </section>

    );

}

export default SleepSection;