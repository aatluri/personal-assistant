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
        <div
            className="
                mb-8
            "
        >

            <h1
                className="
                    text-3xl
                    font-bold
                    text-slate-900
                "
            >
                Log Today
            </h1>

            <div
                className="
                    mt-3
                    flex
                    items-center
                    justify-between
                "
            >

                <p
                    className="
                        text-base
                        text-slate-600
                    "
                >
                    {formattedDate}
                </p>

                <p
                    className={`
                        text-sm
                        font-medium
                        ${
                            isDirty
                                ? "text-amber-600"
                                : "text-green-600"
                        }
                    `}
                >
                    {isDirty ? "● Unsaved Changes" : "✓ Saved"}
                </p>

            </div>

        </div>
    );

}

export default LogTodayHeader;