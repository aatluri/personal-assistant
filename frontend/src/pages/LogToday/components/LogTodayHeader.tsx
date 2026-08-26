/*
    LogTodayHeader

    Displays the page heading together
    with the current save status.

    Responsibilities:
    - Display the page title.
    - Indicate whether the page contains
      unsaved changes.
*/

/*
    isDirty
        Indicates whether the page
        contains unsaved changes.
*/

interface LogTodayHeaderProps {
    isDirty: boolean;
}

function LogTodayHeader({
    isDirty,
}: LogTodayHeaderProps) {


    return (
        /*
            Display the page heading and
            current save status.
        */
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
                {/*
                        Display the current save status.

                        The colour and text change depending
                        on whether the page has unsaved changes.
                */}
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