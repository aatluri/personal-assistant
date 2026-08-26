/*
    NotesSection

    Displays and updates the user's
    notes for the current day.

    Responsibilities:
    - Display the notes field.
    - Update the DailyLog state when the notes change.
    - Keep the UI focused only on notes.

    The page state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextArea from "../../../components/TextArea";
import type { DailyLog } from "../../../types/DailyLog";

/*
    dailyLog
        The current Daily Log displayed on the page.

    setDailyLog
        Callback used to update the page state.
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
        /*
            Display the Notes section.
        */

        <section>

            <div
                className="
                    space-y-6
                "
            >

                <TextArea
                    label="Notes"
                    id="notes"
                    name="notes"
                    rows={6}
                    placeholder="Enter any notes for today"
                    value={dailyLog.notes.notes}

                    /*
                            Triggered whenever the user changes
                            the Notes field.

                            Steps:
                            1. Read the new notes entered by the user.
                            2. Copy the existing DailyLog.
                            3. Copy the Notes object.
                            4. Update only the Notes field whilepreserving the rest of the DailyLog.
                            5. React stores the updated DailyLog
                               and re-renders the UI.
                        */

                    onChange={(event) => {
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

            </div>

        </section>

    );

}

export default NotesSection;