/*
    NutritionSection

    Displays and updates today's meals
    and nutritional information.

    The actual state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextArea from "../../../components/TextArea";
import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent
    LogToday component.
*/
interface NutritionSectionProps {

    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function NutritionSection({

    dailyLog,

    setDailyLog,

}: NutritionSectionProps) {

    return (

        <section>

            {/* Section Heading */}
            <h2>Nutrition</h2>

            {/* ----------------------------- */}
            {/* Meals                         */}
            {/* ----------------------------- */}

            <TextArea
                label="Breakfast"
                id="breakfast"
                name="breakfast"
                rows={3}
                placeholder="Enter breakfast"
                value={dailyLog.nutrition.breakfast}
                onChange={(event) => {

                    const newBreakfast = event.target.value;

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            breakfast: newBreakfast,

                        },

                    }));

                }}
            />

            <TextArea
                label="Lunch"
                id="lunch"
                name="lunch"
                rows={3}
                placeholder="Enter lunch"
                value={dailyLog.nutrition.lunch}
                onChange={(event) => {

                    const newLunch = event.target.value;

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            lunch: newLunch,

                        },

                    }));

                }}
            />

            <TextArea
                label="Dinner"
                id="dinner"
                name="dinner"
                rows={3}
                placeholder="Enter dinner"
                value={dailyLog.nutrition.dinner}
                onChange={(event) => {

                    const newDinner = event.target.value;

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            dinner: newDinner,

                        },

                    }));

                }}
            />

            <TextArea
                label="Snacks"
                id="snacks"
                name="snacks"
                rows={3}
                placeholder="Enter snacks"
                value={dailyLog.nutrition.snacks}
                onChange={(event) => {

                    const newSnacks = event.target.value;

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            snacks: newSnacks,

                        },

                    }));

                }}
            />

            {/* ----------------------------- */}
            {/* Macronutrients                */}
            {/* ----------------------------- */}

            <TextInput
                label="Protein (g)"
                id="protein"
                name="protein"
                type="number"
                min={0}
                value={dailyLog.nutrition.protein}
                onChange={(event) => {

                    const newProtein = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            protein: newProtein,

                        },

                    }));

                }}
            />

            <TextInput
                label="Carbs (g)"
                id="carbs"
                name="carbs"
                type="number"
                min={0}
                value={dailyLog.nutrition.carbs}
                onChange={(event) => {

                    const newCarbs = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            carbs: newCarbs,

                        },

                    }));

                }}
            />

            <TextInput
                label="Fat (g)"
                id="fat"
                name="fat"
                type="number"
                min={0}
                value={dailyLog.nutrition.fat}
                onChange={(event) => {

                    const newFat = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            fat: newFat,

                        },

                    }));

                }}
            />

            <TextInput
                label="Fibre (g)"
                id="fibre"
                name="fibre"
                type="number"
                min={0}
                value={dailyLog.nutrition.fibre}
                onChange={(event) => {

                    const newFibre = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            fibre: newFibre,

                        },

                    }));

                }}
            />

            <TextInput
                label="Sugar (g)"
                id="sugar"
                name="sugar"
                type="number"
                min={0}
                value={dailyLog.nutrition.sugar}
                onChange={(event) => {

                    const newSugar = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            sugar: newSugar,

                        },

                    }));

                }}
            />

            <TextInput
                label="Calories Consumed"
                id="calories-consumed"
                name="caloriesConsumed"
                type="number"
                min={0}
                value={dailyLog.nutrition.caloriesConsumed}
                onChange={(event) => {

                    const newCaloriesConsumed = event.target.value === ""? "": Number(event.target.value);

                    setDailyLog((previousDailyLog) => ({

                        ...previousDailyLog,

                        nutrition: {

                            ...previousDailyLog.nutrition,

                            caloriesConsumed: newCaloriesConsumed,

                        },

                    }));

                }}
            />

        </section>

    );

}

export default NutritionSection;