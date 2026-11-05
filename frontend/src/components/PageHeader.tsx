/*
    PageHeader

    Displays the page heading together
    with the current save status.

    Shared by the metric logging pages.

    Responsibilities:
    - Display the page title.
    - Indicate whether the page contains
      unsaved changes.
*/

/*
    title
        Page heading, e.g. "Nutrition Metrics".

    isDirty
        Indicates whether the page
        contains unsaved changes.

        Optional: read-only pages leave it out,
        and no save status is shown.
*/

interface PageHeaderProps {
    title: string;
    isDirty?: boolean;
}

function PageHeader({
    title,
    isDirty,
}: PageHeaderProps) {


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
                {title}
            </h1>

            {/*
                    Display the current save status.

                    The colour and text change depending
                    on whether the page has unsaved changes.
                    Read-only pages pass no isDirty, so no
                    status is shown.
            */}
            {isDirty !== undefined && (
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
            )}

        </div>
    );

}

export default PageHeader;