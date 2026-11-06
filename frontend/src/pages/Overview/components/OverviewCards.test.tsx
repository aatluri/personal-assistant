import {
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import {
    describe,
    expect,
    test,
    vi,
} from "vitest";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import {
    makeDailyValues,
    makeDashboardSummary,
    makePeriodSummary,
    makeWeekDays,
} from "../../../test/dashboardSummary";

import ActivityCard from "./ActivityCard";
import AlertStrip from "./AlertStrip";
import BodyCard from "./BodyCard";
import NutritionCard from "./NutritionCard";
import RecoveryCard from "./RecoveryCard";
import SleepCard from "./SleepCard";
import TrainingCard from "./TrainingCard";


/*
Overview Card Tests

Each card is rendered on its own with a sample summary
(see src/test/dashboardSummary.ts): by default the week
of Nov 2 – 8, 2026, in progress (4 of 7 days).
*/


/*
Today, Thu Nov 5, in Day view: the 7 chart days end on it.
*/
function daySummary(overrides: Partial<DashboardSummary> = {}): DashboardSummary {

    return makeDashboardSummary({
        period: "day",
        date: "2026-11-05",
        start: "2026-11-05",
        end: "2026-11-05",
        daysInPeriod: 1,
        daysElapsed: 1,
        days: [
            makeDailyValues({ date: "2026-10-30" }),
            makeDailyValues({ date: "2026-10-31" }),
            makeDailyValues({ date: "2026-11-01" }),
            makeDailyValues({ date: "2026-11-02" }),
            makeDailyValues({ date: "2026-11-03" }),
            makeDailyValues({ date: "2026-11-04" }),
            makeDailyValues({
                date: "2026-11-05",
                steps: 8240,
                flightsClimbed: 9,
                sleepHours: 7.2,
                sleepStartTime: "2026-11-04T23:40:00",
                sleepEndTime: "2026-11-05T06:52:00",
            }),
        ],
        ...overrides,
    });

}


const noSelect = () => {};


describe("SleepCard", () => {

    /*
    Verify Day view: last night's duration, bed and wake
    times, and the goal.
    */
    test("shows last night in Day view", () => {

        render(
            <SleepCard
                summary={daySummary({
                    current: makePeriodSummary({
                        sleepHoursAverage: 7.2,
                        deepSleepHoursAverage: 1.2,
                        coreSleepHoursAverage: 4,
                    }),
                })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("last night")).toBeInTheDocument();
        expect(screen.getByText("7h 12m")).toBeInTheDocument();
        expect(
            screen.getByText("Bed 23:40 → woke 06:52 · goal 7h met")
        ).toBeInTheDocument();
        expect(screen.getByText(/Deep 23%/)).toBeInTheDocument();

    });


    /*
    Verify Week view: the average per night, and no data
    shown as such.
    */
    test("shows the average per night, or that nothing was recorded", () => {

        const { rerender } = render(
            <SleepCard
                summary={makeDashboardSummary({
                    current: makePeriodSummary({ sleepHoursAverage: 7.18, sleepNights: 4 }),
                })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("avg per night · 4 nights")).toBeInTheDocument();

        rerender(
            <SleepCard
                summary={makeDashboardSummary({ current: makePeriodSummary() })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("No sleep recorded")).toBeInTheDocument();

    });


    /*
    Verify that tapping a night in Week view opens that day.
    */
    test("opens a day when its bar is tapped", () => {

        const onSelectDay = vi.fn();

        render(
            <SleepCard
                summary={makeDashboardSummary({
                    days: makeWeekDays({ "2026-11-03": { sleepHours: 7.8 } }),
                })}
                onSelectDay={onSelectDay}
            />
        );

        fireEvent.click(
            screen.getByRole("button", { name: "Tue, Nov 3: 7h 48m sleep" })
        );

        expect(onSelectDay).toHaveBeenCalledWith("2026-11-03");

    });

});


describe("RecoveryCard", () => {

    /*
    Verify each metric's value and change: lower resting
    heart rate and higher HRV are good; blood oxygen and
    respiratory rate are neutral.
    */
    test("shows each metric with its change", () => {

        render(
            <RecoveryCard
                summary={makeDashboardSummary({
                    current: makePeriodSummary({
                        restingHeartRateBpmAverage: 53,
                        heartRateVariabilityMsAverage: 61,
                        bloodOxygenSaturationPercentAverage: 97,
                        respiratoryRateBpmAverage: 14.2,
                    }),
                    comparison: makePeriodSummary({
                        start: "2026-10-26",
                        restingHeartRateBpmAverage: 55,
                        heartRateVariabilityMsAverage: 53,
                        bloodOxygenSaturationPercentAverage: 96,
                        respiratoryRateBpmAverage: 14.2,
                    }),
                })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("weekly average")).toBeInTheDocument();

        expect(screen.getByText("53 bpm")).toBeInTheDocument();
        expect(screen.getByText("↓ 2 vs last week").className).toContain("text-green-700");

        expect(screen.getByText("61 ms")).toBeInTheDocument();
        expect(screen.getByText("↑ 8 vs last week").className).toContain("text-green-700");

        expect(screen.getByText("↑ 1 vs last week").className).toContain("text-slate-500");
        expect(screen.getByText("±0 vs last week")).toBeInTheDocument();

    });

});


describe("ActivityCard", () => {

    /*
    Verify Day view: the day's steps, active energy and
    flights, with the selected day highlighted.
    */
    test("shows the day's activity in Day view", () => {

        render(
            <ActivityCard
                summary={daySummary({
                    current: makePeriodSummary({
                        stepsAverage: 8240,
                        activeEnergyKcalAverage: 540,
                        activityDays: 1,
                        days: 1,
                    }),
                })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("today")).toBeInTheDocument();
        expect(screen.getByText("540 active kcal · 9 flights")).toBeInTheDocument();

        /*
        Day view: no bar can be tapped.
        */
        expect(screen.queryAllByRole("button")).toHaveLength(0);

    });


    /*
    Verify Week view: the total, the average active energy,
    and how many days had steps.
    */
    test("shows totals and coverage in Week view", () => {

        render(
            <ActivityCard
                summary={makeDashboardSummary({
                    current: makePeriodSummary({
                        stepsAverage: 9210,
                        stepsTotal: 27630,
                        activeEnergyKcalAverage: 520,
                        activityDays: 3,
                        days: 4,
                    }),
                })}
                onSelectDay={noSelect}
            />
        );

        expect(screen.getByText("avg per day")).toBeInTheDocument();
        expect(screen.getByText("27,630 total · 520 active kcal/day")).toBeInTheDocument();
        expect(screen.getByText("Recorded on 3 of 4 days")).toBeInTheDocument();

    });

});


describe("NutritionCard", () => {

    /*
    Verify protein and water against their goals, and
    logging coverage for a week in progress.
    */
    test("shows goals and coverage", () => {

        render(
            <NutritionCard
                summary={makeDashboardSummary({
                    current: makePeriodSummary({
                        dietaryEnergyKcalAverage: 2180,
                        proteinGAverage: 118,
                        carbohydratesGAverage: 250,
                        totalFatGAverage: 70,
                        waterMlAverage: 2600,
                        nutritionDays: 3,
                        days: 4,
                    }),
                })}
            />
        );

        expect(screen.getByText("avg per logged day")).toBeInTheDocument();
        expect(screen.getByText("2,180")).toBeInTheDocument();
        expect(screen.getByText("118 g / 140 g")).toBeInTheDocument();
        expect(screen.getByText("2.6 L / 3 L")).toBeInTheDocument();
        expect(screen.getByText("Logged 3 of 4 days so far")).toBeInTheDocument();
        expect(screen.getByText(/Fat 30%/)).toBeInTheDocument();

    });


    /*
    Verify a day with nothing logged.
    */
    test("shows when nothing was logged", () => {

        render(<NutritionCard summary={daySummary()} />);

        expect(screen.getByText("Nothing logged")).toBeInTheDocument();
        expect(screen.getByText("– / 140 g")).toBeInTheDocument();

    });

});


describe("TrainingCard", () => {

    const workout = {
        date: "2026-11-03",
        workoutType: "Outdoor Run",
        workoutStartTime: "2026-11-03T17:05:00",
        workoutEndTime: "2026-11-03T17:39:00",
        workoutDurationMin: 34,
        activeEnergyKcal: 421,
        avgHeartRateBpm: 148,
        distanceKm: 6.2,
    };


    /*
    Verify Week view: each session with its day.
    */
    test("lists sessions in Week view", () => {

        render(
            <TrainingCard
                summary={makeDashboardSummary({ workouts: [workout] })}
            />
        );

        expect(screen.getByText("4 sessions")).toBeInTheDocument();
        expect(screen.getByText("Outdoor Run")).toBeInTheDocument();
        expect(screen.getByText("Tue · 34 min · 6.2 km")).toBeInTheDocument();
        expect(screen.getByText("421 kcal · 148 bpm")).toBeInTheDocument();

    });


    /*
    Verify Month view: totals per workout type.
    */
    test("totals workout types in Month view", () => {

        render(
            <TrainingCard
                summary={makeDashboardSummary({
                    period: "month",
                    workoutTypes: [{
                        workoutType: "Strength",
                        count: 10,
                        minutes: 550,
                        activeEnergyKcal: 5620,
                        distanceKm: 0,
                    }],
                })}
            />
        );

        expect(screen.getByText("10 sessions · 9h 10m")).toBeInTheDocument();
        expect(screen.getByText("5,620 kcal")).toBeInTheDocument();

    });


    /*
    Verify a period with no workouts.
    */
    test("says when there are no workouts", () => {

        render(
            <TrainingCard
                summary={makeDashboardSummary({ current: makePeriodSummary() })}
            />
        );

        expect(screen.getByText("No workouts")).toBeInTheDocument();
        expect(screen.getByText("0 sessions")).toBeInTheDocument();

    });

});


describe("BodyCard", () => {

    const body = {
        latestWeightKg: 78.4,
        latestWeightDate: "2026-11-03",
        weightDaysOld: 2,
        weightChangeKg: -0.6,
        weighIns: 2,
        trend: [
            { date: "2026-11-02", weightKg: 79 },
            { date: "2026-11-03", weightKg: 78.4 },
        ],
        latestBodyFatPercent: 18.6,
        bodyFatChangePercent: -0.3,
        latestWaistCm: 84,
        waistChangeCm: 0,
    };


    /*
    Verify Day view: the latest weight and how old it is,
    without changes.
    */
    test("shows the latest weight and its age in Day view", () => {

        render(<BodyCard summary={daySummary({ body })} />);

        expect(screen.getByText("78.4")).toBeInTheDocument();
        expect(screen.getByText("Weighed 2 days ago")).toBeInTheDocument();
        expect(screen.queryByText("↓ 0.6 kg")).not.toBeInTheDocument();
        expect(screen.getByRole("img", { name: "Weight trend" })).toBeInTheDocument();

    });


    /*
    Verify Week view: the changes over the week.
    */
    test("shows changes in Week view", () => {

        render(<BodyCard summary={makeDashboardSummary({ body })} />);

        expect(screen.getByText("↓ 0.6 kg")).toBeInTheDocument();
        expect(screen.getByText("2 weigh-ins this week")).toBeInTheDocument();
        expect(screen.getByText("(↓ 0.3)")).toBeInTheDocument();
        expect(screen.getByText("(±0 cm)")).toBeInTheDocument();

    });

});


describe("AlertStrip", () => {

    const notification = (date: string, time: string, minimum: number) => ({
        date,
        notificationType: "Low Heart Rate",
        startTime: `${date}T${time}:00`,
        endTime: `${date}T${time}:00`,
        minHeartRateBpm: minimum,
        maxHeartRateBpm: 42,
    });


    /*
    Verify that nothing is shown without notifications.
    */
    test("is hidden when there are no notifications", () => {

        const { container } = render(
            <AlertStrip summary={makeDashboardSummary()} />
        );

        expect(container).toBeEmptyDOMElement();

    });


    /*
    Verify the count, the type, and the lowest heart rate
    with when it happened.
    */
    test("summarises the notifications", () => {

        render(
            <AlertStrip
                summary={makeDashboardSummary({
                    notifications: [
                        notification("2026-11-02", "02:10", 41),
                        notification("2026-11-03", "03:12", 39),
                    ],
                })}
            />
        );

        expect(screen.getByRole("status")).toHaveTextContent(
            "2 low heart rate alerts this week · lowest 39 bpm on Tue, Nov 3 at 03:12"
        );

    });

});
