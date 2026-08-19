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