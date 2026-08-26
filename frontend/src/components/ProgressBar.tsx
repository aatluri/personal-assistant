/*
    ProgressBar

    Displays progress towards a goal using
    a horizontal progress bar.

    Responsibilities:
    - Display the metric name.
    - Display the current value and target.
    - Calculate the completion percentage.
    - Visually represent progress.

    Example:
    Protein   110 / 130 g
    ███████░░░░░
*/

interface ProgressBarProps {
    /*
        label
            Name of the metric being tracked.
            Example: Protein, Water, Steps
    */
    label: string;
    /*
        current
            Current progress value.
    */
    current: number;
    /*
        goal
            Target value to be achieved.
    */
    goal: number;
    /*
        unit
            Optional unit displayed after the
            current and goal values.
    */
    unit?: string;
    /*
        color
            Tailwind background colour used for
            the progress bar.
    */
    color?: string;
    /*
        Optional formatted display values.

        Useful when the displayed text differs
        from the numeric value used to calculate
        the progress percentage.
    */
    displayCurrent?: string;
    displayGoal?: string;
}

function ProgressBar({
    label,
    current,
    goal,
    unit = "",
    color = "bg-blue-600",
    displayCurrent,
    displayGoal,
}: ProgressBarProps) {

    /*
        Calculate the percentage of the goal
        that has been completed.

        The value is capped at 100% so the
        progress bar never exceeds its width.
    */
    const percentage = Math.min(
        (current / goal) * 100,
        100
    );

    return (
        <div className="space-y-2">
            {/* Display the label and current progress values. */}
            <div className="flex justify-between">

                <p
                    className="
                        text-sm
                        font-medium
                        text-slate-700
                    "
                >
                    {label}
                </p>

                <p
                    className="
                        text-sm
                        text-slate-500
                    "
                >
                    {/*
                        If formatted display values are supplied,
                        use them.

                        Otherwise display the numeric values
                        together with the optional unit.
                    */}
                    {displayCurrent ?? `${current}${unit}`} / {displayGoal ?? `${goal}${unit}`}
                </p>

            </div>

            {/*
                Outer progress bar representing the
                total goal.
            */}
            <div
                className="
                    h-2
                    rounded-full
                    bg-slate-200
                    overflow-hidden
                "
            >
                {/*
                    Filled portion of the progress bar.

                    The width is determined by the
                    calculated completion percentage.
                */}
                <div
                    className={`
                        h-full
                        rounded-full
                        transition-all
                        ${color}
                    `}
                    style={{
                        width: `${percentage}%`,
                    }}
                />

            </div>

        </div>
    );

}

export default ProgressBar;