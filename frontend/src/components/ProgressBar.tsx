/*
    ProgressBar

    Displays progress towards a goal.

    Example:
    Protein   110 / 130 g
    ███████░░░░░
*/

interface ProgressBarProps {
    label: string;
    current: number;
    goal: number;
    unit?: string;
    color?: string;

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

    const percentage = Math.min(
        (current / goal) * 100,
        100
    );

    return (
        <div className="space-y-2">

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
                    {displayCurrent ?? `${current}${unit}`} / {displayGoal ?? `${goal}${unit}`}
                </p>

            </div>

            <div
                className="
                    h-2
                    rounded-full
                    bg-slate-200
                    overflow-hidden
                "
            >
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