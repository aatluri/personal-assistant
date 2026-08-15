/*
    LogTodayHeader

    Displays the page heading and
    information about the selected
    Daily Log.
*/

interface LogTodayHeaderProps {
    selectedDate: string;
}

function LogTodayHeader({
    selectedDate,
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
                    <p>Good Evening</p>
                </div>

                <div>
                    <p>{formattedDate}</p>
                </div>

            </div>

            <div>

                <div>
                    <p>Day 24 / 90</p>
                </div>

                <div>
                    <p>✓ Saved</p>
                </div>

            </div>

        </div>
    );

}

export default LogTodayHeader;