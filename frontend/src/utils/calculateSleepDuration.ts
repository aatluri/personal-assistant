/*
    calculateSleepDuration

    Calculates the duration between two
    HH:mm time values.

    Returns:
    - "Xh Ym" if both times are present.
    - "-" if either time is missing.

    Supports sleep that crosses midnight.
*/

export function calculateSleepDuration(
    startTime: string,
    endTime: string
): string {
    /*
        Cannot calculate a duration unless
        both times have been entered.
    */

    if (!startTime || !endTime) {
        return "-";
    }

    /*
        Split each HH:mm string into
        hours and minutes.
    */

    const [startHour, startMinute] = startTime
        .split(":")
        .map(Number);

    const [endHour, endMinute] = endTime
        .split(":")
        .map(Number);

    /*
        Create Date objects so the
        time difference can be calculated.
    */
    const start = new Date();
    start.setHours(startHour, startMinute, 0, 0);

    const end = new Date();
    end.setHours(endHour, endMinute, 0, 0);

    /*
        If the end time is earlier than the
        start time, assume the sleep
        continued past midnight.
    */
    if (end < start) {
        end.setDate(end.getDate() + 1);
    }

    /*
        Calculate the duration in minutes.
    */
    const durationMinutes =
        (end.getTime() - start.getTime()) / 60000;

    /*
        Convert the duration into
        hours and minutes.
    */
    const hours = Math.floor(durationMinutes / 60);
    const minutes = durationMinutes % 60;

    /*
        Return a user-friendly string.
    */
    return `${hours}h ${minutes}m`;

}