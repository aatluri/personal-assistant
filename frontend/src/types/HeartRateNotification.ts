/*
HeartRateNotification

One heart rate notification from the watch, such as a
low heart rate alert, as shown on the Heart Rate
Notifications page.

These come from Health Auto Export through the data
importer; the page only displays them.
*/

export interface HeartRateNotification {

    /*
    Notification date in YYYY-MM-DD format.
    */
    date: string;

    /*
    Readable label, e.g. "Low Heart Rate".
    */
    notificationType: string;

    /*
    Start and end time of the notification, as HH:mm.
    */
    startTime: string;
    endTime: string;

    /* ------------------------------ */
    /* Heart Rate                     */
    /* ------------------------------ */

    thresholdBpm: number | null;
    minHeartRateBpm: number | null;
    maxHeartRateBpm: number | null;
    avgHeartRateBpm: number | null;

    /*
    The heart rate readings in time order,
    e.g. "39, 40, 39, 39".
    */
    readings: string | null;

}
