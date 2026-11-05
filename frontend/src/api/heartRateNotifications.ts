/*
Heart Rate Notifications API

Communication layer between the Heart Rate Notifications
page and the backend. The page is read-only, so this
module only loads notifications.
*/

import type { HeartRateNotification } from "../types/HeartRateNotification";
import { API_BASE_URL } from "./config";


/*
Retrieves the heart rate notifications for a date,
earliest first.

The backend returns snake_case fields with full
datetimes; they are converted into the frontend
model, with times shown as HH:mm.
*/
export async function getHeartRateNotificationsByDate(
    date: string,
): Promise<HeartRateNotification[]> {

    const response = await fetch(
        `${API_BASE_URL}/health/heart-rate-notifications?notification_date=${encodeURIComponent(date)}`
    );

    if (!response.ok) {
        throw new Error(
            "Failed to load Heart Rate Notifications"
        );
    }

    const notifications = await response.json();

    return notifications.map(
        (notification: Record<string, unknown>): HeartRateNotification => ({

            date:
                notification.date as string,

            notificationType:
                notification.notification_type as string,

            /*
            "2026-10-29T08:00:08" -> "08:00"
            */
            startTime:
                (notification.start_time as string).substring(11, 16),

            endTime:
                (notification.end_time as string).substring(11, 16),

            thresholdBpm:
                (notification.threshold_bpm as number | null) ?? null,

            minHeartRateBpm:
                (notification.min_heart_rate_bpm as number | null) ?? null,

            maxHeartRateBpm:
                (notification.max_heart_rate_bpm as number | null) ?? null,

            avgHeartRateBpm:
                (notification.avg_heart_rate_bpm as number | null) ?? null,

            readings:
                (notification.readings as string | null) ?? null,

        })
    );
}
