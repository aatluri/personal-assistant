/*
PeriodControls

Chooses what the Overview shows: Day, Week or Month, and
which one.

Responsibilities:
- Switch between Day, Week and Month.
- Step back and forward one period with ‹ ›, from the
  first period with data up to today.
- Jump straight to any date: clicking the period label
  opens the browser's date picker, and the page shows the
  day, week or month containing the picked date.
- Return to the current period with Today.
- Show the period ("Nov 2 – 8") and how much of it has
  happened ("Week so far · 4 of 7 days").
*/

import { useRef } from "react";
import { ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";

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

    selectedDate, today, dataFrom
        The selected date, today, and the earliest date
        with data (YYYY-MM-DD; dataFrom is null when there
        is none). The date picker offers only that range.

    canGoPrevious, canGoNext
        False at the first period with data, and at the
        current period (there is no data after today).

    isCurrent
        True when the period contains today; Today is
        hidden then.
*/
interface PeriodControlsProps {
    period: Period;
    label: string;
    progress: string;
    selectedDate: string;
    today: string;
    dataFrom: string | null;
    canGoPrevious: boolean;
    canGoNext: boolean;
    isCurrent: boolean;
    onPeriodChange: (period: Period) => void;
    onPrevious: () => void;
    onNext: () => void;
    onDateChange: (date: string) => void;
    onToday: () => void;
}

function PeriodControls({
    period,
    label,
    progress,
    selectedDate,
    today,
    dataFrom,
    canGoPrevious,
    canGoNext,
    isCurrent,
    onPeriodChange,
    onPrevious,
    onNext,
    onDateChange,
    onToday,
}: PeriodControlsProps) {

    const dateInput = useRef<HTMLInputElement>(null);

    /*
    Open the browser's own date picker. Browsers without
    showPicker() get the input focused and clicked instead.
    */
    function openDatePicker() {

        const input = dateInput.current;

        if (!input) {
            return;
        }

        try {
            input.showPicker();
        } catch {
            input.focus();
            input.click();
        }

    }

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
                        disabled={!canGoPrevious}
                        className="
                            rounded-md
                            p-1
                            text-slate-600
                            hover:bg-slate-200
                            disabled:opacity-30
                            disabled:hover:bg-transparent
                        "
                    >
                        <ChevronLeft size={20} aria-hidden="true" />
                    </button>

                    {/*
                        The heading's text is the period; clicking it
                        opens the date picker.
                    */}
                    <h2 className="text-lg font-semibold text-slate-900">
                        <button
                            type="button"
                            title="Choose a date"
                            onClick={openDatePicker}
                            className="
                                flex
                                min-w-28
                                items-center
                                justify-center
                                gap-1
                                rounded-md
                                px-2
                                py-0.5
                                hover:bg-slate-200
                            "
                        >
                            {label}
                            <ChevronDown
                                size={16}
                                aria-hidden="true"
                                className="text-slate-400"
                            />
                        </button>
                    </h2>

                    {/*
                        The date picker itself: hidden, and opened by
                        the heading button above. Clearing the date
                        (an empty value) changes nothing.
                    */}
                    <input
                        ref={dateInput}
                        type="date"
                        aria-label="Choose a date"
                        tabIndex={-1}
                        value={selectedDate}
                        min={dataFrom ?? undefined}
                        max={today}
                        onChange={(event) => {
                            if (event.target.value) {
                                onDateChange(event.target.value);
                            }
                        }}
                        className="sr-only"
                    />

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

                    {!isCurrent && (
                        <button
                            type="button"
                            onClick={onToday}
                            className="
                                ml-1
                                rounded-md
                                border
                                border-slate-200
                                bg-white
                                px-2
                                py-0.5
                                text-sm
                                text-slate-700
                                hover:bg-slate-100
                            "
                        >
                            Today
                        </button>
                    )}

                </div>

                <p className="text-sm text-slate-500">
                    {progress}
                </p>

            </div>

        </div>

    );

}

export default PeriodControls;
