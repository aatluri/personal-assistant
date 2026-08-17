/*
    Calculates the duration between two
    HH:mm time values.

    If either value is missing, returns "-".

    Supports sleep that crosses midnight.
*/

export function calculateSleepDuration(
    startTime: string,
    endTime: string
): string {

    if (!startTime || !endTime) {
        return "-";
    }

    const [startHour, startMinute] = startTime
        .split(":")
        .map(Number);

    const [endHour, endMinute] = endTime
        .split(":")
        .map(Number);

    const start = new Date();
    start.setHours(startHour, startMinute, 0, 0);

    const end = new Date();
    end.setHours(endHour, endMinute, 0, 0);

    /*
        If the end time is earlier than the
        start time, the sleep crossed midnight.
    */
    if (end < start) {
        end.setDate(end.getDate() + 1);
    }

    const durationMinutes =
        (end.getTime() - start.getTime()) / 60000;

    const hours = Math.floor(durationMinutes / 60);
    const minutes = durationMinutes % 60;

    return `${hours}h ${minutes}m`;

}