/*
    SleepSection

    Displays and updates the user's
    sleep information.

    Responsibilities:
    - Display sleep-related fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on sleep data.

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
    /*
        Display the Sleep section.
    */
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

                {/* Sleep Start Time */}
                <TextInput
                    label="Sleep Start Time"
                    id="sleep-start-time"
                    name="sleepStartTime"
                    type="time"
                    value={dailyLog.sleep.sleepStartTime}
                    /*
                        Update only the Sleep Start Time
                        while preserving the rest of
                        the DailyLog.
                    */
                    onChange={(event) => {

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
                    /*
                        Update only the Sleep End Time
                        while preserving the rest of
                        the DailyLog.
                    */
                    onChange={(event) => {

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

            </div>

        </section>

    );

}

export default SleepSection;