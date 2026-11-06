/*
BodyCard

Weight, body fat and waist.

The latest values are the most recent measurement up to
the end of the period, even when older than the period,
so the card says how old the weight is. Week and Month
also show the change from the first to the last
measurement in the period; a change has no good or bad
colour, since the right direction depends on your goal.
The line shows the weight across the weigh-ins (the last
30 days in Day view).
*/

import { Scale } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import Sparkline from "../../../components/charts/Sparkline";

import { formatCount, formatNumber, MISSING } from "../../../utils/overviewFormat";

import OverviewCard from "./OverviewCard";


interface BodyCardProps {
    summary: DashboardSummary;
}

/*
"↓ 0.6 kg", "↑ 1 cm", "±0 kg", or "" when there is no
change to show.
*/
function changeText(change: number | null, unit: string): string {

    if (change === null) {
        return "";
    }

    const size = formatNumber(Math.abs(change), 1);

    if (size === "0") {
        return `±0${unit}`;
    }

    return `${change > 0 ? "↑" : "↓"} ${size}${unit}`;

}

/*
"Weighed today", "Weighed yesterday", "Weighed 3 days ago".
*/
function weighedText(daysOld: number | null): string {

    if (daysOld === null) {
        return "No weigh-ins yet";
    }

    if (daysOld === 0) {
        return "Weighed today";
    }

    return daysOld === 1 ? "Weighed yesterday" : `Weighed ${daysOld} days ago`;

}

/*
One row: the measurement, its latest value, and its
change in Week / Month views.
*/
function BodyRow({
    label,
    value,
    change,
}: {
    label: string;
    value: string;
    change: string;
}) {

    return (

        <div
            className="
                flex
                justify-between
                border-t
                border-slate-100
                py-1.5
                text-sm
            "
        >
            <span className="text-slate-500">{label}</span>

            <span className="text-slate-900">
                {value}
                {change && (
                    <span className="ml-2 text-xs text-slate-500">({change})</span>
                )}
            </span>
        </div>

    );

}

function BodyCard({ summary }: BodyCardProps) {

    const { body } = summary;
    const isDay = summary.period === "day";

    const note = {
        day: "latest",
        week: "this week",
        month: "this month",
    }[summary.period];

    const detail = isDay
        ? weighedText(body.weightDaysOld)
        : `${formatCount(body.weighIns, "weigh-in")} this ${summary.period}`;

    return (

        <OverviewCard
            title="Body"
            icon={Scale}
            iconColor="text-slate-500"
            note={note}
        >

            <p className="text-2xl font-semibold text-slate-900">
                {formatNumber(body.latestWeightKg, 1)}
                <span className="ml-1 text-sm font-normal text-slate-500">kg</span>

                {!isDay && body.weightChangeKg !== null && (
                    <span className="ml-2 text-xs font-normal text-slate-500">
                        {changeText(body.weightChangeKg, " kg")}
                    </span>
                )}
            </p>

            <p className="text-xs text-slate-500">{detail}</p>

            <Sparkline
                values={body.trend.map((point) => point.weightKg)}
                label="Weight trend"
            />

            <div className="mt-2">
                <BodyRow
                    label="Body fat"
                    value={
                        body.latestBodyFatPercent === null
                            ? MISSING
                            : `${formatNumber(body.latestBodyFatPercent, 1)}%`
                    }
                    change={isDay ? "" : changeText(body.bodyFatChangePercent, "")}
                />

                <BodyRow
                    label="Waist"
                    value={
                        body.latestWaistCm === null
                            ? MISSING
                            : `${formatNumber(body.latestWaistCm, 1)} cm`
                    }
                    change={isDay ? "" : changeText(body.waistChangeCm, " cm")}
                />
            </div>

        </OverviewCard>

    );

}

export default BodyCard;
