import type { SleepMetrics } from "../types/SleepMetrics";

/*
Creates an empty Sleep Metrics object.

Used when:
- No Sleep Metrics exist for the selected date.
- The page needs an initial empty state.
*/

export function createEmptySleepMetrics(): SleepMetrics {

    return {

        date: "",

        sleepStartTime: "",
        sleepEndTime: "",

        totalSleepDurationHr: "",

        coreSleepHr: "",
        deepSleepHr: "",

        awakeHr: "",
        remSleepHr: "",

        source: "",

    };

}