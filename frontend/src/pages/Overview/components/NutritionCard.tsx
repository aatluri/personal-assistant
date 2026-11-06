/*
NutritionCard

Calories, protein and water against their goals, the
macro split, and how many days were logged.

Week and Month averages count only logged days (days
with calories; water counts on days with water), so an
unlogged day never pulls the average down. The coverage
line says how many days that was.
*/

import { Salad } from "lucide-react";

import type { DashboardSummary } from "../../../types/DashboardSummary";

import ProgressBar from "../../../components/ProgressBar";
import StackedBar from "../../../components/charts/StackedBar";

import { formatNumber, MISSING } from "../../../utils/overviewFormat";

import OverviewCard from "./OverviewCard";


/*
Energy per gram, for the macro split: protein and carbs
4 kcal, fat 9 kcal.
*/
const KCAL_PER_GRAM = { protein: 4, carbs: 4, fat: 9 };


interface NutritionCardProps {
    summary: DashboardSummary;
}

function NutritionCard({ summary }: NutritionCardProps) {

    const { current, goals } = summary;
    const isDay = summary.period === "day";

    const note = isDay
        ? (summary.isCurrent ? "today" : "this day")
        : "avg per logged day";

    let coverage: string;

    if (isDay) {
        coverage = current.nutritionDays > 0 ? "Logged" : "Nothing logged";
    } else {
        coverage = `Logged ${current.nutritionDays} of ${current.days} days`
            + (summary.isCurrent ? " so far" : "");
    }

    const protein = current.proteinGAverage;
    const waterLitres = current.waterMlAverage === null
        ? null
        : current.waterMlAverage / 1000;

    const macros = [
        {
            label: "Protein",
            value: (protein ?? 0) * KCAL_PER_GRAM.protein,
            colorClass: "bg-amber-700",
        },
        {
            label: "Carbs",
            value: (current.carbohydratesGAverage ?? 0) * KCAL_PER_GRAM.carbs,
            colorClass: "bg-amber-500",
        },
        {
            label: "Fat",
            value: (current.totalFatGAverage ?? 0) * KCAL_PER_GRAM.fat,
            colorClass: "bg-amber-300",
        },
    ];

    const hasMacros = macros.some((macro) => macro.value > 0);

    return (

        <OverviewCard
            title="Nutrition"
            icon={Salad}
            iconColor="text-amber-600"
            note={note}
        >

            <p className="text-2xl font-semibold text-slate-900">
                {formatNumber(current.dietaryEnergyKcalAverage)}
                <span className="ml-1 text-sm font-normal text-slate-500">kcal</span>
            </p>

            <div className="mt-3 space-y-3">
                <ProgressBar
                    label="Protein"
                    current={protein ?? 0}
                    goal={goals.proteinG}
                    color="bg-amber-600"
                    displayCurrent={protein === null ? MISSING : `${formatNumber(protein)} g`}
                    displayGoal={`${formatNumber(goals.proteinG)} g`}
                />

                <ProgressBar
                    label="Water"
                    current={waterLitres ?? 0}
                    goal={goals.waterMl / 1000}
                    color="bg-sky-500"
                    displayCurrent={waterLitres === null ? MISSING : `${formatNumber(waterLitres, 1)} L`}
                    displayGoal={`${formatNumber(goals.waterMl / 1000, 1)} L`}
                />
            </div>

            {hasMacros && (
                <StackedBar parts={macros} label="Macros (share of calories)" />
            )}

            <p className="mt-3 text-xs text-slate-400">{coverage}</p>

        </OverviewCard>

    );

}

export default NutritionCard;
