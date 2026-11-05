import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getHeartRateNotificationsByDate,
} from "./heartRateNotifications";


/*
Mock the browser's fetch() function.

No real HTTP requests are made during
these API unit tests.
*/
globalThis.fetch = vi.fn();


afterEach(() => {
    vi.clearAllMocks();
});


describe("Heart Rate Notifications API", () => {

    /*
    Verify that notifications are requested for the date
    and converted from the backend snake_case model into
    the frontend model, with times as HH:mm.
    */
    test("returns notifications for a date", async () => {

        vi.mocked(fetch).mockResolvedValue({
            ok: true,
            status: 200,
            json: vi.fn().mockResolvedValue([
                {
                    date: "2026-10-29",
                    notification_type: "Low Heart Rate",
                    start_time: "2026-10-29T08:00:08",
                    end_time: "2026-10-29T08:10:08",
                    threshold_bpm: 40,
                    min_heart_rate_bpm: 39,
                    max_heart_rate_bpm: 40,
                    avg_heart_rate_bpm: 39.25,
                    readings: "39, 40, 39, 39",
                    source: "Health Auto Export",
                },
            ]),
        } as unknown as Response);


        const notifications =
            await getHeartRateNotificationsByDate(
                "2026-10-29"
            );


        expect(notifications).toEqual([
            {
                date: "2026-10-29",
                notificationType: "Low Heart Rate",
                startTime: "08:00",
                endTime: "08:10",
                thresholdBpm: 40,
                minHeartRateBpm: 39,
                maxHeartRateBpm: 40,
                avgHeartRateBpm: 39.25,
                readings: "39, 40, 39, 39",
            },
        ]);

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/health/heart-rate-notifications?notification_date=2026-10-29"
        );

    });


    /*
    Verify that missing values become null.
    */
    test("converts missing values to null", async () => {

        vi.mocked(fetch).mockResolvedValue({
            ok: true,
            status: 200,
            json: vi.fn().mockResolvedValue([
                {
                    date: "2026-10-29",
                    notification_type: "Low Heart Rate",
                    start_time: "2026-10-29T08:00:08",
                    end_time: "2026-10-29T08:10:08",
                    threshold_bpm: null,
                    min_heart_rate_bpm: null,
                    max_heart_rate_bpm: null,
                    avg_heart_rate_bpm: null,
                    readings: null,
                },
            ]),
        } as unknown as Response);


        const [notification] =
            await getHeartRateNotificationsByDate(
                "2026-10-29"
            );


        expect(notification.thresholdBpm).toBeNull();
        expect(notification.minHeartRateBpm).toBeNull();
        expect(notification.maxHeartRateBpm).toBeNull();
        expect(notification.avgHeartRateBpm).toBeNull();
        expect(notification.readings).toBeNull();

    });


    /*
    Verify that an error is thrown when loading fails.
    */
    test("throws when loading fails", async () => {

        vi.mocked(fetch).mockResolvedValue({
            ok: false,
            status: 500,
            json: vi.fn(),
        } as unknown as Response);


        await expect(
            getHeartRateNotificationsByDate("2026-10-29")
        ).rejects.toThrow(
            "Failed to load Heart Rate Notifications"
        );

    });

});
