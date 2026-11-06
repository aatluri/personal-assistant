/*
ActivityCard

Steps and active energy.

- Day: that day's steps, active energy and flights.
  Steps are stored once per day, so the chart shows the
  7 days ending on that day (hourly bars are not possible).
- Week / Month: the average per day, the total, and the
  average active energy per day.
*/

import { Footprints } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import BarSeries from "../../../components/charts/BarSeries";

import { formatNumber } from "../../../utils/overviewFormat";

import { dailyChartProps } from "./dailyChart";
import OverviewCard from "./OverviewCard";


interface ActivityCardProps {
    summary: DashboardSummary;
    onSelectDay: (date: string) => void;
}

function ActivityCard({ summary, onSelectDay }: ActivityCardProps) {

    const { current } = summary;
    const isDay = summary.period === "day";
    const today = summary.days[summary.days.length - 1];

    const note = isDay
        ? (summary.isCurrent ? "today" : "this day")
        : "avg per day";

    let detail: string;

    if (current.stepsAverage === null) {
        detail = "No activity recorded";
    } else if (isDay) {
        detail = `${formatNumber(current.activeEnergyKcalAverage)} active kcal`
            + ` · ${formatNumber(today?.flightsClimbed ?? null)} flights`;
    } else {
        detail = `${formatNumber(current.stepsTotal)} total`
            + ` · ${formatNumber(current.activeEnergyKcalAverage)} active kcal/day`;
    }

    /*
    Week / Month: say when some days have no steps, so the
    average is read correctly.
    */
    const coverage = !isDay && current.activityDays < current.days
        ? `Recorded on ${current.activityDays} of ${current.days} days`
        : "";

    return (

        <OverviewCard
            title="Activity"
            icon={Footprints}
            iconColor="text-teal-600"
            note={note}
        >

            <p className="text-2xl font-semibold text-slate-900">
                {formatNumber(current.stepsAverage)}
                <span className="ml-1 text-sm font-normal text-slate-500">steps</span>
            </p>

            <p className="text-xs text-slate-500">{detail}</p>

            {coverage && (
                <p className="text-xs text-slate-400">{coverage}</p>
            )}

            <BarSeries
                values={summary.days.map((day) => day.steps)}
                colorClass="bg-teal-500"
                {...dailyChartProps(
                    summary,
                    onSelectDay,
                    (day) => day.steps === null
                        ? "no steps recorded"
                        : `${formatNumber(day.steps)} steps`
                )}
            />

        </OverviewCard>

    );

}

export default ActivityCard;
