/*
PeriodControls

Chooses what the Overview shows: Day, Week or Month, and
which one, with ‹ › arrows to step through them.

Responsibilities:
- Switch between Day, Week and Month.
- Step back and forward one period.
- Show the period ("Nov 2 – 8") and how much of it has
  happened ("Week so far · 4 of 7 days").
*/

import { ChevronLeft, ChevronRight } from "lucide-react";

import type { Period } from "../../../types/DashboardSummary";


const PERIODS: { value: Period; label: string }[] = [
    { value: "day", label: "Day" },
    { value: "week", label: "Week" },
    { value: "month", label: "Month" },
];


/*
    period
        The selected period type.

    label, progress
        The period heading and its progress text; empty
        before the first load.

    canGoNext
        False for the current period: there is no data
        after today.
*/
interface PeriodControlsProps {
    period: Period;
    label: string;
    progress: string;
    canGoNext: boolean;
    onPeriodChange: (period: Period) => void;
    onPrevious: () => void;
    onNext: () => void;
}

function PeriodControls({
    period,
    label,
    progress,
    canGoNext,
    onPeriodChange,
    onPrevious,
    onNext,
}: PeriodControlsProps) {

    return (

        <div className="space-y-3">

            <div
                role="group"
                aria-label="Period"
                className="
                    inline-flex
                    gap-1
                    rounded-lg
                    bg-slate-200/70
                    p-1
                "
            >
                {PERIODS.map((option) => (

                    <button
                        key={option.value}
                        type="button"
                        aria-pressed={period === option.value}
                        onClick={() => onPeriodChange(option.value)}
                        className={`
                            rounded-md
                            px-4
                            py-1.5
                            text-sm
                            ${
                                period === option.value
                                    ? "bg-white text-slate-900 shadow-sm"
                                    : "text-slate-600 hover:text-slate-900"
                            }
                        `}
                    >
                        {option.label}
                    </button>

                ))}
            </div>

            <div
                className="
                    flex
                    flex-wrap
                    items-center
                    justify-between
                    gap-2
                "
            >

                <div className="flex items-center gap-1">

                    <button
                        type="button"
                        aria-label="Previous period"
                        onClick={onPrevious}
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            hover:bg-slate-200
                        "
                    >
                        <ChevronLeft size={20} aria-hidden="true" />
                    </button>

                    <h2
                        className="
                            min-w-28
                            text-center
                            text-lg
                            font-semibold
                            text-slate-900
                        "
                    >
                        {label}
                    </h2>

                    <button
                        type="button"
                        aria-label="Next period"
                        onClick={onNext}
                        disabled={!canGoNext}
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            hover:bg-slate-200
                            disabled:opacity-30
                            disabled:hover:bg-transparent
                        "
                    >
                        <ChevronRight size={20} aria-hidden="true" />
                    </button>

                </div>

                <p className="text-sm text-slate-500">
                    {progress}
                </p>

            </div>

        </div>

    );

}

export default PeriodControls;
