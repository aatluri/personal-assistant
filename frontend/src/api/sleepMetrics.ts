/*
Sleep Metrics API

Acts as the communication layer between the
Sleep Metrics frontend and backend.

Responsibilities:
- Retrieve Sleep Metrics from the backend.
- Convert backend models into frontend models.
- Convert frontend models into backend request models.
- Save Sleep Metrics to the backend.
*/

import type { SleepMetrics } from "../types/SleepMetrics";


/*
Converts an empty numeric field into null
before sending it to the backend.
*/
function buildNumber(
    value: number | ""
): number | null {

    return value === "" ? null : value;

}


/*
Retrieves Sleep Metrics for the specified date.

Returns null if no Sleep Metrics record
exists for the selected date.
*/
export async function getSleepMetric(
    date: string,
): Promise<SleepMetrics | null> {

    const response = await fetch(
        `http://localhost:8000/health/sleep-metrics/${date}`
    );

    /*
    No Sleep Metrics record exists
    for this date.
    */
    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error(
            "Failed to load Sleep Metrics"
        );
    }

    const apiResponse = await response.json();

    /*
    Convert the backend API model into
    the frontend SleepMetrics model.
    */
    const sleepMetrics: SleepMetrics = {

        date: apiResponse.date,

        sleepStartTime:
            apiResponse.sleep_start_time ?? "",

        sleepEndTime:
            apiResponse.sleep_end_time ?? "",

        totalSleepDurationHr:
            apiResponse.total_sleep_duration_hr ?? "",

        coreSleepHr:
            apiResponse.core_sleep_hr ?? "",

        deepSleepHr:
            apiResponse.deep_sleep_hr ?? "",

        awakeHr:
            apiResponse.awake_hr ?? "",

        remSleepHr:
            apiResponse.rem_sleep_hr ?? "",

        source:
            apiResponse.source ?? "",

    };

    return sleepMetrics;

}


/*
Saves Sleep Metrics.

The backend performs an upsert using
the date as the unique key.
*/
export async function saveSleepMetric(
    selectedDate: string,
    sleepMetrics: SleepMetrics,
): Promise<void> {

    /*
    Convert the frontend model into
    the format expected by the backend.
    */
    const request = {

        date: selectedDate,

        sleep_start_time:
            sleepMetrics.sleepStartTime || null,

        sleep_end_time:
            sleepMetrics.sleepEndTime || null,

        total_sleep_duration_hr:
            buildNumber(
                sleepMetrics.totalSleepDurationHr
            ),

        core_sleep_hr:
            buildNumber(
                sleepMetrics.coreSleepHr
            ),

        rem_sleep_hr:
            buildNumber(
                sleepMetrics.remSleepHr
            ),

        deep_sleep_hr:
            buildNumber(
                sleepMetrics.deepSleepHr
            ),

        awake_hr:
            buildNumber(
                sleepMetrics.awakeHr
            ),

        source:
            sleepMetrics.source || null,

    };

    const response = await fetch(
        "http://localhost:8000/health/sleep-metrics",
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        }
    );

    if (!response.ok) {

        const error = await response.text();

        console.error(error);

        throw new Error(
            "Failed to save Sleep Metrics"
        );

    }

}