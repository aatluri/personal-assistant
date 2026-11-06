/*
RecoveryCard

Resting heart rate, HRV, blood oxygen and respiratory
rate, each compared with the usual (Day: the 30 days
before) or the previous period. A lower resting heart
rate and a higher HRV count as good; blood oxygen and
respiratory rate changes are shown without good or bad.
The chart is resting heart rate per day.
*/

import { HeartPulse } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import BarSeries from "../../../components/charts/BarSeries";

import {
    describeChange,
    formatComparisonLabel,
    formatNumber,
    MISSING,
    type Change,
} from "../../../utils/overviewFormat";

import { dailyChartProps } from "./dailyChart";
import OverviewCard from "./OverviewCard";
import { TONE_CLASSES } from "./tones";


interface RecoveryCardProps {
    summary: DashboardSummary;
    onSelectDay: (date: string) => void;
}

/*
One row: the metric, its value with unit, and its change.
*/
function RecoveryRow({
    label,
    value,
    unit,
    change,
}: {
    label: string;
    value: number | null;
    unit: string;
    change: Change | null;
}) {

    return (

        <div
            className="
                flex
                justify-between
                gap-3
                border-t
                border-slate-100
                py-1.5
                text-sm
                first:border-t-0
            "
        >
            <span className="text-slate-500">{label}</span>

            <span>
                <span className="font-medium text-slate-900">
                    {value === null ? MISSING : `${formatNumber(value, 1)}${unit}`}
                </span>

                {change && (
                    <span className={`ml-2 text-xs ${TONE_CLASSES[change.tone]}`}>
                        {change.text}
                    </span>
                )}
            </span>
        </div>

    );

}

function RecoveryCard({ summary, onSelectDay }: RecoveryCardProps) {

    const { current, comparison } = summary;
    const label = formatComparisonLabel(summary);
    const asNumber = (difference: number) => formatNumber(difference, 1);

    /*
    Blood oxygen and respiratory rate have no better
    direction, so their change is always neutral.
    */
    const neutral = (change: Change | null): Change | null =>
        change && { ...change, tone: "neutral" };

    const note = {
        day: "vs 30-day normal",
        week: "weekly average",
        month: "monthly average",
    }[summary.period];

    return (

        <OverviewCard
            title="Recovery"
            icon={HeartPulse}
            iconColor="text-orange-600"
            note={note}
        >

            <div>
                <RecoveryRow
                    label="Resting HR"
                    value={current.restingHeartRateBpmAverage}
                    unit=" bpm"
                    change={describeChange(
                        current.restingHeartRateBpmAverage,
                        comparison.restingHeartRateBpmAverage,
                        label,
                        false,
                        asNumber,
                    )}
                />

                <RecoveryRow
                    label="HRV"
                    value={current.heartRateVariabilityMsAverage}
                    unit=" ms"
                    change={describeChange(
                        current.heartRateVariabilityMsAverage,
                        comparison.heartRateVariabilityMsAverage,
                        label,
                        true,
                        asNumber,
                    )}
                />

                <RecoveryRow
                    label="Blood oxygen"
                    value={current.bloodOxygenSaturationPercentAverage}
                    unit="%"
                    change={neutral(describeChange(
                        current.bloodOxygenSaturationPercentAverage,
                        comparison.bloodOxygenSaturationPercentAverage,
                        label,
                        true,
                        asNumber,
                    ))}
                />

                <RecoveryRow
                    label="Respiratory rate"
                    value={current.respiratoryRateBpmAverage}
                    unit=" /min"
                    change={neutral(describeChange(
                        current.respiratoryRateBpmAverage,
                        comparison.respiratoryRateBpmAverage,
                        label,
                        true,
                        asNumber,
                    ))}
                />
            </div>

            <BarSeries
                values={summary.days.map((day) => day.restingHeartRateBpm)}
                colorClass="bg-orange-300"
                heightClass="h-10"
                {...dailyChartProps(
                    summary,
                    onSelectDay,
                    (day) => day.restingHeartRateBpm === null
                        ? "no resting heart rate"
                        : `resting heart rate ${formatNumber(day.restingHeartRateBpm)} bpm`
                )}
            />

        </OverviewCard>

    );

}

export default RecoveryCard;
