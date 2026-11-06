/*
Dashboard API

Communication layer between the Overview page and the
backend. The Overview is read-only, so this module only
loads the summary.
*/

import type { DashboardSummary, Period } from "../types/DashboardSummary";
import { API_BASE_URL } from "./config";


/*
"protein_g_average" -> "proteinGAverage"
*/
function toCamelCase(key: string): string {

    return key.replace(
        /_([a-z])/g,
        (_, letter: string) => letter.toUpperCase()
    );

}


/*
Converts every key in a JSON value from the backend's
snake_case to the frontend's camelCase, including nested
objects and lists.

The other API modules map each field by hand. The summary
has around a hundred nested fields that keep their names
apart from the casing, so they are converted in one place.
*/
function camelCaseKeys(value: unknown): unknown {

    if (Array.isArray(value)) {
        return value.map(camelCaseKeys);
    }

    if (value !== null && typeof value === "object") {
        return Object.fromEntries(
            Object.entries(value).map(
                ([key, nested]) => [toCamelCase(key), camelCaseKeys(nested)]
            )
        );
    }

    return value;

}


/*
Retrieves the Overview for the day, week or month that
contains date (YYYY-MM-DD; the backend uses today when
it is left out).

refresh asks the backend to read every worksheet again
first, instead of using its cache (the Refresh button).
*/
export async function getDashboardSummary(
    period: Period,
    date?: string,
    refresh = false,
): Promise<DashboardSummary> {

    const query = new URLSearchParams({ period });

    if (date) {
        query.set("date", date);
    }

    if (refresh) {
        query.set("refresh", "true");
    }

    const response = await fetch(
        `${API_BASE_URL}/health/dashboard/summary?${query}`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load the Overview"
        );
    }

    return camelCaseKeys(
        await response.json()
    ) as DashboardSummary;

}
