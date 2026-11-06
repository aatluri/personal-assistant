/*
TrainingCard

The period's workouts.

- Day / Week: each session (type, when, how long, how
  far), with its active energy and average heart rate.
- Month: totals per workout type, most frequent first.
*/

import { Dumbbell } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import {
    formatCount,
    formatMinutes,
    formatNumber,
    formatTime,
    formatWeekday,
} from "../../../utils/overviewFormat";

import OverviewCard from "./OverviewCard";


interface TrainingCardProps {
    summary: DashboardSummary;
}

/*
One row: what, the details below it, and the energy on
the right.
*/
function TrainingRow({
    title,
    details,
    energy,
}: {
    title: string;
    details: string;
    energy: string;
}) {

    return (

        <li
            className="
                flex
                justify-between
                gap-3
                border-t
                border-slate-100
                py-1.5
                first:border-t-0
            "
        >
            <div className="min-w-0">
                <p className="text-sm text-slate-900">{title}</p>
                <p className="text-xs text-slate-500">{details}</p>
            </div>

            <p className="self-center text-right text-xs text-slate-500">
                {energy}
            </p>
        </li>

    );

}

/*
" · 6.2 km" when the workout has a distance.
*/
function distanceText(distanceKm: number | null): string {

    return distanceKm ? ` · ${formatNumber(distanceKm, 1)} km` : "";

}

function TrainingCard({ summary }: TrainingCardProps) {

    const count = summary.current.workouts?.count ?? 0;

    let rows;

    if (summary.period === "month") {

        rows = summary.workoutTypes.map((type) => (
            <TrainingRow
                key={type.workoutType}
                title={type.workoutType}
                details={
                    `${formatCount(type.count, "session")} · `
                    + formatMinutes(type.minutes)
                    + distanceText(type.distanceKm)
                }
                energy={`${formatNumber(type.activeEnergyKcal)} kcal`}
            />
        ));

    } else {

        rows = summary.workouts.map((workout) => {

            /*
            Day view says when (time); Week view says which day.
            */
            const when = summary.period === "day"
                ? formatTime(workout.workoutStartTime)
                : formatWeekday(workout.date);

            const heartRate = workout.avgHeartRateBpm === null
                ? ""
                : ` · ${formatNumber(workout.avgHeartRateBpm)} bpm`;

            return (
                <TrainingRow
                    key={workout.workoutStartTime}
                    title={workout.workoutType}
                    details={
                        `${when} · ${formatNumber(workout.workoutDurationMin)} min`
                        + distanceText(workout.distanceKm)
                    }
                    energy={`${formatNumber(workout.activeEnergyKcal)} kcal${heartRate}`}
                />
            );

        });

    }

    return (

        <OverviewCard
            title="Training"
            icon={Dumbbell}
            iconColor="text-teal-600"
            note={formatCount(count, "session")}
        >

            {count === 0 ? (
                <p className="text-sm text-slate-500">No workouts</p>
            ) : (
                <ul>{rows}</ul>
            )}

        </OverviewCard>

    );

}

export default TrainingCard;
