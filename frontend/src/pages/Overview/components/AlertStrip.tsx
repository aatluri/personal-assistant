/*
AlertStrip

The period's heart rate notifications in one line, e.g.
"2 low heart rate alerts this week · lowest 39 bpm on
Tue, Nov 3 at 03:12". Shown only when there are any.

The Heart Rate Notifications page lists them in full.
*/

import { TriangleAlert } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import {
    formatCount,
    formatDay,
    formatTime,
    parseDate,
} from "../../../utils/overviewFormat";


interface AlertStripProps {
    summary: DashboardSummary;
}

function AlertStrip({ summary }: AlertStripProps) {

    const { notifications } = summary;

    if (notifications.length === 0) {
        return null;
    }

    /*
    "low heart rate alert" when every notification has
    the same type, otherwise "heart rate alert".
    */
    const types = new Set(notifications.map((n) => n.notificationType));

    const noun = types.size === 1
        ? `${[...types][0].toLowerCase()} alert`
        : "heart rate alert";

    const when = {
        day: summary.isCurrent ? "today" : "on this day",
        week: "this week",
        month: "in " + parseDate(summary.start).toLocaleDateString(
            "en-US",
            { month: "long" }
        ),
    }[summary.period];

    /*
    The lowest heart rate reached, and when.
    */
    const withMinimum = notifications.filter(
        (notification) => notification.minHeartRateBpm !== null
    );

    let lowestText = "";

    if (withMinimum.length > 0) {

        const lowest = withMinimum.reduce((low, notification) =>
            (notification.minHeartRateBpm ?? Infinity) < (low.minHeartRateBpm ?? Infinity)
                ? notification
                : low
        );

        const at = summary.period === "day"
            ? `at ${formatTime(lowest.startTime)}`
            : `on ${formatDay(lowest.date)} at ${formatTime(lowest.startTime)}`;

        lowestText = ` · lowest ${lowest.minHeartRateBpm} bpm ${at}`;
    }

    return (

        <div
            role="status"
            className="
                flex
                items-center
                gap-3
                rounded-2xl
                border
                border-amber-200
                bg-amber-50
                p-4
                text-sm
                text-amber-800
            "
        >
            <TriangleAlert size={18} aria-hidden="true" className="shrink-0" />

            <span>
                {formatCount(notifications.length, noun)} {when}
                {lowestText}
            </span>
        </div>

    );

}

export default AlertStrip;
