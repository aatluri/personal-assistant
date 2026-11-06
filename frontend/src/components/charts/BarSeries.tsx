/*
    BarSeries

    A small bar chart with one bar per day, used by the
    Overview cards.

    Responsibilities:
    - Draw each value as a bar, scaled to the largest value.
    - Draw days with no data as a thin grey gap, never as a
      zero-height bar, so "nothing recorded" and "zero" never
      look alike.
    - Optionally highlight one bar (the selected day) by
      dimming the others.
    - Optionally make each bar a button (e.g. tap a day to
      open it).
*/

/*
    values
        One value per bar; null for a day with no data.

    labels
        One axis label per bar; use "" to leave a bar
        unlabelled (e.g. a month shows only every 7th day).

    colorClass
        Tailwind background class for the bars,
        e.g. "bg-violet-400".

    describeBar
        Text for each bar, for screen readers and as the
        button name, e.g. "Mon, Nov 2: 9,210 steps".

    highlightIndex
        Optional. The bar to emphasise; the others are dimmed.

    onSelect
        Optional. Called with a bar's index when it is
        tapped. Bars with no data cannot be tapped.

    heightClass
        Optional Tailwind height class for the chart area.
*/
interface BarSeriesProps {
    values: (number | null)[];
    labels: string[];
    colorClass: string;
    describeBar: (index: number) => string;
    highlightIndex?: number;
    onSelect?: (index: number) => void;
    heightClass?: string;
}

function BarSeries({
    values,
    labels,
    colorClass,
    describeBar,
    highlightIndex,
    onSelect,
    heightClass = "h-14",
}: BarSeriesProps) {

    const largest = Math.max(
        ...values.filter((value): value is number => value !== null),
        0
    );

    return (

        <div className="mt-3">

            <div
                className={`
                    flex
                    items-end
                    gap-[3px]
                    ${heightClass}
                `}
            >
                {values.map((value, index) => {

                    if (value === null) {
                        return (
                            <div
                                key={index}
                                data-testid="bar-gap"
                                aria-label={describeBar(index)}
                                className="h-[3px] flex-1 rounded-sm bg-slate-200"
                            />
                        );
                    }

                    const isDimmed =
                        highlightIndex !== undefined && index !== highlightIndex;

                    const style = {
                        height: `${Math.max(6, (value / (largest || 1)) * 100)}%`,
                    };

                    const className = `
                        flex-1
                        rounded-t-sm
                        ${colorClass}
                        ${isDimmed ? "opacity-35" : ""}
                    `;

                    return onSelect ? (
                        <button
                            key={index}
                            type="button"
                            aria-label={describeBar(index)}
                            onClick={() => onSelect(index)}
                            style={style}
                            className={`${className} hover:brightness-110`}
                        />
                    ) : (
                        <div
                            key={index}
                            role="img"
                            aria-label={describeBar(index)}
                            style={style}
                            className={className}
                        />
                    );

                })}
            </div>

            <div className="mt-1 flex gap-[3px] text-[11px] text-slate-400">
                {labels.map((label, index) => (
                    <span key={index} className="flex-1 text-center">
                        {label}
                    </span>
                ))}
            </div>

        </div>

    );

}

export default BarSeries;
