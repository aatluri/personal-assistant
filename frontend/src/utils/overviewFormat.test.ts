import {
    describe,
    expect,
    test,
} from "vitest";

import type { DashboardSummary } from "../types/DashboardSummary";

import { makeDashboardSummary } from "../test/dashboardSummary";

import {
    describeChange,
    formatComparisonLabel,
    formatDataThrough,
    formatHours,
    formatMinutes,
    formatNumber,
    formatPeriodLabel,
    formatPeriodProgress,
    shiftDate,
} from "./overviewFormat";


/*
A summary for a period, with only the dates that the
label functions read.
*/
function periodSummary(
    period: DashboardSummary["period"],
    start: string,
    end: string,
    overrides: Partial<DashboardSummary> = {},
): DashboardSummary {

    return makeDashboardSummary({
        period,
        date: start,
        start,
        end,
        ...overrides,
    });

}


describe("shiftDate", () => {

    /*
    Verify that days and weeks move across month and
    year boundaries.
    */
    test("moves by a day or a week", () => {

        expect(shiftDate("2026-11-01", "day", -1)).toBe("2026-10-31");
        expect(shiftDate("2026-12-31", "day", 1)).toBe("2027-01-01");
        expect(shiftDate("2026-11-05", "week", -1)).toBe("2026-10-29");

    });


    /*
    Verify that months keep the day where possible, and
    use the month's last day otherwise.
    */
    test("moves by a month", () => {

        expect(shiftDate("2026-11-05", "month", -1)).toBe("2026-10-05");
        expect(shiftDate("2026-01-31", "month", 1)).toBe("2026-02-28");
        expect(shiftDate("2026-03-31", "month", -1)).toBe("2026-02-28");
        expect(shiftDate("2026-12-15", "month", 1)).toBe("2027-01-15");

    });

});


describe("period text", () => {

    /*
    Verify the heading for each kind of period.
    */
    test("labels a day, a week and a month", () => {

        expect(
            formatPeriodLabel(periodSummary("day", "2026-11-05", "2026-11-05"))
        ).toBe("Thu, Nov 5");

        expect(
            formatPeriodLabel(periodSummary("week", "2026-11-02", "2026-11-08"))
        ).toBe("Nov 2 – 8");

        expect(
            formatPeriodLabel(periodSummary("week", "2026-10-26", "2026-11-01"))
        ).toBe("Oct 26 – Nov 1");

        expect(
            formatPeriodLabel(periodSummary("month", "2026-10-01", "2026-10-31"))
        ).toBe("October 2026");

    });


    /*
    Verify the progress text for current and past periods.
    */
    test("describes how much of the period has happened", () => {

        expect(formatPeriodProgress(makeDashboardSummary()))
            .toBe("Week so far · 4 of 7 days");

        expect(formatPeriodProgress(
            periodSummary("day", "2026-11-05", "2026-11-05")
        )).toBe("Today so far");

        expect(formatPeriodProgress(
            periodSummary("month", "2026-10-01", "2026-10-31", {
                isCurrent: false,
                daysInPeriod: 31,
            })
        )).toBe("Full month · 31 days");

        expect(formatPeriodProgress(
            periodSummary("day", "2026-11-03", "2026-11-03", {
                isCurrent: false,
            })
        )).toBe("Full day");

    });


    /*
    Verify the "data through" text, including no data.
    */
    test("shows how current the data is", () => {

        expect(formatDataThrough("2026-11-05"))
            .toBe("Data through Thu, Nov 5");

        expect(formatDataThrough(null)).toBe("No data yet");

    });


    /*
    Verify what each kind of period is compared with.
    */
    test("names the comparison", () => {

        expect(formatComparisonLabel(
            periodSummary("day", "2026-11-05", "2026-11-05")
        )).toBe("vs usual");

        expect(formatComparisonLabel(makeDashboardSummary()))
            .toBe("vs last week");

        const october = periodSummary("month", "2026-10-01", "2026-10-31");
        october.comparison.start = "2026-09-01";

        expect(formatComparisonLabel(october)).toBe("vs Sep");

    });

});


describe("numbers", () => {

    /*
    Verify grouping, rounding, and the dash for missing
    values.
    */
    test("formats numbers, showing a dash when missing", () => {

        expect(formatNumber(8240.4)).toBe("8,240");
        expect(formatNumber(14.25, 1)).toBe("14.3");
        expect(formatNumber(53, 1)).toBe("53");
        expect(formatNumber(null)).toBe("–");

    });


    /*
    Verify hours and minutes.
    */
    test("formats durations", () => {

        expect(formatHours(7.2)).toBe("7h 12m");
        expect(formatHours(0.5)).toBe("30m");
        expect(formatHours(null)).toBe("–");
        expect(formatMinutes(65)).toBe("1h 05m");

    });

});


describe("describeChange", () => {

    const asNumber = (difference: number) => formatNumber(difference);


    /*
    Verify the arrow and tone when higher is better.
    */
    test("an increase is good when higher is better", () => {

        expect(describeChange(9210, 8110, "vs usual", true, asNumber))
            .toEqual({ text: "↑ 1,100 vs usual", tone: "good" });

        expect(describeChange(7000, 8000, "vs usual", true, asNumber))
            .toEqual({ text: "↓ 1,000 vs usual", tone: "bad" });

    });


    /*
    Verify that a fall is good when lower is better
    (resting heart rate).
    */
    test("a decrease is good when lower is better", () => {

        expect(describeChange(53, 55, "vs last week", false, asNumber))
            .toEqual({ text: "↓ 2 vs last week", tone: "good" });

    });


    /*
    Verify that no visible change is neutral, and that
    nothing is shown when a value is missing.
    */
    test("no change is neutral, and missing values show nothing", () => {

        expect(describeChange(53.2, 53, "vs Sep", false, asNumber))
            .toEqual({ text: "±0 vs Sep", tone: "neutral" });

        expect(describeChange(null, 53, "vs Sep", false, asNumber))
            .toBeNull();

        expect(describeChange(53, null, "vs Sep", false, asNumber))
            .toBeNull();

    });

});
