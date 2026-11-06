/*
DashboardSummary

Everything the Overview page shows for one Day, Week
or Month, as returned by GET /health/dashboard/summary.

The backend computes all the values (averages over days
with data, comparisons, coverage); the page only formats
and displays them. A null value means nothing was
recorded, and is shown as a gap, never as zero.

Dates are YYYY-MM-DD. Times are full ISO date-times,
e.g. "2026-11-05T06:52:00", so the page can show both
the day and the time.
*/

export type Period = "day" | "week" | "month";


/*
Every metric for one date: one bar in the small charts.
Sleep is the night that ended on this date.
*/
export interface DailyValues {
    date: string;

    steps: number | null;
    activeEnergyKcal: number | null;
    flightsClimbed: number | null;

    sleepHours: number | null;
    deepSleepHours: number | null;
    coreSleepHours: number | null;
    remSleepHours: number | null;
    awakeHours: number | null;
    sleepStartTime: string | null;
    sleepEndTime: string | null;

    restingHeartRateBpm: number | null;
    heartRateVariabilityMs: number | null;
    bloodOxygenSaturationPercent: number | null;
    respiratoryRateBpm: number | null;

    dietaryEnergyKcal: number | null;
    proteinG: number | null;
    carbohydratesG: number | null;
    totalFatG: number | null;
    waterMl: number | null;

    workoutCount: number;
    workoutMinutes: number;
    weightKg: number | null;
}


export interface WorkoutTotals {
    count: number;
    minutes: number;
    activeEnergyKcal: number;
    distanceKm: number;
}


export interface WorkoutTypeTotals extends WorkoutTotals {
    workoutType: string;
}


/*
The combined values for one period: the selected day,
week or month, or what it is compared with.

Averages count only days with a value; the *Days and
sleepNights fields say how many days that was.
*/
export interface PeriodSummary {
    start: string;
    end: string;

    /*
    Days from the start up to today (or the end, for a
    past period).
    */
    days: number;

    stepsAverage: number | null;
    stepsTotal: number;
    activeEnergyKcalAverage: number | null;
    activeEnergyKcalTotal: number;

    sleepHoursAverage: number | null;
    deepSleepHoursAverage: number | null;
    coreSleepHoursAverage: number | null;
    remSleepHoursAverage: number | null;
    awakeHoursAverage: number | null;

    restingHeartRateBpmAverage: number | null;
    heartRateVariabilityMsAverage: number | null;
    bloodOxygenSaturationPercentAverage: number | null;
    respiratoryRateBpmAverage: number | null;

    dietaryEnergyKcalAverage: number | null;
    proteinGAverage: number | null;
    carbohydratesGAverage: number | null;
    totalFatGAverage: number | null;
    waterMlAverage: number | null;

    /*
    Null in a comparison where workout totals are not
    compared (a single day, or a period in progress).
    */
    workouts: WorkoutTotals | null;

    activityDays: number;
    sleepNights: number;
    nutritionDays: number;
    waterDays: number;
}


export interface DashboardWorkout {
    date: string;
    workoutType: string;
    workoutStartTime: string;
    workoutEndTime: string;
    workoutDurationMin: number | null;
    activeEnergyKcal: number | null;
    avgHeartRateBpm: number | null;
    distanceKm: number | null;
}


export interface DashboardNotification {
    date: string;
    notificationType: string;
    startTime: string;
    endTime: string;
    minHeartRateBpm: number | null;
    maxHeartRateBpm: number | null;
}


export interface BodySummary {
    latestWeightKg: number | null;
    latestWeightDate: string | null;
    weightDaysOld: number | null;
    weightChangeKg: number | null;
    weighIns: number;
    trend: { date: string; weightKg: number }[];

    latestBodyFatPercent: number | null;
    bodyFatChangePercent: number | null;

    latestWaistCm: number | null;
    waistChangeCm: number | null;
}


export interface Goals {
    steps: number;
    proteinG: number;
    sleepHours: number;
    waterMl: number;
}


export interface DashboardSummary {
    period: Period;
    date: string;
    start: string;
    end: string;
    daysInPeriod: number;
    daysElapsed: number;
    isCurrent: boolean;

    /*
    The latest date, up to today, that has any data.
    */
    dataThrough: string | null;

    current: PeriodSummary;

    /*
    Day: the 30 days before it ("vs usual").
    Week / Month: the previous week or month.
    */
    comparison: PeriodSummary;

    /*
    One entry per date for the small charts: the whole
    week or month, or the 7 days ending on the day.
    */
    days: DailyValues[];

    workouts: DashboardWorkout[];
    workoutTypes: WorkoutTypeTotals[];
    notifications: DashboardNotification[];
    body: BodySummary;
    goals: Goals;
}
