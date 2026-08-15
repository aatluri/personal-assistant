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
interface DateSectionProps {
    selectedDate: string;
    setSelectedDate: Dispatch<SetStateAction<string>>;
}

function DateSection({
    selectedDate,
    setSelectedDate,
}: DateSectionProps) {

    return (
        <section>

            <h2>Date</h2>

            <TextInput
                label="Log Date"
                id="log-date"
                name="logDate"
                type="date"
                value={selectedDate}
                onChange={(event) => {

                    /*
                        Triggered whenever the user
                        changes the Log Date.
                    */

                    const newDate = event.target.value;
                    console.log("Selected Date changed:", newDate);
                    setSelectedDate(newDate);

                }}
            />

        </section>
    );

}

export default DateSection;