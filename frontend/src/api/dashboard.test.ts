import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import { getDashboardSummary } from "./dashboard";
import { API_BASE_URL } from "./config";


/*
Mock the browser's fetch() function.

No real HTTP requests are made during
these API unit tests.
*/
globalThis.fetch = vi.fn();


afterEach(() => {
    vi.clearAllMocks();
});


/*
A fetch response returning this JSON.
*/
function respondWith(body: unknown, ok = true) {

    vi.mocked(fetch).mockResolvedValue({
        ok,
        status: ok ? 200 : 500,
        json: vi.fn().mockResolvedValue(body),
    } as unknown as Response);

}


describe("Dashboard API", () => {

    /*
    Verify that only the period is sent when no date
    is given (the backend then uses today).
    */
    test("requests a period without a date", async () => {

        respondWith({});

        await getDashboardSummary("week");

        expect(fetch).toHaveBeenCalledWith(
            `${API_BASE_URL}/health/dashboard/summary?period=week`
        );

    });


    /*
    Verify that the date and refresh are sent when given.
    */
    test("requests a date and a refresh", async () => {

        respondWith({});

        await getDashboardSummary("day", "2026-11-05", true);

        expect(fetch).toHaveBeenCalledWith(
            `${API_BASE_URL}/health/dashboard/summary`
            + "?period=day&date=2026-11-05&refresh=true"
        );

    });


    /*
    Verify that the backend's snake_case keys become
    camelCase at every level, and values are kept.
    */
    test("converts nested keys to camelCase", async () => {

        respondWith({
            period: "week",
            data_through: "2026-11-05",
            current: {
                steps_average: 9210,
                protein_g_average: 118,
                workouts: { count: 4, active_energy_kcal: 2310 },
            },
            comparison: { workouts: null },
            days: [{ date: "2026-11-02", sleep_hours: 7.1 }],
            workouts: [{ workout_type: "Outdoor Run" }],
            body: { trend: [{ date: "2026-11-03", weight_kg: 78.4 }] },
            goals: { protein_g: 140 },
        });

        const summary = await getDashboardSummary("week");

        expect(summary.dataThrough).toBe("2026-11-05");
        expect(summary.current.stepsAverage).toBe(9210);
        expect(summary.current.proteinGAverage).toBe(118);
        expect(summary.current.workouts?.activeEnergyKcal).toBe(2310);
        expect(summary.comparison.workouts).toBeNull();
        expect(summary.days[0].sleepHours).toBe(7.1);
        expect(summary.workouts[0].workoutType).toBe("Outdoor Run");
        expect(summary.body.trend[0].weightKg).toBe(78.4);
        expect(summary.goals.proteinG).toBe(140);

    });


    /*
    Verify that a failed response is reported as an error.
    */
    test("throws when the request fails", async () => {

        respondWith({ detail: "error" }, false);

        await expect(
            getDashboardSummary("week")
        ).rejects.toThrow("Failed to load the Overview");

    });

});
