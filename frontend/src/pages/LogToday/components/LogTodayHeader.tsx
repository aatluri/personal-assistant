/*
    LogTodayHeader

    Displays the page heading and
    information about the selected
    Daily Log.
*/

interface LogTodayHeaderProps {
    isDirty: boolean;
}

function LogTodayHeader({
    isDirty,
}: LogTodayHeaderProps) {


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