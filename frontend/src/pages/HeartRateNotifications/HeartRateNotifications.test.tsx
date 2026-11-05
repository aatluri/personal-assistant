import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";

import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import HeartRateNotifications from "./HeartRateNotifications";

import * as heartRateNotificationsApi from "../../api/heartRateNotifications";

import type { HeartRateNotification } from "../../types/HeartRateNotification";


afterEach(() => {
    cleanup();
});


/*
Mock the Heart Rate Notifications API.

No real backend requests are made during these tests.
*/
vi.mock("../../api/heartRateNotifications", () => ({
    getHeartRateNotificationsByDate: vi.fn(),
}));


/*
Return a notification for the tests, with overrides.
*/
function makeNotification(
    overrides: Partial<HeartRateNotification> = {},
): HeartRateNotification {

    return {
        date: "2026-10-29",
        notificationType: "Low Heart Rate",
        startTime: "08:00",
        endTime: "08:10",
        thresholdBpm: 40,
        minHeartRateBpm: 39,
        maxHeartRateBpm: 40,
        avgHeartRateBpm: 39.25,
        readings: "39, 40, 39, 39",
        ...overrides,
    };

}


beforeEach(() => {

    vi.clearAllMocks();

    /*
    By default, the selected date has no notifications.
    */
    vi.mocked(
        heartRateNotificationsApi.getHeartRateNotificationsByDate
    ).mockResolvedValue([]);

});


describe("HeartRateNotifications", () => {

    /*
    Verify the page heading, and that this read-only page
    shows no save status.
    */
    test("renders page without save status", async () => {

        render(
            <HeartRateNotifications />
        );

        expect(
            await screen.findByRole("heading", {
                level: 1,
                name: "Heart Rate Notifications",
            })
        ).toBeInTheDocument();

        expect(
            screen.queryByText("✓ Saved")
        ).not.toBeInTheDocument();

    });


    /*
    Verify that each notification's details are shown.
    */
    test("lists notifications for the selected date", async () => {

        vi.mocked(
            heartRateNotificationsApi.getHeartRateNotificationsByDate
        ).mockResolvedValue([
            makeNotification(),
            makeNotification({
                startTime: "07:18",
                endTime: "07:28",
                avgHeartRateBpm: 40,
                readings: "39, 41",
            }),
        ]);

        render(
            <HeartRateNotifications />
        );

        expect(
            await screen.findByText("08:00 – 08:10")
        ).toBeInTheDocument();

        expect(
            screen.getByText("07:18 – 07:28")
        ).toBeInTheDocument();

        expect(
            screen.getAllByText("Low Heart Rate")
        ).toHaveLength(2);

        expect(
            screen.getByText("39, 40, 39, 39")
        ).toBeInTheDocument();

        expect(
            screen.getByText("39.25 bpm")
        ).toBeInTheDocument();

    });


    /*
    Verify that missing values are shown as "-".
    */
    test("shows missing values as a dash", async () => {

        vi.mocked(
            heartRateNotificationsApi.getHeartRateNotificationsByDate
        ).mockResolvedValue([
            makeNotification({
                thresholdBpm: null,
                minHeartRateBpm: null,
                maxHeartRateBpm: null,
                avgHeartRateBpm: null,
                readings: null,
            }),
        ]);

        render(
            <HeartRateNotifications />
        );

        await screen.findByText("08:00 – 08:10");

        /*
        Threshold, Min, Max, Avg and Readings.
        */
        expect(
            screen.getAllByText("-")
        ).toHaveLength(5);

    });


    /*
    Verify the empty state.
    */
    test("shows a message when there are no notifications", async () => {

        render(
            <HeartRateNotifications />
        );

        expect(
            await screen.findByText("No notifications on this date.")
        ).toBeInTheDocument();

    });


    /*
    Verify that changing the date loads that date's
    notifications.
    */
    test("reloads when date changes", async () => {

        render(
            <HeartRateNotifications />
        );

        await screen.findByText("No notifications on this date.");

        fireEvent.change(
            screen.getByDisplayValue(/^\d{4}-\d{2}-\d{2}$/),
            {
                target: {
                    value: "2026-10-29",
                },
            }
        );

        await waitFor(() => {

            expect(
                heartRateNotificationsApi.getHeartRateNotificationsByDate
            ).toHaveBeenLastCalledWith("2026-10-29");

        });

    });


    /*
    Verify the error message when loading fails.
    */
    test("shows load error when notifications fail to load", async () => {

        vi.mocked(
            heartRateNotificationsApi.getHeartRateNotificationsByDate
        ).mockRejectedValue(
            new Error("Failed to load Heart Rate Notifications")
        );

        vi.spyOn(console, "error").mockImplementation(() => {});

        render(
            <HeartRateNotifications />
        );

        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

    });

});
