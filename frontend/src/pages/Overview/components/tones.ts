/*
Text colours for a change's tone, shared by the Overview's
headline numbers and cards.
*/

import type { Tone } from "../../../utils/overviewFormat";


export const TONE_CLASSES: Record<Tone, string> = {
    good: "text-green-700",
    bad: "text-red-700",
    neutral: "text-slate-500",
};
