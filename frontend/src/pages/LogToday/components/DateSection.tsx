/*
    LogDateSection

    Displays and updates the date
    for the current Daily Log.

    The selected date determines
    which Daily Log is being edited.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent
    LogToday component.
*/
interface LogDateSectionProps {
    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;
}

function LogDateSection({
    dailyLog,
    setDailyLog,
}: LogDateSectionProps) {

    return (
        <section>

            <h2>Date</h2>

            <TextInput
                label="Log Date"
                id="log-date"
                name="logDate"
                type="date"
                value={dailyLog.date}
                onChange={(event) => {

                    /*
                        Triggered whenever the user
                        changes the Log Date.
                    */

                    const newDate = event.target.value;

                    setDailyLog((previousDailyLog) => ({
                        ...previousDailyLog,
                        date: newDate,
                    }));

                }}
            />

        </section>
    );

}

export default LogDateSection;