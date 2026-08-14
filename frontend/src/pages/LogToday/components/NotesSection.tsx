/*
    NotesSection

    Displays and updates the user's
    notes for the current day.

    The actual state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextArea from "../../../components/TextArea";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent
    LogToday component.
*/
interface NotesSectionProps {

    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function NotesSection({

    dailyLog,

    setDailyLog,

}: NotesSectionProps) {

    return (

        <section>

            {/* Section Heading */}
            <h2>Notes</h2>

            <TextArea
                label="Notes"
                id="notes"
                name="notes"
                rows={6}
                placeholder="Enter any notes for today"
                value={dailyLog.notes.notes}
                onChange={(event) => {

                    /*
                        Triggered whenever the user changes
                        the Notes field.

                        Steps:
                        1. Read the new notes entered by the user.
                        2. Copy the existing DailyLog.
                        3. Copy the Notes object.
                        4. Update only the Notes field.
                        5. React stores the updated DailyLog
                           and re-renders the UI.
                    */

                    const newNotes = event.target.value;

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        notes: {

                            ...previousDailyLog.notes,

                            notes: newNotes,

                        },

                    }));

                }}
            />

        </section>

    );

}

export default NotesSection;