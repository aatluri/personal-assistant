/*
    StackedBar

    One horizontal bar split into parts, with a legend,
    e.g. sleep stages (deep / core / REM / awake) or
    macros (protein / carbs / fat).

    Each part's width is its share of the total, and the
    legend shows that share as a percentage.
*/

export interface StackedBarPart {
    label: string;
    value: number;
    colorClass: string;
}

/*
    parts
        The parts in order; parts with no value (0) are
        left out of the bar but stay in the legend.

    label
        What the bar shows, for screen readers,
        e.g. "Sleep stages".
*/
interface StackedBarProps {
    parts: StackedBarPart[];
    label: string;
}

function StackedBar({ parts, label }: StackedBarProps) {

    const total = parts.reduce((sum, part) => sum + part.value, 0);

    const share = (part: StackedBarPart) =>
        total === 0 ? 0 : Math.round((part.value / total) * 100);

    return (

        <div className="mt-3">

            <div
                role="img"
                aria-label={
                    `${label}: `
                    + parts.map((part) => `${part.label} ${share(part)}%`).join(", ")
                }
                className="flex h-2 overflow-hidden rounded-full bg-slate-100"
            >
                {parts.map((part) => (
                    <div
                        key={part.label}
                        className={part.colorClass}
                        style={{ width: `${share(part)}%` }}
                    />
                ))}
            </div>

            <div
                className="
                    mt-1
                    flex
                    flex-wrap
                    gap-x-3
                    gap-y-1
                    text-[11px]
                    text-slate-500
                "
            >
                {parts.map((part) => (
                    <span key={part.label} className="flex items-center gap-1">
                        <span
                            aria-hidden="true"
                            className={`inline-block h-2 w-2 rounded-sm ${part.colorClass}`}
                        />
                        {part.label} {share(part)}%
                    </span>
                ))}
            </div>

        </div>

    );

}

export default StackedBar;
