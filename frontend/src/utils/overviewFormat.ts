/*
Overview formatting

Date arithmetic and text formatting for the Overview
page. The backend computes the values; these helpers
only turn them into what the page shows, e.g.
"Nov 2 – 8", "7h 12m" or "↑ 14m vs last week".

Dates are YYYY-MM-DD strings, read as local dates.
*/

import type { DashboardSummary, Period } from "../types/DashboardSummary";


/* ------------------------------ */
/* Dates                          */
/* ------------------------------ */

/*
"2026-11-05" -> a local Date (not UTC, so the day never
shifts with the time zone).
*/
export function parseDate(date: string): Date {

    const [year, month, day] = date.split("-").map(Number);

    return new Date(year, month - 1, day);

}


export function toIsoDate(date: Date): string {

    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${date.getFullYear()}-${month}-${day}`;

}


/*
Moves a date one period back (-1) or forward (1): a day,
a week, or a month. Moving a month keeps the day where
possible (Jan 31 -> Feb 28).
*/
export function shiftDate(
    date: string,
    period: Period,
    direction: -1 | 1,
): string {

    const shifted = parseDate(date);

    if (period === "day") {
        shifted.setDate(shifted.getDate() + direction);
    } else if (period === "week") {
        shifted.setDate(shifted.getDate() + 7 * direction);
    } else {
        const day = shifted.getDate();

        shifted.setDate(1);
        shifted.setMonth(shifted.getMonth() + direction);

        const daysInMonth = new Date(
            shifted.getFullYear(),
            shifted.getMonth() + 1,
            0
        ).getDate();

        shifted.setDate(Math.min(day, daysInMonth));
    }

    return toIsoDate(shifted);

}


/*
"2026-11-05T06:52:00" -> "06:52"
*/
export function formatTime(dateTime: string): string {

    return dateTime.substring(11, 16);

}


/*
"2026-11-05" -> "Thu"
*/
export function formatWeekday(date: string): string {

    return parseDate(date).toLocaleDateString("en-US", {
        weekday: "short",
    });

}


/*
Axis labels for the cards' daily charts, one per day:
weekday initials ("M T W T F S S") for a day or week,
and only days 1, 8, 15, 22 and 29 for a month.
*/
export function formatChartLabels(summary: DashboardSummary): string[] {

    return summary.days.map((day) => {

        const date = parseDate(day.date);

        if (summary.period === "month") {
            return [1, 8, 15, 22, 29].includes(date.getDate())
                ? String(date.getDate())
                : "";
        }

        return "MTWTFSS"[(date.getDay() + 6) % 7];

    });

}


/*
"1 night", "4 nights"
*/
export function formatCount(count: number, noun: string): string {

    return `${count} ${noun}${count === 1 ? "" : "s"}`;

}


/*
"2026-11-05" -> "Thu, Nov 5"
*/
export function formatDay(date: string): string {

    return parseDate(date).toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
    });

}


/*
The heading for the period:
- Day:   "Thu, Nov 5"
- Week:  "Nov 2 – 8", or "Oct 26 – Nov 1" across months
- Month: "October 2026"
*/
export function formatPeriodLabel(summary: DashboardSummary): string {

    if (summary.period === "day") {
        return formatDay(summary.date);
    }

    const start = parseDate(summary.start);

    if (summary.period === "month") {
        return start.toLocaleDateString("en-US", {
            month: "long",
            year: "numeric",
        });
    }

    const end = parseDate(summary.end);

    const startText = start.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
    });

    const endText = end.getMonth() === start.getMonth()
        ? String(end.getDate())
        : end.toLocaleDateString("en-US", { month: "short", day: "numeric" });

    return `${startText} – ${endText}`;

}


/*
How much of the period has happened:
- "Today so far", "Week so far · 4 of 7 days"
- "Full day", "Full week · 7 days"
*/
export function formatPeriodProgress(summary: DashboardSummary): string {

    const name = { day: "Day", week: "Week", month: "Month" }[summary.period];

    if (summary.isCurrent) {
        return summary.period === "day"
            ? "Today so far"
            : `${name} so far · ${summary.daysElapsed} of ${summary.daysInPeriod} days`;
    }

    return summary.period === "day"
        ? "Full day"
        : `Full ${name.toLowerCase()} · ${summary.daysInPeriod} days`;

}


/*
"Data through Thu, Nov 5", because imports run behind
real time.
*/
export function formatDataThrough(dataThrough: string | null): string {

    return dataThrough === null
        ? "No data yet"
        : `Data through ${formatDay(dataThrough)}`;

}


/*
What the period is compared with: "vs usual" (the 30
days before a day), "vs last week", or "vs Sep".
*/
export function formatComparisonLabel(summary: DashboardSummary): string {

    if (summary.period === "day") {
        return "vs usual";
    }

    if (summary.period === "week") {
        return "vs last week";
    }

    return "vs " + parseDate(summary.comparison.start).toLocaleDateString(
        "en-US",
        { month: "short" }
    );

}


/* ------------------------------ */
/* Numbers                        */
/* ------------------------------ */

/*
Missing values are shown as a dash, never as 0.
*/
export const MISSING = "–";


/*
8240.4 -> "8,240"; with decimals = 1, 14.25 -> "14.3"
(trailing zeros dropped).
*/
export function formatNumber(
    value: number | null,
    decimals = 0,
): string {

    if (value === null) {
        return MISSING;
    }

    return value.toLocaleString("en-US", {
        maximumFractionDigits: decimals,
    });

}


/*
Minutes as "14m" or "1h 05m".
*/
export function formatMinutes(minutes: number): string {

    const rounded = Math.round(minutes);

    if (rounded < 60) {
        return `${rounded}m`;
    }

    const remainder = String(rounded % 60).padStart(2, "0");

    return `${Math.floor(rounded / 60)}h ${remainder}m`;

}


/*
7.2 hours -> "7h 12m".
*/
export function formatHours(hours: number | null): string {

    if (hours === null) {
        return MISSING;
    }

    return formatMinutes(hours * 60);

}


/* ------------------------------ */
/* Changes                        */
/* ------------------------------ */

/*
good / bad colour the change; neutral is used when there
is no change or no better direction.
*/
export type Tone = "good" | "bad" | "neutral";

export interface Change {
    text: string;
    tone: Tone;
}


/*
Describes how a value changed against its comparison,
e.g. "↑ 1,100 vs usual" or "↓ 3 vs last week".

formatDifference formats the size of the change.
higherIsBetter decides the tone (steps: yes; resting
heart rate: no). Returns null when either value is
missing, so nothing is shown.
*/
export function describeChange(
    current: number | null,
    comparison: number | null,
    label: string,
    higherIsBetter: boolean,
    formatDifference: (difference: number) => string,
): Change | null {

    if (current === null || comparison === null) {
        return null;
    }

    const difference = current - comparison;
    const text = formatDifference(Math.abs(difference));

    if (text === formatDifference(0)) {
        return { text: `±${text} ${label}`, tone: "neutral" };
    }

    const isUp = difference > 0;

    return {
        text: `${isUp ? "↑" : "↓"} ${text} ${label}`,
        tone: isUp === higherIsBetter ? "good" : "bad",
    };

}
