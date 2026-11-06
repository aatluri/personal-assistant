/*
HeadlineNumbers

The four numbers at the top of the Overview: steps,
sleep, resting heart rate and workouts, each compared
with the usual (Day) or the previous period (Week /
Month).
*/

import type { DashboardSummary } from "../../../types/DashboardSummary";

import {
    describeChange,
    formatComparisonLabel,
    formatHours,
    formatMinutes,
    formatNumber,
    type Change,
} from "../../../utils/overviewFormat";

import { TONE_CLASSES } from "./tones";


/*
One headline tile: a label, a value, and a line below
it (a change, or extra detail). "avg" is added to the
label for weeks and months.
*/
function HeadlineNumber({
    label,
    isAverage,
    value,
    detail,
}: {
    label: string;
    isAverage: boolean;
    value: string;
    detail: Change | null;
}) {

    return (

        <div
            className="
                rounded-xl
                border
                border-slate-200
                bg-white
                p-4
            "
        >

            <p className="text-sm text-slate-500">
                {label}
                {isAverage && (
                    <span className="text-slate-400"> avg</span>
                )}
            </p>

            <p
                className="
                    mt-1
                    text-2xl
                    font-semibold
                    text-slate-900
                "
            >
                {value}
            </p>

            <p
                className={`
                    mt-1
                    min-h-5
                    text-xs
                    ${detail ? TONE_CLASSES[detail.tone] : ""}
                `}
            >
                {detail?.text}
            </p>

        </div>

    );

}


/*
The workouts tile's detail line:
- Day:   "Strength · 55 min", "2 sessions · 89 min" or "Rest day"
- Week / Month: "210 min · 2,310 kcal"
*/
function describeWorkouts(summary: DashboardSummary): Change {

    const totals = summary.current.workouts;

    if (summary.period !== "day") {
        return {
            text: `${formatNumber(totals?.minutes ?? 0)} min · `
                + `${formatNumber(totals?.activeEnergyKcal ?? 0)} kcal`,
            tone: "neutral",
        };
    }

    if (summary.workouts.length === 0) {
        return { text: "Rest day", tone: "neutral" };
    }

    if (summary.workouts.length === 1) {
        const workout = summary.workouts[0];

        return {
            text: `${workout.workoutType} · `
                + `${formatNumber(workout.workoutDurationMin)} min`,
            tone: "neutral",
        };
    }

    return {
        text: `${summary.workouts.length} sessions · `
            + `${formatNumber(totals?.minutes ?? 0)} min`,
        tone: "neutral",
    };

}


function HeadlineNumbers({ summary }: { summary: DashboardSummary }) {

    const { current, comparison } = summary;
    const label = formatComparisonLabel(summary);
    const isAverage = summary.period !== "day";

    /*
    Steps change: the difference for a day ("↑ 1,100"),
    a percentage for a week or month ("↑ 6%").
    */
    const stepsChange = describeChange(
        current.stepsAverage,
        comparison.stepsAverage,
        label,
        true,
        (difference) => summary.period === "day"
            ? formatNumber(difference)
            : `${Math.round(
                (difference / (comparison.stepsAverage ?? 1)) * 100
            )}%`,
    );

    return (

        <section
            aria-label="Headline numbers"
            className="
                grid
                grid-cols-2
                gap-3
                sm:grid-cols-4
            "
        >

            <HeadlineNumber
                label="Steps"
                isAverage={isAverage}
                value={formatNumber(current.stepsAverage)}
                detail={stepsChange}
            />

            <HeadlineNumber
                label="Sleep"
                isAverage={isAverage}
                value={formatHours(current.sleepHoursAverage)}
                detail={describeChange(
                    current.sleepHoursAverage,
                    comparison.sleepHoursAverage,
                    label,
                    true,
                    (difference) => formatMinutes(difference * 60),
                )}
            />

            <HeadlineNumber
                label="Resting HR"
                isAverage={isAverage}
                value={formatNumber(current.restingHeartRateBpmAverage)}
                detail={describeChange(
                    current.restingHeartRateBpmAverage,
                    comparison.restingHeartRateBpmAverage,
                    label,
                    false,
                    (difference) => formatNumber(difference, 1),
                )}
            />

            <HeadlineNumber
                label="Workouts"
                isAverage={false}
                value={formatNumber(current.workouts?.count ?? 0)}
                detail={describeWorkouts(summary)}
            />

        </section>

    );

}

export default HeadlineNumbers;
