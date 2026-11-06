/*
Sample Overview data for tests.

A week in progress: Thursday, November 5, 2026, in the
week of Monday, November 2 to Sunday, November 8,
compared with the previous week. Tests override what
they need.
*/

import type {
    DailyValues,
    DashboardSummary,
    PeriodSummary,
} from "../types/DashboardSummary";


/*
One day with no data, for the cards' charts.
*/
export function makeDailyValues(
    overrides: Partial<DailyValues> = {},
): DailyValues {

    return {
        date: "2026-11-02",
        steps: null,
        activeEnergyKcal: null,
        flightsClimbed: null,
        sleepHours: null,
        deepSleepHours: null,
        coreSleepHours: null,
        remSleepHours: null,
        awakeHours: null,
        sleepStartTime: null,
        sleepEndTime: null,
        restingHeartRateBpm: null,
        heartRateVariabilityMs: null,
        bloodOxygenSaturationPercent: null,
        respiratoryRateBpm: null,
        dietaryEnergyKcal: null,
        proteinG: null,
        carbohydratesG: null,
        totalFatG: null,
        waterMl: null,
        workoutCount: 0,
        workoutMinutes: 0,
        weightKg: null,
        ...overrides,
    };

}


/*
The 7 days of the sample week (Mon Nov 2 to Sun Nov 8),
with the given values; days not listed have no data.
*/
export function makeWeekDays(
    values: Record<string, Partial<DailyValues>> = {},
): DailyValues[] {

    return [2, 3, 4, 5, 6, 7, 8].map((day) => {
        const date = `2026-11-0${day}`;
        return makeDailyValues({ date, ...values[date] });
    });

}


/*
A period with no data at all.
*/
export function makePeriodSummary(
    overrides: Partial<PeriodSummary> = {},
): PeriodSummary {

    return {
        start: "2026-11-02",
        end: "2026-11-08",
        days: 4,
        stepsAverage: null,
        stepsTotal: 0,
        activeEnergyKcalAverage: null,
        activeEnergyKcalTotal: 0,
        sleepHoursAverage: null,
        deepSleepHoursAverage: null,
        coreSleepHoursAverage: null,
        remSleepHoursAverage: null,
        awakeHoursAverage: null,
        restingHeartRateBpmAverage: null,
        heartRateVariabilityMsAverage: null,
        bloodOxygenSaturationPercentAverage: null,
        respiratoryRateBpmAverage: null,
        dietaryEnergyKcalAverage: null,
        proteinGAverage: null,
        carbohydratesGAverage: null,
        totalFatGAverage: null,
        waterMlAverage: null,
        workouts: { count: 0, minutes: 0, activeEnergyKcal: 0, distanceKm: 0 },
        activityDays: 0,
        sleepNights: 0,
        nutritionDays: 0,
        waterDays: 0,
        ...overrides,
    };

}


export function makeDashboardSummary(
    overrides: Partial<DashboardSummary> = {},
): DashboardSummary {

    return {
        period: "week",
        date: "2026-11-05",
        start: "2026-11-02",
        end: "2026-11-08",
        daysInPeriod: 7,
        daysElapsed: 4,
        isCurrent: true,
        dataFrom: "2022-01-01",
        dataThrough: "2026-11-05",
        highlights: [],

        current: makePeriodSummary({
            stepsAverage: 9210,
            stepsTotal: 36840,
            sleepHoursAverage: 7.18,
            restingHeartRateBpmAverage: 53,
            workouts: {
                count: 4,
                minutes: 210,
                activeEnergyKcal: 2310,
                distanceKm: 6.2,
            },
        }),

        comparison: makePeriodSummary({
            start: "2026-10-26",
            end: "2026-11-01",
            days: 7,
            stepsAverage: 8689,
            sleepHoursAverage: 6.81,
            restingHeartRateBpmAverage: 55,
            workouts: null,
        }),

        days: [],
        workouts: [],
        workoutTypes: [],
        notifications: [],

        body: {
            latestWeightKg: null,
            latestWeightDate: null,
            weightDaysOld: null,
            weightChangeKg: null,
            weighIns: 0,
            trend: [],
            latestBodyFatPercent: null,
            bodyFatChangePercent: null,
            latestWaistCm: null,
            waistChangeCm: null,
        },

        goals: {
            steps: 10000,
            proteinG: 140,
            sleepHours: 7,
            waterMl: 3000,
        },

        ...overrides,
    };

}
