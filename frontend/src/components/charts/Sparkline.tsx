/*
    Sparkline

    A small line showing how a value moved over time,
    e.g. weight across the weigh-ins in a period.

    The line is scaled to its own lowest and highest value,
    so small changes are visible; it shows the shape of the
    change, not exact numbers (those are in the card's text).
    Nothing is drawn with fewer than two points.
*/

/*
    values
        The values in time order.

    label
        What the line shows, for screen readers,
        e.g. "Weight trend".

    colorClass
        Tailwind text colour class; the line uses
        the current text colour.
*/
interface SparklineProps {
    values: number[];
    label: string;
    colorClass?: string;
}

/*
    The drawing area is 100 x 34 units, stretched to the
    card's width. The line keeps 4 units clear of the top
    and bottom.
*/
const WIDTH = 100;
const HEIGHT = 34;
const PADDING = 4;

function Sparkline({
    values,
    label,
    colorClass = "text-slate-400",
}: SparklineProps) {

    if (values.length < 2) {
        return null;
    }

    const lowest = Math.min(...values);
    const range = Math.max(...values) - lowest || 1;

    const points = values
        .map((value, index) => {
            const x = (index / (values.length - 1)) * WIDTH;
            const y = HEIGHT - PADDING - ((value - lowest) / range) * (HEIGHT - 2 * PADDING);
            return `${x.toFixed(1)},${y.toFixed(1)}`;
        })
        .join(" ");

    return (

        <svg
            role="img"
            aria-label={label}
            viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
            preserveAspectRatio="none"
            className={`mt-2 h-12 w-full ${colorClass}`}
        >
            <polyline
                points={points}
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                vectorEffect="non-scaling-stroke"
            />
        </svg>

    );

}

export default Sparkline;
