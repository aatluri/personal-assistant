/*
dailyChart

What every Overview card's daily chart has in common:
- Day view shows the 7 days ending on the selected day,
  with that day highlighted.
- Week and Month views show every day, and tapping a day
  with data opens it in Day view.
*/

import type { DailyValues, DashboardSummary } from "../../../types/DashboardSummary";

import { formatChartLabels, formatDay } from "../../../utils/overviewFormat";


export interface DailyChartProps {
    labels: string[];
    highlightIndex?: number;
    onSelect?: (index: number) => void;
    describeBar: (index: number) => string;
}


/*
    summary
        The Overview summary; its days are the chart's bars.

    onSelectDay
        Opens a date in Day view.

    describeValue
        Text for one day's value, e.g. "9,210 steps" or
        "no data".
*/
export function dailyChartProps(
    summary: DashboardSummary,
    onSelectDay: (date: string) => void,
    describeValue: (day: DailyValues) => string,
): DailyChartProps {

    const isDay = summary.period === "day";

    return {
        labels: formatChartLabels(summary),
        highlightIndex: isDay ? summary.days.length - 1 : undefined,
        onSelect: isDay
            ? undefined
            : (index) => onSelectDay(summary.days[index].date),
        describeBar: (index) => {
            const day = summary.days[index];
            return `${formatDay(day.date)}: ${describeValue(day)}`;
        },
    };

}
