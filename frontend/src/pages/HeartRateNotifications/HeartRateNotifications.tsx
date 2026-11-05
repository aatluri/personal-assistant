/*
HeartRateNotifications

Read-only page listing the heart rate notifications
(e.g. low heart rate alerts) for a selected date.

The notifications come from the watch through the data
importer, so there is nothing to enter or save here.

Responsibilities:
- Load the notifications for the selected date.
- Display each notification's time, type, threshold,
  heart rate statistics and readings.
*/

import { useEffect, useState } from "react";
import { BellRing } from "lucide-react";

import { getHeartRateNotificationsByDate } from "../../api/heartRateNotifications";

import type { HeartRateNotification } from "../../types/HeartRateNotification";

import LoadingSpinner from "../../components/LoadingSpinner";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";
import PageHeader from "../../components/PageHeader";
import DateSection from "../../components/DateSection";


/*
Shows a value with its unit, or "-" when it is missing.
*/
function formatBpm(value: number | null): string {

    return value === null ? "-" : `${value} bpm`;

}


function HeartRateNotifications() {

    /*
    Today's date in YYYY-MM-DD format.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Currently selected date.

    Changing this value automatically reloads
    the notifications for that date.
    */
    const [selectedDate, setSelectedDate] =
        useState(today);

    const [notifications, setNotifications] =
        useState<HeartRateNotification[]>([]);

    const [isLoading, setIsLoading] =
        useState(true);

    const [loadError, setLoadError] =
        useState(false);


    /*
    Whenever the selected date changes,
    retrieve its notifications from the backend.
    */
    useEffect(() => {

        async function loadNotifications() {

            setIsLoading(true);
            setLoadError(false);

            try {

                setNotifications(
                    await getHeartRateNotificationsByDate(selectedDate)
                );

            } catch (error) {

                console.error(
                    "Failed to load Heart Rate Notifications:",
                    error
                );
                setNotifications([]);
                setLoadError(true);

            } finally {

                setIsLoading(false);

            }

        }

        loadNotifications();

    }, [selectedDate]);


    /*
    Display a loading indicator while
    the notifications are being retrieved.
    */
    if (isLoading) {

        return <LoadingSpinner />;

    }


    /*
    Page Layout
    */
    return (

        <PageContainer>

            <div className="space-y-8">

                {/* Read-only page: no save status. */}
                <PageHeader
                    title="Heart Rate Notifications"
                />

                <DateSection
                    selectedDate={selectedDate}
                    setSelectedDate={setSelectedDate}
                />

                {loadError && (
                    <div
                        className="
                            rounded-xl
                            border
                            border-red-200
                            bg-red-50
                            px-4
                            py-3
                            text-sm
                            text-red-700
                        "
                    >
                        Unable to load data. Please check your connection and try again.
                    </div>
                )}

                <CollapsibleCard
                    title="Notifications"
                    icon={BellRing}
                    iconColor="text-rose-600"
                >

                    {notifications.length === 0 ? (

                        <p className="text-sm text-slate-500">
                            No notifications on this date.
                        </p>

                    ) : (

                        <ul className="space-y-4">

                            {notifications.map((notification) => (

                                <li
                                    key={notification.startTime}
                                    className="
                                        rounded-xl
                                        border
                                        border-slate-200
                                        p-4
                                    "
                                >

                                    <div
                                        className="
                                            flex
                                            items-center
                                            justify-between
                                        "
                                    >
                                        <p className="font-medium text-slate-900">
                                            {notification.notificationType}
                                        </p>

                                        <p className="text-sm text-slate-500">
                                            {notification.startTime}
                                            {" – "}
                                            {notification.endTime}
                                        </p>
                                    </div>

                                    <dl
                                        className="
                                            mt-3
                                            grid
                                            grid-cols-2
                                            gap-2
                                            text-sm
                                            sm:grid-cols-4
                                        "
                                    >
                                        <div>
                                            <dt className="text-slate-500">Threshold</dt>
                                            <dd>{formatBpm(notification.thresholdBpm)}</dd>
                                        </div>

                                        <div>
                                            <dt className="text-slate-500">Min</dt>
                                            <dd>{formatBpm(notification.minHeartRateBpm)}</dd>
                                        </div>

                                        <div>
                                            <dt className="text-slate-500">Max</dt>
                                            <dd>{formatBpm(notification.maxHeartRateBpm)}</dd>
                                        </div>

                                        <div>
                                            <dt className="text-slate-500">Avg</dt>
                                            <dd>{formatBpm(notification.avgHeartRateBpm)}</dd>
                                        </div>
                                    </dl>

                                    <p className="mt-3 text-sm text-slate-500">
                                        Readings:{" "}
                                        <span className="text-slate-900">
                                            {notification.readings ?? "-"}
                                        </span>
                                    </p>

                                </li>

                            ))}

                        </ul>

                    )}

                </CollapsibleCard>

            </div>

        </PageContainer>

    );

}

export default HeartRateNotifications;
