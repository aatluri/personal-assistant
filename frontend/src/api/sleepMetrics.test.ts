import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getSleepMetric,
    saveSleepMetric,
} from "./sleepMetrics";

import {
    createEmptySleepMetrics,
} from "../utils/createEmptySleepMetrics";


/*
Mock the browser's fetch() function.

No real HTTP requests are made during
these API unit tests.
*/
globalThis.fetch = vi.fn();


/*
Clean up mock call history after each test.
*/
afterEach(() => {

    vi.clearAllMocks();

});


/*
Configure the default fetch response.

Individual tests can override this response
when required.
*/
beforeEach(() => {

    vi.mocked(fetch).mockResolvedValue({

        ok: true,

        status: 200,

        json: vi.fn().mockResolvedValue({}),

        text: vi.fn(),

    } as unknown as Response);

});


describe("Sleep Metrics API", () => {

    /*
    Verify that Sleep Metrics are correctly
    retrieved and converted from the backend
    snake_case model into the frontend model.
    */
    test("returns Sleep Metrics", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                date: "2026-08-27",

                sleep_start_time:
                    "2026-08-26T23:15:00",

                sleep_end_time:
                    "2026-08-27T07:15:00",

                total_sleep_duration_hr: 8,

                core_sleep_hr: 4.5,
                rem_sleep_hr: 1.5,
                deep_sleep_hr: 1.5,
                awake_hr: 0.5,

                source: "Apple Health",

            }),

        } as unknown as Response);


        const sleepMetrics =
            await getSleepMetric(
                "2026-08-27"
            );


        expect(sleepMetrics).toEqual({

            date: "2026-08-27",

            sleepStartTime:
                "2026-08-26T23:15:00",

            sleepEndTime:
                "2026-08-27T07:15:00",

            totalSleepDurationHr: 8,

            coreSleepHr: 4.5,
            remSleepHr: 1.5,
            deepSleepHr: 1.5,
            awakeHr: 0.5,

            source: "Apple Health",

        });


        /*
        Verify that the selected date is
        included in the GET endpoint.
        */
        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/sleep-metrics/2026-08-27"

        );

    });


    /*
    Verify that null is returned when no
    Sleep Metrics record exists for the date.
    */
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);


        const sleepMetrics =
            await getSleepMetric(
                "2026-08-27"
            );


        expect(sleepMetrics).toBeNull();

    });


    /*
    Verify that an unexpected backend error
    causes the API function to throw.
    */
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);


        await expect(

            getSleepMetric(
                "2026-08-27"
            )

        ).rejects.toThrow(

            "Failed to load Sleep Metrics"

        );

    });


    /*
    Verify that saveSleepMetric converts the
    frontend model into the correct backend
    request model.
    */
    test("sends correct Sleep Metrics request", async () => {

        const sleepMetrics =
            createEmptySleepMetrics();


        sleepMetrics.sleepStartTime =
            "2026-08-26T23:15:00";

        sleepMetrics.sleepEndTime =
            "2026-08-27T07:15:00";

        sleepMetrics.totalSleepDurationHr = 8;

        sleepMetrics.coreSleepHr = 4.5;
        sleepMetrics.remSleepHr = 1.5;
        sleepMetrics.deepSleepHr = 1.5;
        sleepMetrics.awakeHr = 0.5;

        sleepMetrics.source = "Apple Health";


        await saveSleepMetric(
            "2026-08-27",
            sleepMetrics
        );


        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/sleep-metrics",

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    sleep_start_time:
                        "2026-08-26T23:15:00",

                    sleep_end_time:
                        "2026-08-27T07:15:00",

                    total_sleep_duration_hr: 8,

                    core_sleep_hr: 4.5,
                    rem_sleep_hr: 1.5,
                    deep_sleep_hr: 1.5,
                    awake_hr: 0.5,

                    source: "Apple Health",

                }),
            }
        );

    });


    /*
    Verify that empty numeric, datetime,
    and source values are converted to null
    before being sent to the backend.
    */
    test("converts empty Sleep Metrics values to null", async () => {

        const sleepMetrics =
            createEmptySleepMetrics();


        await saveSleepMetric(
            "2026-08-27",
            sleepMetrics
        );


        expect(fetch).toHaveBeenCalledTimes(1);


        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];


        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );


        expect(
            requestBody.sleep_start_time
        ).toBeNull();

        expect(
            requestBody.sleep_end_time
        ).toBeNull();


        expect(
            requestBody.total_sleep_duration_hr
        ).toBeNull();

        expect(
            requestBody.core_sleep_hr
        ).toBeNull();

        expect(
            requestBody.rem_sleep_hr
        ).toBeNull();

        expect(
            requestBody.deep_sleep_hr
        ).toBeNull();

        expect(
            requestBody.awake_hr
        ).toBeNull();


        expect(
            requestBody.source
        ).toBeNull();

    });


    /*
    Verify that an error is thrown when
    saving Sleep Metrics fails.
    */
    test("throws on Sleep Metrics save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);


        const sleepMetrics =
            createEmptySleepMetrics();


        await expect(

            saveSleepMetric(
                "2026-08-27",
                sleepMetrics
            )

        ).rejects.toThrow(

            "Failed to save Sleep Metrics"

        );

    });

});