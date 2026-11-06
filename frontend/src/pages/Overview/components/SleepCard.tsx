/*
SleepCard

Sleep for the period. Each night belongs to the day you
woke up, so Day view shows the night that ended that
morning ("last night" for today).

- Day: that night's duration, bed and wake times, and
  whether the goal was met.
- Week / Month: the average per night.
- Both: the stage split (deep / core / REM / awake) and
  a bar per night.
*/

import { Moon } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import BarSeries from "../../../components/charts/BarSeries";
import StackedBar from "../../../components/charts/StackedBar";

import {
    formatCount,
    formatHours,
    formatTime,
} from "../../../utils/overviewFormat";

import { dailyChartProps } from "./dailyChart";
import OverviewCard from "./OverviewCard";


interface SleepCardProps {
    summary: DashboardSummary;
    onSelectDay: (date: string) => void;
}

function SleepCard({ summary, onSelectDay }: SleepCardProps) {

    const { current, goals } = summary;
    const isDay = summary.period === "day";
    const night = summary.days[summary.days.length - 1];

    const note = isDay
        ? (summary.isCurrent ? "last night" : "the night before")
        : `avg per night · ${formatCount(current.sleepNights, "night")}`;

    /*
    Day view: "Bed 23:40 → woke 06:52 · goal 7h met".
    */
    let detail = "";

    if (isDay && current.sleepHoursAverage !== null) {
        const goalText = current.sleepHoursAverage >= goals.sleepHours
            ? "met"
            : "not met";

        detail = night?.sleepStartTime && night.sleepEndTime
            ? `Bed ${formatTime(night.sleepStartTime)} → woke `
                + `${formatTime(night.sleepEndTime)} · `
            : "";

        detail += `goal ${goals.sleepHours}h ${goalText}`;
    }

    const stages = [
        { label: "Deep", value: current.deepSleepHoursAverage ?? 0, colorClass: "bg-violet-700" },
        { label: "Core", value: current.coreSleepHoursAverage ?? 0, colorClass: "bg-violet-500" },
        { label: "REM", value: current.remSleepHoursAverage ?? 0, colorClass: "bg-violet-300" },
        { label: "Awake", value: current.awakeHoursAverage ?? 0, colorClass: "bg-slate-300" },
    ];

    const hasStages = stages.some((stage) => stage.value > 0);

    return (

        <OverviewCard
            title="Sleep"
            icon={Moon}
            iconColor="text-violet-500"
            note={note}
        >

            <p className="text-2xl font-semibold text-slate-900">
                {formatHours(current.sleepHoursAverage)}
            </p>

            <p className="text-xs text-slate-500">
                {current.sleepHoursAverage === null
                    ? "No sleep recorded"
                    : detail}
            </p>

            {hasStages && (
                <StackedBar parts={stages} label="Sleep stages" />
            )}

            <BarSeries
                values={summary.days.map((day) => day.sleepHours)}
                colorClass="bg-violet-400"
                {...dailyChartProps(
                    summary,
                    onSelectDay,
                    (day) => day.sleepHours === null
                        ? "no sleep recorded"
                        : `${formatHours(day.sleepHours)} sleep`
                )}
            />

        </OverviewCard>

    );

}

export default SleepCard;
