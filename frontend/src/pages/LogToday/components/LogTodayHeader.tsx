/*
    LogTodayHeader

    Displays the page heading and
    information about the selected
    Daily Log.
*/

interface LogTodayHeaderProps {
    selectedDate: string;
    isDirty: boolean;
}

function LogTodayHeader({
    selectedDate,
    isDirty,
}: LogTodayHeaderProps) {

    /*
        Format the selected date into
        a more readable form.
    */
    const formattedDate = new Date(selectedDate).toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
        }
    );

    return (
        <div>

            <h1>Log Today</h1>

            <hr />

            <div>

                <div>
                    <p>{formattedDate}</p>
                </div>

            </div>

            <div>

                <div>
                    <p>{isDirty ? "● Unsaved Changes" : "✓ Saved"}</p>
                </div>

            </div>

        </div>
    );

}

export default LogTodayHeader;