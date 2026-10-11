/*
SleepMetrics

Defines the structure of the Sleep Metrics
object used throughout the frontend.

This interface represents the page state and is
shared between:
- API layer
- Page components
- Utility functions
*/

export interface SleepMetrics {

    /*
    Sleep record date in YYYY-MM-DD format.
    */
    date: string;

    /* ------------------------------ */
    /* Sleep Times                    */
    /* ------------------------------ */

    sleepStartTime: string;
    sleepEndTime: string;

    /* ------------------------------ */
    /* Sleep Duration                 */
    /* ------------------------------ */

    totalSleepDurationHr: number | "";

    /* ------------------------------ */
    /* Sleep Stages                   */
    /* ------------------------------ */

    coreSleepHr: number | "";
    deepSleepHr: number | "";

    awakeHr: number | "";
    remSleepHr: number | "";

    /* ------------------------------ */
    /* Source                         */
    /* ------------------------------ */

    source: string;

}