/*
Highlights

The Overview's highlights, above the headline numbers, in
two groups:
- Goal rings: one ring per goal (Day: progress towards the
  day's goal; Week / Month: how many days met it), filled
  to the share completed and coloured by how complete it
  is, from red to green (COMPLETION_BANDS), with a tick
  when the goal is fully met.
- Record badges: the step streak and the bests (best
  sleep, most steps, furthest workout), as gold pills.

The backend decides which highlights there are, their
order and every part of them (highlights.py); a highlight
with progress is a goal, one without is a record. A group
with nothing in it is left out, and nothing is shown when
there are no highlights.
*/

import {
    Check,
    Droplet,
    Flame,
    Footprints,
    Medal,
    Moon,
    Salad,
    type LucideIcon,
} from "lucide-react";

import type { Highlight } from "../../../types/DashboardSummary";


/*
A ring's colour by how complete the goal is, from red to
green. Each band covers the percentages above the previous
band's limit, up to and including its own. The percentage
used is the one shown in the ring (rounded), so the colour
and the number always agree.
*/
const COMPLETION_BANDS = [
    { upTo: 30, name: "red", stroke: "stroke-rose-500", text: "text-rose-600" },
    { upTo: 50, name: "orange", stroke: "stroke-orange-500", text: "text-orange-600" },
    { upTo: 70, name: "amber", stroke: "stroke-amber-400", text: "text-amber-600" },
    { upTo: 90, name: "lime", stroke: "stroke-lime-500", text: "text-lime-700" },
    { upTo: 100, name: "green", stroke: "stroke-green-500", text: "text-green-600" },
];

/*
The topic's icon and colour beside a ring's caption,
matching the cards.
*/
const TOPIC_ICONS: Partial<Record<Highlight["topic"], { icon: LucideIcon; className: string }>> = {
    steps: { icon: Footprints, className: "text-teal-600" },
    sleep: { icon: Moon, className: "text-violet-600" },
    protein: { icon: Salad, className: "text-amber-600" },
    water: { icon: Droplet, className: "text-sky-600" },
};

/*
The ring is drawn in a 64 x 64 box: radius 28 with a
6-unit stroke.
*/
const RADIUS = 28;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;


function completionBand(percent: number) {

    return (
        COMPLETION_BANDS.find((band) => percent <= band.upTo)
        ?? COMPLETION_BANDS[COMPLETION_BANDS.length - 1]
    );

}


function GoalRing({ highlight }: { highlight: Highlight }) {

    const progress = highlight.progress ?? 0;
    const percent = Math.round(progress * 100);
    const colours = completionBand(percent);
    const topic = TOPIC_ICONS[highlight.topic];

    return (

        <li
            aria-label={highlight.text}
            data-completion={colours.name}
            className="flex w-24 flex-col items-center text-center"
        >

            <div className="relative h-16 w-16">

                <svg viewBox="0 0 64 64" className="h-16 w-16" aria-hidden="true">
                    <circle
                        cx="32"
                        cy="32"
                        r={RADIUS}
                        fill="none"
                        strokeWidth="6"
                        className="stroke-slate-100"
                    />

                    {/*
                        The arc starts at 12 o'clock and runs clockwise.
                        At 0% there is no arc (a rounded line end would
                        still draw a dot), so the ring is empty.
                    */}
                    {percent > 0 && (
                        <circle
                            data-testid="ring-arc"
                            cx="32"
                            cy="32"
                            r={RADIUS}
                            fill="none"
                            strokeWidth="6"
                            strokeLinecap="round"
                            strokeDasharray={`${(progress * CIRCUMFERENCE).toFixed(1)} ${CIRCUMFERENCE.toFixed(1)}`}
                            transform="rotate(-90 32 32)"
                            className={colours.stroke}
                        />
                    )}
                </svg>

                <span
                    className={`
                        absolute
                        inset-0
                        flex
                        items-center
                        justify-center
                        text-sm
                        font-semibold
                        ${colours.text}
                    `}
                >
                    {highlight.goalMet ? (
                        <Check size={20} strokeWidth={3} aria-hidden="true" data-testid="goal-met" />
                    ) : (
                        `${percent}%`
                    )}
                </span>

            </div>

            <p className="mt-1 text-sm font-semibold text-slate-900">
                {highlight.value}
            </p>

            <p className="flex items-center gap-1 text-xs text-slate-500">
                {topic && (
                    <topic.icon size={12} aria-hidden="true" className={`shrink-0 ${topic.className}`} />
                )}
                {highlight.label}
            </p>

            {highlight.detail && (
                <p className="text-xs text-slate-400">{highlight.detail}</p>
            )}

        </li>

    );

}


function RecordBadge({ highlight }: { highlight: Highlight }) {

    const isStreak = highlight.topic === "streak";
    const Icon = isStreak ? Flame : Medal;

    return (

        <li
            aria-label={highlight.text}
            className="
                flex
                items-center
                gap-1.5
                rounded-full
                border
                border-yellow-200
                bg-yellow-50
                px-3
                py-1
                text-xs
                text-slate-700
            "
        >
            <Icon
                size={14}
                aria-hidden="true"
                className={`shrink-0 ${isStreak ? "text-orange-500" : "text-yellow-600"}`}
            />

            <span>
                {/* Capitalise the caption, which reads as a title here. */}
                {highlight.label.charAt(0).toUpperCase() + highlight.label.slice(1)}
                {" · "}
                <span className="font-semibold text-slate-900">{highlight.value}</span>
                {highlight.detail && ` · ${highlight.detail}`}
            </span>
        </li>

    );

}


function Highlights({ highlights }: { highlights: Highlight[] }) {

    const goals = highlights.filter((highlight) => highlight.progress !== null);
    const records = highlights.filter((highlight) => highlight.progress === null);

    if (highlights.length === 0) {
        return null;
    }

    return (

        <section aria-label="Highlights" className="space-y-3">

            {goals.length > 0 && (
                <ul aria-label="Goals" className="flex flex-wrap gap-2">
                    {goals.map((highlight) => (
                        <GoalRing key={highlight.text} highlight={highlight} />
                    ))}
                </ul>
            )}

            {records.length > 0 && (
                <ul aria-label="Records" className="flex flex-wrap gap-2">
                    {records.map((highlight) => (
                        <RecordBadge key={highlight.text} highlight={highlight} />
                    ))}
                </ul>
            )}

        </section>

    );

}

export default Highlights;
